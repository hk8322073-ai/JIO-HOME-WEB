host = "api.jiohome.jio.com"

auth_url = f"https://{host}/auth/v2"
send_otp_url = f"{auth_url}/otp/send"
verify_otp_url = f"{auth_url}/otp/verify"
refresh_token_url = f"{auth_url}/refreshToken"
logout_url = f"{auth_url}/logout"

connection_details_url = f"https://{host}/jh-frontend/v2/app/users/connections"
customer_url = f"https://{host}/plume/api/Customers/{{customerId}}/locations/{{locationId}}"  # (customerId,locationId) Can be added with string formatting i.e .format/.format_map

wifi_network_details_url = f"{customer_url}/wifiNetwork"
node_details_url = f"{customer_url}/nodes"
connected_devices_details_url = f"{customer_url}/devices"
profiles_details_url = f"{customer_url}/persons"
