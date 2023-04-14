import requests
from .auth import Auth
import json

class Moderation:
    '''
    https://github.com/bluesky-social/atproto/tree/main/lexicons/com/atproto/moderation
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
    
    def createReport(self, reason_type, subject, reason=None, method='POST', data=None):
        """
        Report a repo or a record.
        Usage:
            api_handler = APIHandler()
            response = api_handler.createReport(reason_type="Spam", subject="subject_identifier")
            print(response)
        Args:
            reason_type (str): The reason type for the report. Allowed values: "Spam", "Other".
            subject (str): The identifier of the subject (repo or record) being reported.
            reason (str, optional): The specific reason for the report. Defaults to None.
            method (str, optional): The HTTP method to use for the request. Defaults to 'POST'.
            data (dict, optional): The data to send in the request body. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        if reason_type not in ["Spam", "Other"]:
            raise ValueError("Invalid reason_type. Allowed values: 'Spam', 'Other'")
        request_url = f"{self.url}/com.atproto.moderation.createReport"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {"reasonType": reason_type, "subject": subject}
        if reason:
            json_data["reason"] = reason
        response = requests.request(method, request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.request(method, request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response
