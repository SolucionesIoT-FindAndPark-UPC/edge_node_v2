from pydantic import BaseModel

# 1. /serverRequestsOpening()
class ServerRequestsOpeningIn(BaseModel):
    user_id: int
class ServerRequestsOpeningOut(BaseModel):
    open: bool
    plate: str = None
# 2. /miniClientRequestsOpening()
# 3. /getIdentity()