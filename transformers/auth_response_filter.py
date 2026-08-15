from fastapi.responses import JSONResponse
from typing import Any

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
                "message" : response["message"]
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