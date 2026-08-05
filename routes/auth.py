from fastapi import APIRouter

from api.auth import sendOtp,verifyOtp,refreshToken
from models.auth import OTPRequest,OTPVerify,RefreshTokenRequest
from utils.utility import refactor_otp_send_response,refactor_auth_response,refactor_refresh_token_response

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