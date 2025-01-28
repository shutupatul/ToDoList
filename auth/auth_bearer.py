from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt_handler import decode_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid or expired token")
            return credentials.credentials
        raise HTTPException(status_code=403, detail="Invalid authorization")

    def verify_jwt(self, jwt_token: str):
        try:
            payload = decode_token(jwt_token)
            return True
        except:
            return False
