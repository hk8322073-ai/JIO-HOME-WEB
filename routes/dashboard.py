from fastapi import APIRouter, Request, HTTPException, status
from api.dashboard import getConnectionDetails, getNodes, getWifiNetworkDetails, getDevices, getProfiles
from models.dashboard import CustomerLocationPayload
from transformers.dashboard_response_filter import (
    refactor_connection_response,
    refactor_node_details_response,
    refactor_wifi_details,
    refactor_device_details,
    refactor_profile_details
)

dashboardRoute = APIRouter()

@dashboardRoute.post("/user")
async def get_connection_details(request: Request):
    """Retrieve user connection details and account information."""
    userToken = request.headers.get("userToken","default")
    tokenIdentifier = request.headers.get("tokenIdentifier","default")
    
    try:
        response = await getConnectionDetails(
            userToken=userToken,
            tokenIdentifier=tokenIdentifier
        )
        return refactor_connection_response(response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user details."
        )
    
@dashboardRoute.post("/nodes")
async def get_nodes(data: CustomerLocationPayload, request: Request):
    """Retrieve network nodes information for a customer location."""
    userToken = request.headers.get("userToken","default")
    tokenIdentifier = request.headers.get("tokenIdentifier","default")
    
    try:
        response = await getNodes(
            data=data.model_dump(),
            userToken=userToken,
            tokenIdentifier=tokenIdentifier
        )
        return refactor_node_details_response(response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve nodes information."
        )
    
@dashboardRoute.post("/wifi")
async def get_wifi_networks_details(data: CustomerLocationPayload, request: Request):
    """Retrieve WiFi network details for a customer location."""
    userToken = request.headers.get("userToken","default")
    tokenIdentifier = request.headers.get("tokenIdentifier","default")
    
    try:
        response = await getWifiNetworkDetails(
            data=data.model_dump(),
            userToken=userToken,
            tokenIdentifier=tokenIdentifier
        )
        return refactor_wifi_details(response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve WiFi network details."
        )
    
@dashboardRoute.post("/devices")
async def get_devices(data: CustomerLocationPayload, request: Request):
    """Retrieve connected devices for a customer location."""
    userToken = request.headers.get("userToken","default")
    tokenIdentifier = request.headers.get("tokenIdentifier","default")
    
    try:
        response = await getDevices(
            data=data.model_dump(),
            userToken=userToken,
            tokenIdentifier=tokenIdentifier
        )
        return refactor_device_details(response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve device information."
        )
        
@dashboardRoute.post("/profiles")
async def get_profiles(data: CustomerLocationPayload, request: Request):
    """Retrieve user profiles/configurations for a customer location."""
    userToken = request.headers.get("userToken","default")
    tokenIdentifier = request.headers.get("tokenIdentifier","default")
    
    try:
        response = await getProfiles(
            data=data.model_dump(),
            userToken=userToken,
            tokenIdentifier=tokenIdentifier
        )
        return refactor_profile_details(response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve profile information."
        )
        