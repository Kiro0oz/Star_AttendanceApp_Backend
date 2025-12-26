# attendance/utils.py
import json
import time
from cryptography.fernet import Fernet
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

try:
    FERNET = Fernet(settings.FERNET_KEY.encode()) 
except:
    raise Exception("FERNET_KEY is not configured in settings.") 


QR_CODE_LIFETIME_SECONDS = 90 

def generate_encrypted_qr_data(user_id, session_id, committee_id):
    
    timestamp_utc = int(time.time())
    expiry_utc = timestamp_utc + QR_CODE_LIFETIME_SECONDS

    data_payload = {
        'user_id': user_id,
        'session_id': session_id,
        'committee_id': committee_id,
        'timestamp': timestamp_utc, 
        'expiry': expiry_utc,       
    }
    
    json_data = json.dumps(data_payload).encode()
    encrypted_data = FERNET.encrypt(json_data).decode()
    
    return encrypted_data

def decrypt_and_validate_qr_data(encrypted_data):
    
    try:
        decrypted_bytes = FERNET.decrypt(encrypted_data.encode(), ttl=QR_CODE_LIFETIME_SECONDS)
        data = json.loads(decrypted_bytes.decode())
        
        current_time = int(time.time())
        if current_time > data.get('expiry', 0):
             return {'valid': False, 'reason': 'Expired QR Code (Time Check)'}

        return {'valid': True, 'data': data}

    except Exception as e:
        return {'valid': False, 'reason': f'Invalid or Expired QR Code Signature'}