from typing import Any
from fastapi.responses import JSONResponse

from configs.jioConfig import appId,apiKey,appVersion,userName
from configs.deviceConfig import mobileOs,mobileOsVersion,get_random_android_id,get_random_mobile_model

from .urls import host

def get_auth_header(userId:str) -> dict[str,str]:
    return {
        'Host': host,
        'userId': userId,                     # For Mobile No. starting with +91<mob_no>
        'appId': appId,
        'apiKey': apiKey,
        'Connection': 'close',
        'Accept': 'application/protobuf,application/json',
        'Accept-Charset': 'UTF-8',
        'User-Agent': 'Ktor client',
        'Content-Type': 'application/json'
    }

def get_refresh_token_header(tokenIdentifier:str) -> dict[str,str]:
    return  {
        'tokenIdentifier': tokenIdentifier,
        'refreshSSO': 'F',
        'refreshUserToken': 'T',
        'Connection': 'close',
        'Accept': 'application/protobuf,application/json',
        'Accept-Charset': 'UTF-8',
        'User-Agent': 'Ktor client',
        'Content-Type': 'application/json',
        'Host': host,
    }
    
def get_authorised_header(Authorization:str,tokenIdentifier:str) -> dict[str,str]:
    return {
        'Host': host,
        'Tokenidentifier': tokenIdentifier,
        'Authorization': f'Bearer {Authorization}',
        'User-Agent': 'okhttp/5.0.0-alpha.11',
    }

def get_refresh_token_json(refreshToken:str):
    mobileModel = get_random_mobile_model()
    androidId = get_random_android_id()
    return {
        'dataObject': {
            'consumptionDeviceName': mobileModel,
            'info': {
                'androidId': androidId,
                'platform': {
                    'name': mobileOs,
                },
                'type': mobileOs,
            },
        },
        'refreshToken': refreshToken,
    }
    
def get_auth_otp_verify_json(mob_no:str,otp:str):
    mobileModel = get_random_mobile_model()
    androidId = get_random_android_id()
    
    # From JIO HOME Api req
    return {
        'dataObject': {
            'consumptionDeviceName': mobileModel,
            'info': {
                'androidId': androidId,
                'platform': {
                    'name': mobileOs,
                },
                'type': mobileOs,
            },
        },
        'identifier': mob_no,
        'otp': otp,
        'rememberUser': 'T',
        'returnSessionDetails': 'T',
        'shallBecomeIdentifierIfNotTaken': 'T',
        'upgradeAuth': 'Y',
        'userInfo': {
            'clientAppName': appId,
            'clientAppVersion': appVersion,
            'deviceUuid': androidId,
            'mobileModel': mobileModel,
            'mobileOs': mobileOs,
            'mobileOsVersion': mobileOsVersion,
            'userName': userName,
        },
    }
    
def refactor_otp_send_response(response:dict[str,Any]) -> JSONResponse:
    status_code = 200
    status = response["status"]
    msg = "OTP sent successfully"
    if (status == "FAILURE"):
        status_code = 400
        msg = response["message"]
        
    return JSONResponse(
        status_code = status_code,
        content = {
            "status" : status,
            "message" : msg
        }
    )
    
def refactor_refresh_token_response(response:dict[str,Any]) -> JSONResponse:
    status = response["status"]
    if (status == "FAILURE"):
        return JSONResponse(
            status_code = 404,
            content = {
                "status" : status,
                "message" : response["status"]
            }
        )
    return JSONResponse(
        status_code = 200,
        content = {
            "status" : status,
            "message" : "user token refreshed",
            "userToken" : response["data"]["userToken"]
        }
    )
    
def refactor_auth_response(response:dict[str,Any]) -> JSONResponse:
    status = response["status"]
    msg = response["message"]
    data = response.get("data")
    
    if (not data):
        return JSONResponse(
            status_code = 400,
            content = {
                "status" : status,
                "message" : msg
            }
        )
        
    content = {
        "status" : status,
        "message" : msg,
        "userToken" : data["userToken"],
        "tokenIdentifier" : data["tokenIdentifier"],
        "refreshToken" : data["refreshToken"],
        "user" : data["sessionAttributes"]["user"]
    }
    status_code = 200
    
    if (status == "FAILURE"):
        content["status"] = "MAX-USER"
        content["existingSessions"] = data["existingSessions"]
        status_code = 406
        
    return JSONResponse(
        status_code = status_code,
        content = content 
    )
    
def refactor_logout_response(response:dict[str,Any]) -> JSONResponse | None:
    status = response["status"]
    if (status == "FAILURE"):
        return JSONResponse(
            status_code = 401,
            content = {
                "status":status,
                "message":response["message"]
            }
        )
    return None