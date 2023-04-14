import requests
import json
from cryptography.fernet import Fernet
import base64

class Auth:
    def __init__(self):
        self.url = 'https://bsky.social/xrpc'
        self.encrypted_credentials = b''
        self.decryption_key_path = '.secrets/secret.key'
        self.decryption_key = self._read_decryption_key(self.decryption_key_path)
        self.access_jwt = None
        self.refresh_jwt = None
        self.credentials = self._read_and_decrypt_credentials()
        self.createSession()

    def _read_and_decrypt_credentials(self):
        cipher_suite = Fernet(self.decryption_key)
        decrypted_data = cipher_suite.decrypt(self.encrypted_credentials)
        decoded_data = base64.b64decode(decrypted_data).decode('utf-8')
        credentials = json.loads(decoded_data)
        return credentials

    def _read_decryption_key(self, decryption_key_path):
        with open(decryption_key_path, 'r') as f:
            decryption_key = f.read().strip()
        return decryption_key

    def createSession(self):
        auth_url = f"{self.url}/com.atproto.server.createSession"
        headers = {
            'Content-Type': 'application/json; charset=utf-16'
        }
        response = requests.post(auth_url, headers=headers, data=json.dumps(self.credentials, ensure_ascii=False).encode('utf-16'))
        response_data = response.json()
        self.access_jwt = response_data['accessJwt']
        self.refresh_jwt = response_data['refreshJwt']

    def refreshSession(self):
        refresh_tokens_url = f"{self.url}/com.atproto.server.refreshSession"
        headers = {
            'Content-Type': 'application/json; charset=utf-16'
        }
        refresh_data = {
            'refresh_token': self.refresh_jwt
        }
        response = requests.post(refresh_tokens_url, headers=headers, data=json.dumps(refresh_data, ensure_ascii=False).encode('utf-16'))
        response_data = response.json()
        if response.status_code == 200:
            self.access_jwt = response_data['accessJwt']
            self.refresh_jwt = response_data['refreshJwt']
        else:
            print(f"Failed to refresh tokens. Status code: {response.status_code}")
            print(f"Response text: {response.text}")
