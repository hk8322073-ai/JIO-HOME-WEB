from pydantic import BaseModel

class OTPRequest(BaseModel):
    mobileNum: str
    
class OTPVerify(BaseModel):
    mobileNum: str
    otp: str
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str
    token_identifier: str