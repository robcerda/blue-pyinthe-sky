import requests
import json
from cryptography.fernet import Fernet
import base64
from typing import Optional, Any, Dict

class APIHandler:
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
    
    # Admin - https://github.com/bluesky-social/atproto/tree/25c23b6b61eb8f1057fcedcbe7e93c183d3050a3/lexicons/com/atproto/moderation    
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

    # Identity - https://github.com/bluesky-social/atproto/tree/25c23b6b61eb8f1057fcedcbe7e93c183d3050a3/lexicons/com/atproto/identity    
    def resolveHandle(self, handle=None, method='GET'):
        request_url = f"{self.url}/com.atproto.identity.resolveHandle"
        if handle:
            request_url += f"?handle={handle}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        response = requests.request(method, request_url, headers=headers)
        if response.status_code == 401:  # Unauthorized
            print("Unauthorized. Refreshing tokens...")
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.request(method, request_url, headers=headers)
        else:
            print("Request successful.")
            json_response = response.json()
            return json_response

    def updateHandle(self, handle, data=None):
        """
        Updates the handle of the account.
        Usage:
            api_handler = APIHandler()
            response = api_handler.updateHandle(handle="new_handle")
            print(response)
        Args:
            handle (str): The new handle to set for the account.
            data (dict, optional): The data to send in the request body. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.identity.updateHandle"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {"handle": handle}
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response
        
    
    # Label - https://github.com/bluesky-social/atproto/tree/main/lexicons/com/atproto/label
    def queryLabels(self, uriPatterns, sources=None, limit=50, cursor=None):
        """
        Find labels relevant to the provided URI patterns.
        Args:
            uriPatterns (list): List of AT URI patterns to match (boolean 'OR'). 
                Each may be a prefix (ending with '*'; will match inclusive of the string leading to '*'), or a full URI
            sources (list): Optional list of label sources (DIDs) to filter on.
            limit (int): The maximum number of labels to return.
            cursor (str): An optional cursor to get the next set of results.
        Returns:
            A dictionary with a "labels" key containing the list of matching labels.
        """
        request_url = f"{self.url}/com.atproto.label.queryLabels"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "uriPatterns": uriPatterns,
            "sources": sources,
            "limit": limit,
            "cursor": cursor
        }
        response = requests.get(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, json=json_data)
        return response.text
        
    def subscribeLabels(self, cursor=None):
        """
        Subscribe to label updates
        Args:
            cursor (int): The last known event to backfill from.
        Returns:
            A streaming response of label updates.
        Raises:
            FutureCursor: If the provided cursor is in the future.
        """
        request_url = f"{self.url}/com.atproto.label.subscribeLabels"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {"cursor": cursor} if cursor is not None else {}
        response = requests.post(request_url, headers=headers, json=json_data, stream=True)

        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data, stream=True)

        if response.status_code == 403:  # FutureCursor
            raise Exception("FutureCursor: provided cursor is in the future")

        return response
    # Moderation - https://github.com/bluesky-social/atproto/tree/25c23b6b61eb8f1057fcedcbe7e93c183d3050a3/lexicons/com/atproto/moderation    
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

    # Repo - 

    def applyWrites(self, repo, writes, validate=True, swap_commit=None):
        """
        Apply a batch transaction of creates, updates, and deletes.

        Args:
        - repo (str): The handle or DID of the repo.
        - writes (List[Dict[str, Any]]): A list of write operations, which can be creates, updates, or deletes.
        - validate (bool): Whether or not to validate the records.
        - swap_commit (str): The CID of the commit to swap out.

        Raises:
        - InvalidSwap: If the swap commit is invalid.

        Returns:
        - None
        """
        pass
    
    def createRecord(self, repo: str, collection: str, rkey: str, record: Any, validate: bool = True, swap_commit: str = None) -> Dict[str, str]:
        """
        Create a new record.
        
        Args:
        - repo (str): The handle or DID of the repo.
        - collection (str): The NSID of the record collection.
        - rkey (str): The key of the record.
        - record (Any): The record to create.
        - validate (bool): Validate the record? Default is True.
        - swap_commit (str): Compare and swap with the previous commit by cid.
        
        Returns:
        - Dict[str, str]: A dictionary with keys "uri" and "cid".
        """
        # Implementation goes here
        pass

    def deleteRecord(self, repo, collection, rkey, swapRecord=None, swapCommit=None):
        """
        Delete a record, or ensure it doesn't exist.
        Args:
            repo (str): The handle or DID of the repo.
            collection (str): The NSID of the record collection.
            rkey (str): The key of the record.
            swapRecord (str): Compare and swap with the previous record by cid.
            swapCommit (str): Compare and swap with the previous commit by cid.
        Returns:
            The response content in bytes.
        """
        request_url = f"{self.url}/com.atproto.repo.deleteRecord"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "repo": repo,
            "collection": collection,
            "rkey": rkey,
            "swapRecord": swapRecord,
            "swapCommit": swapCommit
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        return response.content

    def describeRepo(self, repo):
        """
        Get information about the repo, including the list of collections.
        Args:
            repo (str): The handle or DID of the repo.
        Returns:
            The response content in bytes.
        """
        request_url = f"{self.url}/com.atproto.repo.describeRepo"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "repo": repo
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        return response.content

    def getRecord(self, did, collection, rkey, commit=None):
        """
        Get a record from the repo.
        Args:
            did (str): The handle or DID of the repo.
            collection (str): The namespace of the collection.
            rkey (str): The record key.
            commit (str): The CID of the version of the record. If not specified, return the most recent version.
        Returns:
            The response content in bytes.
        """
        request_url = f"{self.url}/com.atproto.repo.getRecord"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "repo": did,
            "collection": collection,
            "rkey": rkey,
            "cid": commit
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        return response.content

    def listRecords(self, did, collection, limit=50, rkeyStart=None, rkeyEnd=None, reverse=False):
        """
        List a range of records in a collection.
        Args:
            did (str): The DID of the repo.
            collection (str): The namespace of the collection.
            limit (int): The number of records to return. Default is 50.
            rkeyStart (str): The lowest sort-ordered rkey to start from (exclusive).
            rkeyEnd (str): The highest sort-ordered rkey to stop at (exclusive).
            reverse (bool): Reverse the order of the returned records? Default is False.
        Returns:
            The response content in bytes.
        """
        request_url = f"{self.url}/com.atproto.sync.listRecords"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "repo": did,
            "collection": collection,
            "limit": limit,
            "rkeyStart": rkeyStart,
            "rkeyEnd": rkeyEnd,
            "reverse": reverse
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        return response.content

    def putRecord(self, did, collection, rkey, record, validate=True, swapRecord=None, swapCommit=None):
        """
        Write a record, creating or updating it as needed.
        Args:
            did (str): The DID of the repo.
            collection (str): The namespace of the collection.
            rkey (str): The record key.
            record (dict): The record to write.
            validate (bool): Whether to validate the record (default True).
            swapRecord (str): Compare and swap with the previous record by CID.
            swapCommit (str): Compare and swap with the previous commit by CID.
        Returns:
            The response content in bytes.
        Raises:
            InvalidSwap: If the swapRecord or swapCommit is not valid.
        """
        request_url = f"{self.url}/com.atproto.repo.putRecord"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "repo": did,
            "collection": collection,
            "rkey": rkey,
            "record": record,
            "validate": validate,
            "swapRecord": swapRecord,
            "swapCommit": swapCommit
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 400:  # Bad request
            error = response.json().get('error')
            if error and error.get('name') == 'InvalidSwap':
                raise InvalidSwap(error.get('message'))
        response.raise_for_status()
        return response.content

    def uploadBlob(self, blob):
        """
        Upload a new blob to be added to repo in a later request.
        Args:
            blob (bytes): The blob data to upload.
        Returns:
            The response content as a dictionary.
        """
        request_url = f"{self.url}/com.atproto.repo.uploadBlob"
        headers = {
            'Authorization': f"Bearer {self.access_jwt}"
        }
        response = requests.post(request_url, headers=headers, data=blob)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, data=blob)
        return response.json()

    # Server - https://github.com/bluesky-social/atproto/tree/25c23b6b61eb8f1057fcedcbe7e93c183d3050a3/lexicons/com/atproto/server
    def createAccount(self, handle, email, password, inviteCode=None, recoveryKey=None):
        request_url = f"{self.url}/com.atproto.server.createAccount"
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'handle': handle,
            'email': email,
            'password': password
        }
        if inviteCode:
            data['inviteCode'] = inviteCode
        if recoveryKey:
            data['recoveryKey'] = recoveryKey
        
        response = requests.post(request_url, headers=headers, json=data)
        json_response = response.json()
        return json_response
    
    def createInviteCode(self, use_count, method='POST'):
        request_url = f"{self.url}/com.atproto.server.createInviteCode"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        data = {"useCount": use_count}
        response = requests.request(method, request_url, headers=headers, json=data)
        if response.status_code == 401:  # Unauthorized
            print("Unauthorized. Refreshing tokens...")
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.request(method, request_url, headers=headers, json=data)
        else:
            print("Request successful.")
            json_response = response.json()
            return json_response

        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")

    def createSession(self):
        auth_url = f"{self.url}/com.atproto.server.createSession"
        headers = {
            'Content-Type': 'application/json; charset=utf-16'
        }
        response = requests.post(auth_url, headers=headers, data=json.dumps(self.credentials, ensure_ascii=False).encode('utf-16'))
        response_data = response.json()
        self.access_jwt = response_data['accessJwt']
        self.refresh_jwt = response_data['refreshJwt']

    def deleteAccount(self, did, password, token):
        request_url = f"{self.url}/com.atproto.server.deleteAccount"
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'did': did,
            'password': password,
            'token': token
        }
        
        response = requests.delete(request_url, headers=headers, json=data)
        if response.status_code != 204:
            raise Exception(f"Error deleting account: {response.status_code}, {response.text}")
        return True

    def deleteSession(self):
        request_url = f"{self.url}/com.atproto.server.deleteSession"
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.delete(request_url, headers=headers)
        if response.status_code != 204:
            raise Exception(f"Error deleting session: {response.status_code}, {response.text}")
        return True
    
    def describeServer(self):
        request_url = f"{self.url}/com.atproto.server.describeServer"
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.get(request_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error getting server description: {response.status_code}, {response.text}")

        return response.json()
    
    def getSession(self):
        request_url = f"{self.url}/com.atproto.server.getSession"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }

        response = requests.get(request_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error getting session information: {response.status_code}, {response.text}")

        return response.json()

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

    def requestAccountDelete(self):
        request_url = f"{self.url}/com.atproto.server.requestAccountDelete"
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(request_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error initiating account deletion: {response.status_code}, {response.text}")
        
    def requestPasswordReset(self, email):
        request_url = f"{self.url}/com.atproto.server.requestPasswordReset"
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'email': email
        }

        response = requests.post(request_url, headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(f"Error initiating password reset: {response.status_code}, {response.text}")
    
    def resetPassword(self, token, password):
        request_url = f"{self.url}/com.atproto.server.resetPassword"
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'token': token,
            'password': password
        }

        response = requests.post(request_url, headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(f"Error resetting password: {response.status_code}, {response.text}")


    def getAccountInviteCodes(self, include_used=True, create_available=True, method='GET', data=None):
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

        response = requests.request(method, request_url, headers=headers, json=data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.request(method, request_url, headers=headers, json=data)
        else:
            json_response = response.json()
            return json_response
        
    # Sync - https://github.com/bluesky-social/atproto/tree/25c23b6b61eb8f1057fcedcbe7e93c183d3050a3/lexicons/com/atproto/sync
    def getBlob(self, repo_did, blob_cid):
        """
        Get a blob associated with a given repo.
        Args:
            repo_did (str): The DID of the repo.
            blob_cid (str): The CID of the blob to fetch.
        Returns:
            bytes: The contents of the blob.
        """
        request_url = f"{self.url}/com.atproto.sync.getBlob?did={repo_did}&cid={blob_cid}"
        headers = {'Authorization': f"Bearer {self.access_jwt}"}
        response = requests.get(request_url, headers=headers)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers)
        else:
            return response.content

    def getBlocks(self, did, cids):
        """
        Get blocks from a given repo.
        Args:
            did (str): The DID of the repo.
            cids (list): A list of CIDs to fetch.
        Returns:
            bytes: The binary data of the fetched blocks.
        """
        request_url = f"{self.url}/com.atproto.sync.getBlocks"
        headers = {
            'Authorization': f"Bearer {self.access_jwt}"
        }
        params = {
            "did": did,
            "cids": cids
        }
        response = requests.get(request_url, headers=headers, params=params)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, params=params)
        else:
            return response.content

    def getCheckout(self, did, commit=None):
        """
        Get the checkout of a repo at a specified commit.
        Args:
            api_handler (APIHandler): An instance of the APIHandler class.
            did (str): The DID of the repo.
            commit (str, optional): The commit to get the checkout from. Defaults to current HEAD.
        Returns:
            bytes: The CAR file containing the repo state at the specified commit.
        """
        request_url = f"{self.url}/com.atproto.sync.getCheckout"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "did": did
        }
        if commit:
            json_data['commit'] = commit
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            return response.content

    def getCommitPath(self, did, latest=None, earliest=None):
        """
        Gets the path of repo commits.
        Args:
            api_handler (APIHandler): An instance of the APIHandler class.
            did (str): The DID of the repo.
            latest (str, optional): The most recent commit. Defaults to None.
            earliest (str, optional): The earliest commit to start from. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.sync.getCommitPath"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "did": did
        }
        if latest:
            json_data["latest"] = latest
        if earliest:
            json_data["earliest"] = earliest
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response

    def getHead(self, did):
        """
        Gets the current HEAD CID of a repo.
        Args:
            did (str): The DID of the repo.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.sync.getHead"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "did": did
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response

    def getRecord(self, did, collection, rkey, commit=None):
        """
        Gets blocks needed for existence or non-existence of record.
        Args:
            did (str): The DID of the repo.
            collection (str): The namespace of the collection.
            rkey (str): The record key.
            commit (str): An optional past commit CID.
        Returns:
            The response content in bytes.
        """
        request_url = f"{self.url}/com.atproto.sync.getRecord"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "did": did,
            "collection": collection,
            "rkey": rkey,
            "commit": commit
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        return response.content

    def getRepo(self, did, earliest=None, latest=None):
        """
        Gets the repo state.
        Args:
            did (str): The DID of the repo.
            earliest (str, optional): The earliest commit in the commit range (not inclusive).
            latest (str, optional): The latest commit in the commit range (inclusive).
        Returns:
            dict: The response from the API.
        """
        request_url = f"{self.url}/com.atproto.sync.getRepo"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "did": did,
            "earliest": earliest,
            "latest": latest
        }
        response = requests.get(request_url, headers=headers, params=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, params=json_data)
        else:
            response_content = response.text()
            return response_content

    def listBlobs(self, did, latest, earliest):
        """
        List blob CIDs for some range of commits.
        Args:
            did (str): The DID of the repo.
            latest (str): The most recent commit.
            earliest (str): The earliest commit to start from.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.sync.listBlobs"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "did": did,
            "latest": latest,
            "earliest": earliest
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response

    def notifyOfUpdate(self, hostname):
        """
        Notify a crawling service of a recent update.
        Args:
            api_handler (APIHandler): An instance of the APIHandler class.
            hostname (str): The hostname of the service that is notifying of update.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.sync.notifyOfUpdate"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {"hostname": hostname}
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response
        
    def requestCrawl(self, hostname):
        """
        Request a service to persistently crawl hosted repos.
        Args:
            api_handler (APIHandler): An instance of the APIHandler class.
            hostname (str): The hostname of the service that is requesting to be crawled.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.sync.requestCrawl"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "hostname": hostname
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response
        
    def subscribeRepos(self, cursor: Optional[int] = None):
        """
        Subscribe to repo updates.

        Args:
            cursor (int, optional): The last known event to backfill from.

        Returns:
            None
        """
        pass

    # App Actor Bsky - https://github.com/bluesky-social/atproto/tree/25c23b6b61eb8f1057fcedcbe7e93c183d3050a3/lexicons/app/bsky/actor
    def getProfile(self, actor):
        request_url = f"{self.url}/app.bsky.actor.getProfile"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        params = {
            'actor': actor
        }
        response = requests.get(request_url, headers=headers, params=params)
        
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error getting profile: {response.status_code}, {response.text}")
        return response.json()
    
    def getProfiles(self, actors):
        request_url = f"{self.url}/app.bsky.actor.getProfiles"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        params = {
            'actors': actors
        }
        response = requests.get(request_url, headers=headers, params=params)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error getting profiles: {response.status_code}, {response.text}")
        return response.json()

    def getSuggestions(self, limit=100):
        request_url = f"{self.url}/app.bsky.actor.getSuggestions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        all_suggestions = []
        cursor = None
        while True:
            params = {'limit': limit}
            if cursor:
                params['cursor'] = cursor
            response = requests.get(request_url, headers=headers, params=params)
            if response.status_code == 401:  # Unauthorized
                self.refreshSession()
                headers['Authorization'] = f"Bearer {self.access_jwt}"
                response = requests.get(request_url, headers=headers, params=params)
            elif response.status_code != 200:
                raise Exception(f"Error getting suggestions: {response.status_code}, {response.text}")
            json_response = response.json()
            all_suggestions.extend(json_response['actors'])
            if 'cursor' in json_response:
                cursor = json_response['cursor']
            else:
                break

        return all_suggestions

    def searchActors(self, term, limit=50, cursor=None):
        request_url = f"{self.url}/app.bsky.actor.searchActors"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        params = {
            'term': term,
            'limit': limit
        }
        if cursor is not None:
            params['cursor'] = cursor

        response = requests.get(request_url, headers=headers, params=params)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, params=params)

        json_response = response.json()
        return json_response
    
    def searchActorsTypeahead(self, term, limit=50):
        request_url = f"{self.url}/app.bsky.actor.searchActorsTypeahead"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        params = {
            'term': term,
            'limit': limit
        }

        response = requests.get(request_url, headers=headers, params=params)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, params=params)
        
        json_response = response.json()
        return json_response
    
    # App Feed Bsky - https://github.com/bluesky-social/atproto/tree/25c23b6b61eb8f1057fcedcbe7e93c183d3050a3/lexicons/app/bsky/feed
    def getAuthorFeed(self, actor, limit=50, cursor=None):
        """
        Fetches an actor's feed.
        Usage:
            api_handler = APIHandler()
            response = api_handler.getAuthorFeed(actor="did:plc:sg22gxlwhuxtkwd5owhrqrhb")
            print(response)
        Args:
            actor (str): The actor whose feed to fetch.
            limit (int, optional): The maximum number of posts to return per request. Defaults to 50.
            cursor (str, optional): The cursor indicating the start of the next page of results. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/app.bsky.feed.getAuthorFeed"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        params = {
            'actor': actor,
            'limit': limit
        }
        if cursor:
            params['cursor'] = cursor
        response = requests.get(request_url, headers=headers, params=params)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, params=params)
        json_response = response.json()
        return json_response

    def getLikes(self, uri, cid=None, limit=50, cursor=None):
        """
        Retrieves a list of likes for a specified URI.
        Usage:
            api_handler = APIHandler()
            response = api_handler.getLikes(uri="at://example.com/uri")
            print(response)
        Args:
            uri (str): The URI for which to retrieve likes.
            cid (str, optional): The content ID for the URI.
            limit (int, optional): The maximum number of likes to retrieve. Defaults to 50.
            cursor (str, optional): A cursor to paginate through the results. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/app.bsky.feed.getLikes"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        params = {
            'uri': uri,
            'limit': limit
        }
        if cid:
            params['cid'] = cid
        if cursor:
            params['cursor'] = cursor

        response = requests.get(request_url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error getting likes: {response.status_code}, {response.text}")

        json_response = response.json()
        return json_response
    
    def getPostThread(self, uri, depth=None):
        """
        Retrieves the thread of a post given its URI.
        Usage:
            api_handler = APIHandler()
            response = api_handler.getPostThread(uri="at://my_post_uri")
            print(response)
        Args:
            uri (str): The URI of the post.
            depth (int, optional): The depth of the thread to retrieve. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/app.bsky.feed.getPostThread"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        params = {
            'uri': uri
        }
        if depth is not None:
            params['depth'] = depth
        response = requests.get(request_url, headers=headers, params=params)
        if response.status_code != 200:
            if response.status_code == 404:
                raise Exception(f"Post not found: {uri}")
            raise Exception(f"Error getting post thread: {response.status_code}, {response.text}")
        json_response = response.json()
        return json_response
    
    def getRepostedBy(self, uri, cid=None, limit=50, cursor=None):
        """
        Returns a list of users who have reposted a particular post.
        Args:
            uri (str): The URI of the post to retrieve reposters for.
            cid (str, optional): The CID of the post to retrieve reposters for. Defaults to None.
            limit (int, optional): The maximum number of reposters to return. Defaults to 50.
            cursor (str, optional): The cursor to use for pagination. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/app.bsky.feed.getRepostedBy"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        params = {"uri": uri, "limit": limit}
        if cid:
            params["cid"] = cid
        if cursor:
            params["cursor"] = cursor
        response = requests.get(request_url, headers=headers, params=params)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, params=params)
        json_response = response.json()
        return json_response
    
    def getTimeline(self, algorithm=None, limit=50, cursor=None):
        request_url = f"{self.url}/com.atproto.feed.getTimeline"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {"limit": limit}
        if algorithm:
            json_data["algorithm"] = algorithm
        if cursor:
            json_data["cursor"] = cursor
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        return response.json()
    
    # App Graph Bsky - https://github.com/bluesky-social/atproto/tree/25c23b6b61eb8f1057fcedcbe7e93c183d3050a3/lexicons/app/bsky/graph
    def follow(subject):
        """
        Creates a social follow.
        Usage:
            api_handler = APIHandler()
            response = api_handler.follow(subject="did:example:123")
            print(response)
        Args:
            subject (str): The DID of the subject to follow.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.graph.follow"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {"subject": subject}
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response

    def getFollowers(self, actor, limit=50, cursor=None):
        """
        Retrieves a list of followers for a given actor.
        Usage:
            api_handler = APIHandler()
            response = api_handler.getFollowers(actor="@myusername", limit=50)
            print(response)
        Args:
            actor (str): The identifier of the actor to retrieve followers for.
            limit (int, optional): The maximum number of followers to retrieve. Defaults to 50.
            cursor (str, optional): The cursor to use for pagination. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        if not actor:
            raise ValueError("The 'actor' parameter is required.")
        
        request_url = f"{self.url}/app.bsky.graph.getFollowers"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "actor": 'robcerda.com',
            "limit": limit,
            "cursor": cursor
        }
        response = requests.get(request_url, headers=headers, params=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, params=json_data)

        json_response = response.json()
        if "error" in json_response:
            raise ValueError(f"Error: {json_response['error']}. Message: {json_response['message']}")

        return json_response
        
    def getFollows(self, actor, limit=50, cursor=None):
        """
        Retrieves a list of accounts that an actor is following.
        Usage:
            api_handler = APIHandler()
            response = api_handler.getFollows(actor="@myusername", limit=50)
            print(response)
        Args:
            actor (str): The identifier of the actor to retrieve follows for.
            limit (int, optional): The maximum number of follows to retrieve. Defaults to 50.
            cursor (str, optional): The cursor to use for pagination. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/app.bsky.graph.getFollows"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "actor": actor,
            "limit": limit,
            "cursor": cursor
        }
        response = requests.get(request_url, headers=headers, params=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, params=json_data)
        else:
            json_response = response.json()
            return json_response

    def getMutes(self, limit=50, cursor=None):
        """
        Retrieves a list of actors that the viewer has muted.
        Usage:
            api_handler = APIHandler()
            response = api_handler.getMutes(limit=50)
            print(response)
        Args:
            limit (int, optional): The maximum number of mutes to retrieve. Defaults to 50.
            cursor (str, optional): The cursor to use for pagination. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/app.bsky.graph.getMutes"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "limit": limit,
            "cursor": cursor
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response

    def muteActor(self, actor):
        """
        Mutes an actor by DID or handle.
        Usage:
            api_handler = APIHandler()
            response = api_handler.muteActor(actor="@myusername")
            print(response)
        Args:
            actor (str): The identifier of the actor to mute.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/app.bsky.graph.muteActor"
        headers = {
            'Content-Type': 'application/json; charset=utf-16',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "actor": actor
        }
        response = requests.post(request_url, headers=headers, data=json.dumps(json_data, ensure_ascii=False).encode('utf-16'))
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, data=json.dumps(json_data, ensure_ascii=False).encode('utf-16'))
        if response.content:
            json_response = response.json()
            return json_response
        else:
            return {"message": "No response from the server"} 

        
    def unmuteActor(self, actor):
        request_url = f"{self.url}/app.bsky.graph.unmuteActor"
        headers = {
            'Content-Type': 'application/json; charset=utf-16',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "actor": actor
        }
        response = requests.post(request_url, headers=headers, data=json.dumps(json_data, ensure_ascii=False).encode('utf-16'))
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, data=json.dumps(json_data, ensure_ascii=False).encode('utf-16'))
        if response.content:
            json_response = response.json()
            return json_response
        else:
            return {"message": "No response from the server"} 

    # App Notifications Bsky - https://github.com/bluesky-social/atproto/tree/25c23b6b61eb8f1057fcedcbe7e93c183d3050a3/lexicons/app/bsky/notification    
    def getUnreadCount(self):
        """
        Retrieves the number of unread notifications for the current user.
        Usage:
            api_handler = APIHandler()
            response = api_handler.getUnreadCount()
            print(response)
        Returns:
            dict: The JSON response from the API containing the number of unread notifications.
        """
        request_url = f"{self.url}/app.bsky.notification.getUnreadCount"
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
        
    def listNotifications(self, limit=50, cursor=None):
        """
        Retrieves a list of notifications.
        Usage:
            api_handler = APIHandler()
            response = api_handler.listNotifications(limit=50)
            print(response)
        Args:
            limit (int, optional): The maximum number of notifications to retrieve. Defaults to 50.
            cursor (str, optional): The cursor to use for pagination. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/app.bsky.notification.listNotifications"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "limit": limit,
            "cursor": cursor
        }
        response = requests.get(request_url, headers=headers, params=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.get(request_url, headers=headers, params=json_data)
        else:
            json_response = response.json()
            return json_response

    def updateSeen(self, seen_at):
        """
        Notify the server that the user has seen notifications.
        Usage:
            api_handler = APIHandler()
            response = api_handler.updateSeen(seen_at='2022-04-09T12:34:56.789012Z')
            print(response)
        Args:
            seen_at (str): The timestamp in ISO-8601 format when the user has seen the notifications.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/app.bsky.notification.updateSeen"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "seenAt": seen_at
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        if response.content:
            json_response = response.json()
            return json_response
        else:
            return {"message": "No response from the server"} 

    # App Richtext Bsky - https://github.com/bluesky-social/atproto/tree/25c23b6b61eb8f1057fcedcbe7e93c183d3050a3/lexicons/app/bsky/richtext
    def getFacet(text):
        """
        Extracts the facet features from a given text.
        Usage:
            api_handler = APIHandler()
            text = "Check out this link https://example.com and mention @myfriend"
            response = api_handler.getFacet(text=text)
            print(response)
        Args:
            text (str): The text to extract facet features from.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/app.bsky.richtext.facet"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "text": text
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response

    # App Unspecced Bsky - https://github.com/bluesky-social/atproto/tree/25c23b6b61eb8f1057fcedcbe7e93c183d3050a3/lexicons/app/bsky/unspecced
    def getPopular(self, limit=50, cursor=None):
        """
        Retrieves a list of popular global items.
        Usage:
            api_handler = APIHandler()
            response = api_handler.getPopular(limit=50)
            print(response)
        Args:
            limit (int, optional): The maximum number of items to retrieve. Defaults to 50.
            cursor (str, optional): The cursor to use for pagination. Defaults to None.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/app.bsky.unspecced.getPopular?limit={limit}"
        if cursor:
            request_url += f"&cursor={cursor}"
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

#test = APIHandler().getProfile()

#print(APIHandler().createSession())
df = pd.DataFrame(APIHandler().getSuggestions(limit=100))
#print(APIHandler().getBlob(term='Dogs'))
print(df.head(10))