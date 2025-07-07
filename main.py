from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
import httpx
from sqlalchemy.orm import Session
import os
import tempfile
from adapters.fast_alpr_recognizer import FastAlprRecognizer
from adapters.ipify_ip_recollector import IpifyIpRecollector
from database import get_db
from resources import ServerRequestsOpeningIn
import uuid

# 1. Servers URLs
MAIN_SERVER_URL = "http://main-server-address:port"
ESP32_URL = "http://esp32-local-ip:port"
EDGE_NODE_PORT = 8000
# 2. Declare server
app = FastAPI()
# 3. Get Adapters
ip_recollector = IpifyIpRecollector()
recognizer = FastAlprRecognizer()
# 4. Startup
@app.on_event("startup")
async def startup():
    # 4.1. Get public IP
    ip = ip_recollector.get_ip()
    # 4.2. Activate on main server, get an identity from there
    async with httpx.AsyncClient() as client:
        activate_response = await client.post(f"{MAIN_SERVER_URL}/activate", json={"ip": ip, "port": EDGE_NODE_PORT})
        identity = activate_response.json()
        # 4.3. Save Identity on persistence

        # 4.4. Copy users
        users_response = await client.post(f"{MAIN_SERVER_URL}/users")
        users = users_response.json()
        # 4.5. Save missing users to persistence
# 5. Root Directory
@app.get("/")
async def root():
    return {"message": "Hello World"}
# 6. 1/3 Endpoint: miniClientRequestOpening() for ESP32 Exit
@app.post("/miniClientRequestsOpening")
async def mini_client_requests_opening(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 6.1. Save/upload file, run OCR
    # 6.2. Lookup plate in LicensePlate table
    # 6.3.
    pass
# 7. 2/3 Endpoint: serverRequestsOpening() for Server
@app.post("/serverRequestsOpening")
async def server_requests_opening(
        req: ServerRequestsOpeningIn,
        db: Session = Depends(get_db)
):
    # 1. Ask ESP32 Entry for a photo
    async with httpx.AsyncClient() as client:
        try:
            image_resp = await client.get(f"{ESP32_URL}/image")
            image_bytes = image_resp.content
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        # 2. OCR the photo
        plate_text = ""
        try:
            ext = "png"
            temp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}{ext}")
            with open(temp_path, 'wb') as f:
                f.write(image_bytes)
            plate_text = recognizer.recognize(temp_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        # 3. Save it + request opening + send it back to the server

# 8. 3/3 Endpoint: getQR() for ESP32 Screen
@app.get("/getIdentity")
async def get_identity(db: Session = Depends(get_db)):
    pass