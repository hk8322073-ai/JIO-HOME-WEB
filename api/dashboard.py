from api.client import client
from utils.utility import get_authorised_header
from utils.urls import (
    connection_details_url,
    node_details_url,
    wifi_network_details_url,
    profiles_details_url,
    connected_devices_details_url
)

async def getConnectionDetails(userToken:str,tokenIdentifier:str):
    headers = get_authorised_header(
        Authorization = userToken,
        tokenIdentifier = tokenIdentifier
    )
    async with client.session.get(connection_details_url,headers=headers) as res:
        return await res.json()
    
async def getNodes(data:dict[str,str],userToken:str,tokenIdentifier:str):
    headers = get_authorised_header(
        Authorization = userToken,
        tokenIdentifier = tokenIdentifier
    )
    url = node_details_url.format_map(data)
    
    async with client.session.get(url,headers=headers) as res:
        return await res.json()
    
async def getWifiNetworkDetails(data:dict[str,str],userToken:str,tokenIdentifier:str):
    headers = get_authorised_header(
        Authorization = userToken,
        tokenIdentifier = tokenIdentifier
    )
    url = wifi_network_details_url.format_map(data)
    
    async with client.session.get(url,headers=headers) as res:
        return await res.json()
    
async def getDevices(data:dict[str,str],userToken:str,tokenIdentifier:str):
    headers = get_authorised_header(
        Authorization = userToken,
        tokenIdentifier = tokenIdentifier
    )
    url = connected_devices_details_url.format_map(data)
    
    async with client.session.get(url,headers=headers) as res:
        return await res.json()
    
async def getProfiles(data:dict[str,str],userToken:str,tokenIdentifier:str):
    headers = get_authorised_header(
        Authorization = userToken,
        tokenIdentifier = tokenIdentifier
    )
    url = profiles_details_url.format_map(data)
    
    async with client.session.get(url,headers=headers) as res:
        return await res.json()
    
    