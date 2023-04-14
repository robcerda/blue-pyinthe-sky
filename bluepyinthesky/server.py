import requests
from .auth import Auth
import json

class Server:
    '''
    https://github.com/bluesky-social/atproto/tree/main/lexicons/com/atproto/server
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

    def createAccount(self, handle, email, password, invite_code=None, recovery_key=None):
        """
        Create an account.
        Args:
            handle (str): The user's handle.
            email (str): The user's email address.
            password (str): The user's password.
            invite_code (str, optional): An invite code to use. Defaults to None.
            recovery_key (str, optional): The user's recovery key. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.server.createAccount"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        request_data = {
            'handle': handle,
            'email': email,
            'password': password
        }
        if invite_code:
            request_data['inviteCode'] = invite_code
        if recovery_key:
            request_data['recoveryKey'] = recovery_key
        response = requests.post(request_url, headers=headers, json=request_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=request_data)
        json_response = response.json()
        return json_response

    def createInviteCode(self, use_count, for_account=None):
        """
        Create an invite code.
        Args:
            use_count (int): The number of times the invite code can be used.
            for_account (str, optional): The DID of the account the invite code is being created for. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.server.createInviteCode"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        body = {
            "useCount": use_count
        }
        if for_account is not None:
            body["forAccount"] = for_account
        response = requests.post(request_url, headers=headers, json=body)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=body)
        json_response = response.json()
        return json_response

    def createInviteCodes(self, code_count=1, use_count=None, for_account=None):
        """
        Create one or more invite codes.
        Usage:
            api_handler = APIHandler()
            response = self.createInviteCodes(code_count=5, use_count=1, for_account="did:example:123")
            print(response)
        Args:
            code_count (int, optional): The number of invite codes to create. Defaults to 1.
            use_count (int, required): The number of times each invite code can be used.
            for_account (str, optional): The DID of the account that the invite codes are for. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        params = {
            'codeCount': code_count,
            'useCount': use_count
        }
        if for_account:
            params['forAccount'] = for_account
        response = requests.post(f"{self.url}/com.atproto.server.createInviteCodes", headers=headers, json=params)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(f"{self.url}/com.atproto.server.createInviteCodes", headers=headers, json=params)
        json_response = response.json()
        return json_response

    def deleteAccount(self, did, password, token):
        """
        Delete a user account with a token and password.
        Args:
            did (str): The user's decentralized identifier.
            password (str): The user's password.
            token (str): The deletion token.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.server.deleteAccount"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        data = {
            "did": did,
            "password": password,
            "token": token
        }
        response = requests.post(request_url, headers=headers, json=data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=data)
        else:
            json_response = response.json()
            return json_response

    def deleteSession(self):
        endpoint_url = f"{self.url}/com.atproto.server.deleteSession"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        response = requests.post(endpoint_url, headers=headers)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(endpoint_url, headers=headers)
        return response.json()
    
    def describeServer(self):
        """
        Get a document describing the service's accounts configuration.
        Usage:
            api_handler = APIHandler()
            response = api_handler.describeServer()
            print(response)

        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.server.describeServer"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        response = requests.get(request_url, headers=headers)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers)

        json_response = response.json()
        return json_response
    
    def getSession(self):
        """
        Get information about the current session.
        Usage:
            api_handler = APIHandler()
            response = api_handler.getSession()
            print(response)
        Args:
            None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.server.getSession"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        response = requests.get(request_url, headers=headers)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers)
        else:
            json_response = response.json()
            return json_response

    def requestAccountDelete(self):
        endpoint = f"{self.url}/com.atproto.server.requestAccountDelete"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        response = requests.post(endpoint, headers=headers)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(endpoint, headers=headers)
        json_response = response.json()
        return json_response
        
    def requestPasswordReset(self, email):
        """
        Initiate a user account password reset via email.
        Args:
            email (str): The email address associated with the account to reset.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.server.requestPasswordReset"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        data = {
            'email': email
        }
        response = requests.post(request_url, headers=headers, json=data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=data)
        else:
            json_response = response.json()
            return json_response
    
    def resetPassword(self, token, password):
        """
        Reset a user account password using a token.
        Usage:
            api_handler = APIHandler()
            response = api_handler.resetPassword(token, password)
            print(response)
        Args:
            token (str): The password reset token.
            password (str): The new password for the user account.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.server.resetPassword"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        data = {
            "token": token,
            "password": password
        }
        response = requests.post(request_url, headers=headers, json=data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=data)
        else:
            json_response = response.json()
            return json_response


    def getAccountInviteCodes(self, include_used=True, create_available=False, data=None):
        """
        Get all invite codes for a given account.
        Usage:
            api_handler = APIHandler()
            response = self.getAccountInviteCodes(include_used=True, create_available=True)
            print(response)
        Args:
            include_used (bool, optional): Include used invite codes. Defaults to True.
            create_available (bool, optional): Create available invite codes. Defaults to True.
            method (str, optional): The HTTP method to use for the request. Defaults to 'GET'.
            data (dict, optional): The data to send in the request body. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.server.getAccountInviteCodes?includeUsed={include_used}&createAvailable={create_available}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        response = requests.get(request_url, headers=headers, json=data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, json=data)
        else:
            json_response = response.json()
            return json_response