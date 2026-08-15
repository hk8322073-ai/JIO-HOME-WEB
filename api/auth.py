from utils.urls import send_otp_url,verify_otp_url,refresh_token_url,logout_url
from utils.utility import (
    get_auth_header,
    get_refresh_token_header,
    get_authorised_header
)
from transformers.auth_request_mapper import get_auth_otp_verify_json,get_refresh_token_json

from api.client import client

async def sendOtp(mobile_num:str):  
    headers = get_auth_header(userId=mobile_num)
    async with client.session.post(send_otp_url,headers=headers) as res:
        return await res.json()
    
async def verifyOtp(mobile_num:str,otp:str):    
    headers = get_auth_header(userId=mobile_num)
    json_data = get_auth_otp_verify_json(mob_no=mobile_num,otp=otp)
    
    async with client.session.post(verify_otp_url,headers=headers,json=json_data) as res:
        return  await res.json()
    
async def logOut(userToken:str,tokenIdentifier:str):
    headers = get_authorised_header(
                    Authorization=userToken,
                    tokenIdentifier=tokenIdentifier
                )
    async with client.session.post(logout_url,headers=headers) as res:
        return  await res.json()
    
async def refreshToken(tokenIdentifier:str,refreshToken:str):    
    headers = get_refresh_token_header(tokenIdentifier)
    json_data = get_refresh_token_json(refreshToken)
    
    async with client.session.post(refresh_token_url,headers=headers,json=json_data) as res:
        return  await res.json()
    
