from configs.deviceConfig import mobileOs,mobileOsVersion,get_random_android_id,get_random_mobile_model
from configs.jioConfig import appId,appVersion,userName

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
