import requests
from .auth import Auth
import json

class Admin:
    '''
    https://github.com/bluesky-social/atproto/tree/main/lexicons/com/atproto/admin  
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

    def disableInviteCodes(self, codes=None, accounts=None):
        """
        Disable some set of invite codes and/or all codes associated with a set of users.
        Usage:
            api_handler = APIHandler()
            response = api_handler.disableInviteCodes(codes=["abc123", "def456"], accounts=["user1", "user2"])
            print(response)
        Args:
            codes (list, optional): List of invite codes to disable. Defaults to None.
            accounts (list, optional): List of user accounts whose codes should be disabled. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.admin.disableInviteCodes"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        data = {
            "codes": codes,
            "accounts": accounts
        }
        response = requests.post(request_url, headers=headers, json=data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=data)
        else:
            json_response = response.json()
            return json_response
        
    def getInviteCodes(self, sort='recent', limit=100, cursor=None):
        """
        Admin view of invite codes
        Usage:
            api_handler = APIHandler()
            response = api_handler.getInviteCodes(sort='usage', limit=50)
            print(response)
        Args:
            sort (str): Sort the codes by 'recent' or 'usage' (default 'recent').
            limit (int): The maximum number of codes to retrieve (default 100).
            cursor (str): A cursor to use for pagination (default None).
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.admin.getInviteCodes"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        params = {
            'sort': sort,
            'limit': limit,
            'cursor': cursor
        }
        response = requests.get(request_url, headers=headers, params=params)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, params=params)
        else:
            json_response = response.json()
            return json_response

    def getModerationAction(self, action_id):
        """
        Retrieves details about a specific moderation action.
        Usage:
            api_handler = APIHandler()
            response = api_handler.getModerationAction(action_id=123)
            print(response)
        Args:
            action_id (int): The ID of the moderation action to retrieve details for.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.admin.getModerationAction"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "id": action_id
        }
        response = requests.get(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response
    
    def getModerationActions(self, subject=None, limit=50, cursor=None):
        """
        Retrieves a list of moderation actions related to a subject.
        Usage:
            api_handler = APIHandler()
            response = api_handler.getModerationActions(subject="my_subject", limit=50)
            print(response)
        Args:
            subject (str, optional): The subject of the moderation actions. Defaults to None.
            limit (int, optional): The maximum number of items to retrieve. Defaults to 50.
            cursor (str, optional): The cursor to use for pagination. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.admin.getModerationActions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "subject": subject,
            "limit": limit,
            "cursor": cursor
        }
        response = requests.get(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response
        
    def getModerationReport(self, report_id):
        """
        Retrieves details about a moderation report.
        Usage:
            api_handler = APIHandler()
            response = api_handler.getModerationReport(report_id=123)
            print(response)
        Args:
            report_id (int): The ID of the moderation report to retrieve details about.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.admin.getModerationReport"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "id": report_id
        }
        response = requests.get(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response

    def getModerationReports(self, subject=None, resolved=None, limit=50, cursor=None):
        """
        List moderation reports related to a subject.
        Usage:
            api_handler = APIHandler()
            response = api_handler.getModerationReports(subject="example", resolved=False, limit=50)
            print(response)
        Args:
            subject (str, optional): The subject to retrieve reports for. Defaults to None.
            resolved (bool, optional): Whether to retrieve resolved or unresolved reports. Defaults to None.
            limit (int, optional): The maximum number of reports to retrieve. Defaults to 50.
            cursor (str, optional): The cursor to use for pagination. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.admin.getModerationReports"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "subject": subject,
            "resolved": resolved,
            "limit": limit,
            "cursor": cursor
        }
        response = requests.get(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response
        
    def getRecord(self, uri=None, cid=None):
        """
        View details about a record.
        Usage:
            api_handler = APIHandler()
            response = api_handler.getRecord(uri="at://example.record")
            print(response)
        Args:
            uri (str, optional): The URI of the record. Defaults to None.
            cid (str, optional): The CID of the record. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.admin.getRecord"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {}
        if uri is not None:
            json_data['uri'] = uri
        if cid is not None:
            json_data['cid'] = cid
        response = requests.get(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response
        
    def getRepo(self, did):
        """
        Retrieves details about a repository, given its DID.
        Args:
            did (str): The DID of the repository.
        Returns:
            dict: A JSON object with details about the repository.
        """
        request_url = f"{self.url}/com.atproto.admin.getRepo"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "did": did
        }
        response = requests.get(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response

    def resolveModerationReports(self, action_id, report_ids, created_by):
        """
        Resolve moderation reports by an action.
        Args:
            api_handler (APIHandler): An instance of the APIHandler class.
            action_id (int): The ID of the action to resolve the reports with.
            report_ids (list): A list of report IDs to resolve.
            created_by (str): The DID of the user resolving the reports.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.admin.resolveModerationReports"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "actionId": action_id,
            "reportIds": report_ids,
            "createdBy": created_by
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response
        
    def reverseModerationAction(self, action_id, reason, created_by):
        """
        Reverse a moderation action.
        Args:
            api_handler (APIHandler): An instance of the APIHandler class.
            action_id (int): The ID of the action to reverse.
            reason (str): The reason for reversing the action.
            created_by (str): The DID of the user reversing the action.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.admin.reverseModerationAction"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "id": action_id,
            "reason": reason,
            "createdBy": created_by
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response
        
    def searchRepos(self, term, limit=50, cursor=None):
        """
        Find repositories based on a search term.
        Args:
            term (str): The search term to use.
            limit (int, optional): The maximum number of items to retrieve. Defaults to 50.
            cursor (str, optional): The cursor to use for pagination. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.admin.searchRepos"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "term": term,
            "limit": limit,
            "cursor": cursor
        }
        response = requests.get(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response
        
    def takeModerationAction(self, action, subject, reason, created_by):
        """
        Take a moderation action on a repo.
        Args:
            action (str): The action to take.
            subject (dict): A dictionary containing information about the subject of the action.
            reason (str): The reason for the action.
            created_by (str): The DID of the user taking the action.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.admin.takeModerationAction"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "action": action,
            "subject": subject,
            "reason": reason,
            "createdBy": created_by
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response
        
    def updateAccountEmail(self, account, email):
        """
        Administrative action to update an account's email.
        Usage:
            api_handler = APIHandler()
            response = api_handler.updateAccountEmail(account="abc123", email="newemail@example.com")
            print(response)
        Args:
            account (str): The handle or DID of the account to update the email for.
            email (str): The new email address.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.admin.updateAccountEmail"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "account": account,
            "email": email
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response

    def updateAccountHandle(self, did, new_handle):
        """
        Administrative action to update an account's handle.
        Usage:
            api_handler = APIHandler()
            response = api_handler.updateAccountHandle(did='did:123', new_handle='new_handle')
            print(response)
        Args:
            did (str): The DID of the account to update.
            new_handle (str): The new handle to set for the account.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.admin.updateAccountHandle"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "did": did,
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
