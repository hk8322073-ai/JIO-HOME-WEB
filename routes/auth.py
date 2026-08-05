from fastapi import APIRouter, Header, HTTPException, status

from api.auth import sendOtp,verifyOtp,refreshToken,logOut
from models.auth import OTPRequest,OTPVerify,RefreshTokenRequest
from utils.utility import (
    refactor_otp_send_response,
    refactor_auth_response,
    refactor_refresh_token_response,
    refactor_logout_response
)

authRoute = APIRouter()

@authRoute.post("/otp/send")
async def send_otp(data:OTPRequest):
    return refactor_otp_send_response(
                await sendOtp(mobile_num=data.mobileNum)
            )

@authRoute.post("/otp/verify")
async def verify_otp(data:OTPVerify):
    response =  await verifyOtp(
                    mobile_num=data.mobileNum,
                    otp=data.otp
                )
    
    return refactor_auth_response(response)

@authRoute.post("/refreshToken")
async def refresh_token(data:RefreshTokenRequest):
    return refactor_refresh_token_response(
        await refreshToken(
            tokenIdentifier = data.token_identifier,
            refreshToken = data.refresh_token
            )
        )
    
@authRoute.post("/logout")
async def log_out(
            user_token: str | None = Header(None, alias="userToken"),
            token_identifier: str | None = Header(None, alias="tokenIdentifier")
        ):
    if user_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing userToken headers"
        )
    if token_identifier is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing tokenIdentifier headers"
        )
    return refactor_logout_response(
            await logOut(
                    userToken=user_token,
                    tokenIdentifier=token_identifier
                )
            )