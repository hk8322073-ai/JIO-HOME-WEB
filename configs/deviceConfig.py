from random import choice
import secrets

ANDROID_BUILD_MODELS = [
    "Pixel 9",
    "Pixel 9 Pro",
    "Pixel 8",
    "Pixel 8 Pro",
    "Pixel 7",
    "Pixel 7 Pro",
    "Pixel 6a",
    "SM-S918B",        
    "SM-S928B",        
    "SM-S926B",        
    "SM-S921B",        
    "SM-A546E",        
    "SM-A556E",        
    "SM-M546B",        
    "SM-F946B",        
    "SM-F731B",        
    "CPH2449",         
    "CPH2581",         
    "LE2123",          
    "2201123G",        
    "2211133G",        
    "23049PCD8G",      
    "2312DRA50G",      
    "M2102J20SG",      
    "2201116PG",       
    "V2230",           
    "V2303",           
    "RMX3561",         
    "RMX3840",         
    "CPH2487",         
    "PGEM10",          
    "NE2215",          
    "M2012K11AG",      
]

mobileOs = "android"
mobileOsVersion = "32"

def get_random_mobile_model() -> str:
    return choice(ANDROID_BUILD_MODELS)

def get_random_android_id() -> str:
    return secrets.token_hex(8)