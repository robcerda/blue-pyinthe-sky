import requests
from .auth import Auth
import json

class Identity:
    '''
    https://github.com/bluesky-social/atproto/tree/25c23b6b61eb8f1057fcedcbe7e93c183d3050a3/lexicons/com/atproto/identity     
    '''
    def __init__(self):
        self.url = Auth().url
        self.encrypted_credentials = Auth().encrypted_credentials
        self.decryption_key_path = Auth().decryption_key_path
        self.decryption_key = Auth().decryption_key
        self.access_jwt = Auth().access_jwt
        self.refresh_jwt = Auth().refresh_jwt

        self.credentials = Auth()._read_and_decrypt_credentials()
        self.refreshSession = Auth().refreshSession
 
    def resolveHandle(self, handle=None):
        request_url = f"{self.url}/com.atproto.identity.resolveHandle"
        if handle:
            request_url += f"?handle={handle}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        response = requests.get(method, request_url, headers=headers)
        if response.status_code == 401:  # Unauthorized
            print("Unauthorized. Refreshing tokens...")
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(method, request_url, headers=headers)
        else:
            print("Request successful.")
            json_response = response.json()
            return json_response

    def updateHandle(self, new_handle):
        """
        Update the handle of the account.
        Usage:
            api_handler = APIHandler()
            response = api_handler.updateHandle(new_handle='new_handle')
            print(response)
        Args:
            new_handle (str): The new handle to be set for the account.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.identity.updateHandle"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "handle": new_handle
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response

        