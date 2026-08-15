from fastapi import APIRouter, Depends, Request, HTTPException, status
from api.auth import sendOtp, verifyOtp, refreshToken, logOut
from models.auth import OTPRequest, OTPVerify, RefreshTokenRequest
from utils.utility import verify_auth
from transformers.auth_response_filter import (
    refactor_otp_send_response,
    refactor_auth_response,
    refactor_refresh_token_response,
    refactor_logout_response
)

authRoute = APIRouter()

@authRoute.post("/otp/send")
async def send_otp(data: OTPRequest):
    """
    Send OTP to the provided mobile number.
    
    Args:
        data: OTPRequest containing mobileNum
        
    Returns:
        dict: Response with success status and message
        
    Raises:
        HTTPException: If OTP sending fails
    """
    try:
        response = await sendOtp(mobile_num=data.mobileNum)
        return refactor_otp_send_response(response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP. Please try again."
        )

@authRoute.post("/otp/verify")
async def verify_otp(data: OTPVerify):
    """
    Verify OTP and return authentication tokens.
    
    Args:
        data: OTPVerify containing mobileNum and otp
        
    Returns:
        dict: Response with userToken, tokenIdentifier, and refreshToken
        
    Raises:
        HTTPException: If OTP verification fails
    """
    try:
        response = await verifyOtp(
            mobile_num=data.mobileNum,
            otp=data.otp
        )
        return refactor_auth_response(response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid OTP. Please try again."
        )

@authRoute.post("/refreshToken")
async def refresh_token(data: RefreshTokenRequest):
    """
    Refresh the authentication token.
    
    Args:
        data: RefreshTokenRequest containing refresh_token and token_identifier
        
    Returns:
        dict: Response with new userToken and tokenIdentifier
        
    Raises:
        HTTPException: If token refresh fails
    """
    try:
        response = await refreshToken(
            tokenIdentifier=data.token_identifier,
            refreshToken=data.refresh_token
        )
        return refactor_refresh_token_response(response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to refresh token. Please login again."
        )
    
@authRoute.post("/logout", dependencies=[Depends(verify_auth)])
async def log_out(request: Request):
    """
    Logout the user and invalidate the session.
    
    Args:
        request: Request object containing auth headers
        
    Returns:
        dict: Response with logout status
        
    Raises:
        HTTPException: If logout fails
    """
    userToken = request.headers.get("userToken","default")
    tokenIdentifier = request.headers.get("tokenIdentifier","default")
    
    try:
        response = await logOut(
            userToken=userToken,
            tokenIdentifier=tokenIdentifier
        )
        return refactor_logout_response(response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to logout. Please try again."
        )