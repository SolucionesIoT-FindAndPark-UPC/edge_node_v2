from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
import httpx
from sqlalchemy.orm import Session
import os
import tempfile

from adapters.esp32_servers_service import Esp32ServersService
from adapters.fast_alpr_recognizer import FastAlprRecognizer
from adapters.identity_mysql_repository import IdentityMySqlRepository
from adapters.ipify_ip_recollector import IpifyIpRecollector
from adapters.main_server_service import MainServerService
from database import get_db, SessionLocal
from resources import ServerRequestsOpeningIn
from models import User
import uuid
import threading
import socket
from schemas import CreateIdentityCommand
from zeroconf import Zeroconf, ServiceInfo

zeroconf: Zeroconf | None = None
info: ServiceInfo | None = None

def register_mdns_service(local_ip, port):
    global zeroconf, info
    zeroconf = Zeroconf()
    info = ServiceInfo(
        "_http._tcp.local.",
        "localedge._http._tcp.local.",
        addresses=[socket.inet_aton(local_ip)],
        port=port,
        properties={},
        server="localedge.local."
    )
    zeroconf.register_service(info)
    print(f"mDNS registered: localedge.local at {local_ip}:{port}")

# 1. Servers URLs
MAIN_SERVER_URL = "http://127.0.0.1:8080/api/v1"
EDGE_NODE_PORT = 8000
# 2. Declare server
app = FastAPI()
# 3. Get Adapters
ip_recollector = IpifyIpRecollector()
recognizer = FastAlprRecognizer()
identity_repository = IdentityMySqlRepository()
main_server_service = MainServerService()
esp32_servers_service = Esp32ServersService()
# 4. Startup
@app.on_event("startup")
async def startup():
    # 4.0. Get Database session
    db = SessionLocal()
    # 4.0.1. Get local IP
    local_ip = ip_recollector.get_local_ip()
    # 4.0.2. Register mDNS
    thread = threading.Thread(target=register_mdns_service, args=(local_ip, EDGE_NODE_PORT))
    thread.daemon = True
    thread.start()
    # 4.1. Get public IP
    ip = ip_recollector.get_ip()
    # 4.2. Check if it has a saved identity, that will define the payload
    identity = identity_repository.get_identity(db)
    payload = None
    url = ""
    if identity is None:
        payload = {
            "url": local_ip,
            "port": EDGE_NODE_PORT,
        }
        # 4.3. No id: create edge node.
        async with httpx.AsyncClient() as client:
            activate_response = await client.post(f"{MAIN_SERVER_URL}/edgenodes", json=payload)
            response = activate_response.json()
            if activate_response.status_code != 200:
                raise Exception(f"Activation failed: {activate_response.status_code} - {activate_response.text}")
            # 4.4. Save Identity on persistence
            if identity is None:
                identity_repository.create_identity(db, CreateIdentityCommand(id=response["id"]))
    else:
        payload = {
            "id": identity.id,
            "url": local_ip,
            "port": EDGE_NODE_PORT,
        }
        # 4.3. Has id: update edge node
        async with httpx.AsyncClient() as client:
            activate_response = await client.put(f"{MAIN_SERVER_URL}/edgenodes/{identity.id}", json=payload)
            if activate_response.status_code != 200:
                raise Exception(f"Activation failed: {activate_response.status_code} - {activate_response.text}")
    # 5. Delete all users
    try:
        # 1. Delete all local users
        db.query(User).delete()
        db.commit()
        # 2. Get all users
        user_resources = main_server_service.get_all_users()
        # 3. Save to db
        for user in user_resources:
            role = user["roles"][0] if user.get("roles") else ""
            db.add(User(
                id=user["id"],
                username=user["username"],
                role=role
            ))
        db.commit()
        print(f"Synced {len(user_resources)} users from big server.")
    except Exception as e:
        print(f"Error syncing users: {e}")
        db.rollback()
    finally:
        db.close()
# 5. Root Directory
@app.get("/")
async def root():
    ip = ip_recollector.get_ip()
    local_ip = ip_recollector.get_local_ip()
    return {"ip": ip, "port": EDGE_NODE_PORT, "local_ip": local_ip}
# 6. 1/3 Endpoint: miniClientRequestOpening() for ESP32 Exit
@app.post("/miniClientRequestsOpening")
async def mini_client_requests_opening(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 6.1. Save/upload file, run OCR
    # 6.2. Lookup plate in LicensePlate table
    # 6.3.
    pass
# 7. 2/3 Endpoint: letSomeoneEnter() for Server
@app.post("/let_someone_enter")
async def let_someone_enter(
        req: ServerRequestsOpeningIn,
):
    esp32_servers_service.open_entry()

# 8. 3/3 Endpoint: getIdentity() for ESP32 Screen
@app.get("/getIdentity")
async def get_identity():
    db = SessionLocal()
    identity = identity_repository.get_identity(db)
    return identity.id
# 9. 4/3 Endpoint: mvpServers()
@app.on_event("shutdown")
def shutdown_mdns():
    global zeroconf, info
    if zeroconf and info:
        zeroconf.unregister_service(info)
        zeroconf.close()