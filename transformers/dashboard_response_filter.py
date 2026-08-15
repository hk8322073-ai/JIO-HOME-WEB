from fastapi.responses import JSONResponse
from typing import Any

def refactor_connection_response(response:dict[str,Any]) -> JSONResponse:
    connections = response.get("connections")    
    if (not connections):
        return JSONResponse(
            status_code = 401,
            content = {
                "status" : False,
                "message" : "Invalid JWTToken/tokenIdenfier or something went wrong!"
            }
        )
        
    filtered_connection = [filter_one_connection(connection) for connection in connections]
    return JSONResponse(
        status_code = 200,
        content = {
            "status" : True,
            "message" : "Connection fetched",
            "connections" : filtered_connection
        }
    )
    
def filter_one_connection(connection:dict[str,str]) -> dict[str,str]:
    return {
        "deviceType":connection["deviceType"],
        "serialNumber":connection["serialNumber"],
        "plumeLocationId":connection["plumeLocationId"],
        "mobile":connection["mobile"],
        "plumeCustomerId":connection["plumeCustomerId"],
        "connectionType":connection["connectionType"],
        "accountId":connection["accountId"],
        "zone":connection["zone"],
        "name":connection["name"],
        "customerId":connection["customerId"],
        "email":connection["email"],
        "gatewayId":connection["gatewayId"],
        "fixedLineNumber":connection["fixedLineNumber"],
    }

def refactor_node_details_response(response:dict[str,Any]) -> JSONResponse:
    nodes = response.get("nodes")    
    if (not nodes):
        return JSONResponse(
            status_code = 401,
            content = {
                "status" : False,
                "message" : "Invalid JWTToken/tokenIdenfier or something went wrong!"
            }
        )
    filtered_nodes = [filter_one_node(node) for node in nodes]
    return JSONResponse(
        status_code = 200,
        content = {
            "status" : True,
            "message" : "Success",
            "connections" : filtered_nodes
        }
    )

def filter_one_node(node:dict[str,Any]) -> dict[str,Any]:
    return {
      "id": node["id"],
      "connectionState": node["connectionState"],
      "model": node["model"],
      "mac": node["mac"],
      "ip": node["ip"],
      "backhaulType": node["backhaulType"],
      "defaultName": node["defaultName"],
      "serialNumber": node["serialNumber"],
      "ipv6": node["ipv6"],
      "firmwareVersion": node["firmwareVersion"],
      "platformVersion": node["platformVersion"],
      "connectedDeviceCount": node["connectedDeviceCount"],
      "connectionStateChangeAt": node["connectionStateChangeAt"],
      "networkMode": node["networkMode"],
      "packId": node["packId"],
      "speedTest": node["speedTest"],
      "manufacturerSerialNumber": node["manufacturerSerialNumber"],
      "bootAt": node["bootAt"],
      "publicIp": node["publicIp"],
      "linkStates": map_ethernet(node["linkStates"]),
      "openSyncVersion": node["openSyncVersion"],
      "health": node["health"]
    }


def map_ethernet(ethernets:list[dict[str,Any]]):
    for ethernet in ethernets:
        ifName = ethernet["ifName"]
        duplex = ethernet["duplex"]
        linkSpeed = ethernet["linkSpeed"]
        isUplink = ethernet["isUplink"]
        hasEthClient = ethernet["hasEthClient"]
        
        if ("." in ifName):
            parentInterface = ethernet["parentInterface"]
            vlanId = ifName.split(".")[1]
            return {
                "ifName": ifName,
                "ifType": "vlan",
                "parentInterface": parentInterface,
                "vlanId": vlanId,
                "duplex": duplex,
                "linkSpeed": linkSpeed,
                "isUplink": isUplink,
                "hasEthClient": hasEthClient
                }
    
        return {
            "ifName": ifName,
            "ifType": "ethernet",
            "duplex": duplex,
            "linkSpeed": linkSpeed,
            "isUplink": isUplink,
            "hasEthClient": hasEthClient
            }
    
def refactor_wifi_details(response:dict[str,Any]) -> JSONResponse:
    if (response.get("status",True) == "FAILURE"):                   
        return JSONResponse(
                    status_code = 401,
                    content = {
                        "status" : False,
                        "message" : "Invalid JWTToken/tokenIdenfier or something went wrong!"
                    }
                )
    wifiNetwork = response["wifiNetwork"]
    
    return JSONResponse(
        status_code = 200,
        content = {
            "status" : True,
            "message" : "Success",
            "encryptionKey": wifiNetwork["encryptionKey"],
            "ssid": wifiNetwork["ssid"],
            "masterKeyIndex": wifiNetwork["masterKeyIndex"],
            "encryption": wifiNetwork["encryption"],
            "wpaMode":wifiNetwork["wpaMode"],
            "encryptionMode": wifiNetwork["encryptionMode"],
            "ssidBroadcast": wifiNetwork["ssidBroadcast"],
            "enabled": wifiNetwork["enabled"],
            "createdAt": wifiNetwork["createdAt"],
            "updatedAt": wifiNetwork.get("updatedAt"),
            "id": wifiNetwork["id"],
            "locationId": wifiNetwork["locationId"],
            "keys": wifiNetwork["keys"],
            "persons": wifiNetwork["persons"],
            "encrypted": wifiNetwork["encrypted"],
            "encryptedAt": wifiNetwork["encryptedAt"]
        }
    )


def refactor_device_details(response:dict[str,Any]) -> JSONResponse:
    if (response.get("status",True) == "FAILURE"):                   
        return JSONResponse(
                    status_code = 401,
                    content = {
                        "status" : False,
                        "message" : "Invalid JWTToken/tokenIdenfier or something went wrong!"
                    }
                )
    
    devices:list[dict[str,Any]] = response["devices"]
    
    return JSONResponse(
            status_code = 200,
            content = {
                "status" : True,
                "message" : "Success",
                "devices" : [filter_one_device(device) for device in devices]
            }
            )

def filter_one_device(device:dict[str,Any]) -> dict[str,Any]:
    return  {
      "mac": device["mac"],
      "hostName": device["hostName"],
      "medium": device["medium"],
      "connectionState": device["connectionState"],
      "connectionStateChangeAt": device["connectionStateChangeAt"],
      "vapType": device["vapType"],
      "networkId": device["networkId"],
      "favorite": device["favorite"],
      "ip": device["ip"],
      "ipv6": device["ipv6"],
      "channel": device.get("channel","Unknown"),
      "freqBand": device.get("freqBand","Unknown"),
      "name": device["name"],
      "category": device["category"],
      "osName": device.get("osName","Unknown"),
      "health": device["health"],
      "freeze": device["freeze"],
      "firstConnectedAt": device["firstConnectedAt"],
      "nickname": device["nickname"],
      "wpaMode": device["wpaMode"],
      "deviceId": device["deviceId"],
      "groupOfUnassignedDevices": device.get("groupOfUnassignedDevices","Unknown")
    }
    
def refactor_profile_details(response:dict[str,Any]) -> JSONResponse:
    if (isinstance(response,dict)):                   
        return JSONResponse(
                    status_code = 401,
                    content = {
                        "status" : False,
                        "message" : "Invalid JWTToken/tokenIdenfier or something went wrong!"
                    }
                )
    return JSONResponse(
        status_code = 200,
        content ={
            "status" : True,
            "message" : "Success",
            "profiles":[
                {
                    "id": profile["id"],
                    "nickname": profile["nickname"],
                    "firstName": profile["firstName"],
                    "lastName": profile["lastName"],
                    "imageId": profile["imageId"],
                    "profile": profile["profile"],
                    "type": profile["type"],
                    "createdAt": profile["createdAt"],
                    "locationId": profile["locationId"],
                    "freeze": profile["freeze"],
                    "connectionState": profile["connectionState"],
                    "connectionStateChangeAt": profile["connectionStateChangeAt"]
                } 
            for profile in response
            ]
        }
    )
