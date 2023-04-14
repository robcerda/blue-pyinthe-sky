import requests
from .auth import Auth
import json

class Label:
    '''
    https://github.com/bluesky-social/atproto/tree/main/lexicons/com/atproto/label   
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
 
    def queryLabels(api_url, access_token, uri_patterns, sources=None, limit=50, cursor=None):
        """
        Queries labels relevant to the provided URI patterns.
        Usage:
            labels = queryLabels(api_url, access_token, uri_patterns=["at://foo*"], limit=10)
            print(labels)
        Args:
            api_url (str): The URL of the API server.
            access_token (str): The access token for authentication.
            uri_patterns (list of str): A list of AT URI patterns to match (boolean 'OR'). Each may be a prefix (ending with '*'; will match inclusive of the string leading to '*'), or a full URI.
            sources (list of str, optional): A list of label sources (DIDs) to filter on. Defaults to None.
            limit (int, optional): The maximum number of labels to return. Defaults to 50.
            cursor (str, optional): The cursor string for pagination. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{api_url}/com.atproto.label.queryLabels"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {access_token}"
        }
        json_data = {
            "uriPatterns": uri_patterns,
            "sources": sources,
            "limit": limit,
            "cursor": cursor
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            raise Exception("Unauthorized access token.")
        else:
            json_response = response.json()
            return json_response
        
    def subscribeLabels(self, cursor=None):
        """
        Subscribes to label updates.
        Usage:
            api_handler = APIHandler()
            response = api_handler.subscribeLabels(cursor=123)
            print(response)
        Args:
            cursor (int, optional): The last known event to backfill from.

        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.label.subscribeLabels"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {}
        if cursor is not None:
            json_data['cursor'] = cursor
        response = requests.get(request_url, headers=headers, json=json_data, stream=True)
        # If unauthorized, refresh session and retry request
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, json=json_data, stream=True)
        # Parse response stream line by line
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                return json_response
