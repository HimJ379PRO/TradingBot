import socket
import uuid
import requests

# AngelOne SmartAPI configuration
# Historical API
API_KEY = "my_api_key"
SECRET_KEY = "my_secret_key"
CLIENT_ID = "my_client_id"
TOTP_SECRET = "my_totp_secret" # For 2FA (if using pyotp) 

# === System Info ===
def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "0.0.0.0"

def get_mac_address():
    mac = uuid.getnode()
    return ':'.join(['{:02x}'.format((mac >> ele) & 0xff) for ele in range(40, -8, -8)]).upper()

# Fetch system values on import
LOCAL_IP = get_local_ip()
PUBLIC_IP = get_public_ip()
MAC_ADDRESS = get_mac_address()

if __name__ == "__main__":
    print("LOCAL IP: "+LOCAL_IP, "PUBLIC IP: "+PUBLIC_IP, "MAC ADDRESS: "+MAC_ADDRESS, sep="\n")