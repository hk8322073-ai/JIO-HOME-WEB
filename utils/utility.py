from fastapi import Header,HTTPException,status

from configs.jioConfig import appId,apiKey

from .urls import host

async def verify_auth(
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

