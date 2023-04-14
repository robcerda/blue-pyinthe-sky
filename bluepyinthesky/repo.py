import requests
from .auth import Auth
import json

class Repo:
    '''
    https://github.com/bluesky-social/atproto/tree/main/lexicons/com/atproto/repo
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

    def applyWrites(self, repo, writes, validate=True, swapCommit=None):
        """
        Apply a batch transaction of creates, updates, and deletes.
        Usage:
            api_handler = APIHandler()
            response = api_handler.applyWrites(repo="my-repo", writes=[{...}])
            print(response)
        Args:
            repo (str): The handle or DID of the repo.
            writes (list): A list of create, update, or delete operations to apply.
            validate (bool): Validate the records? Default is True.
            swapCommit (str): The CID of a swap file commit to use. Optional.
        Returns:
            dict: The JSON response from the API.
        """
        request_url = f"{self.url}/com.atproto.repo.applyWrites"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "repo": repo,
            "validate": validate,
            "writes": writes,
            "swapCommit": swapCommit
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return json_response
        
    def create_record(self, repo, collection, record, rkey=None, validate=True, swap_commit=None):
        """
        Create a new record.

        Args:
            repo (str): The handle or DID of the repo.
            collection (str): The NSID of the record collection.
            record (unknown): The record to create.
            rkey (str): The key of the record.
            validate (bool): Validate the record?
            swap_commit (str): Compare and swap with the previous commit by cid.

        Returns:
            dict: The URI and CID of the newly created record.
        """
        request_url = f"{self.url}/com.atproto.repo.createRecord"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "repo": repo,
            "collection": collection,
            "record": record,
            "validate": validate
        }
        if rkey:
            json_data["rkey"] = rkey
        if swap_commit:
            json_data["swapCommit"] = swap_commit
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            return {"uri": json_response["uri"], "cid": json_response["cid"]}

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

    def putRecord(self, repo, collection, rkey, record, validate=True, swapRecord=None, swapCommit=None):
        """
        Write a record, creating or updating it as needed.

        Args:
            repo (str): The handle or DID of the repo.
            collection (str): The NSID of the record collection.
            rkey (str): The key of the record.
            record (dict): The record to write.
            validate (bool, optional): Validate the record? Defaults to True.
            swapRecord (str, optional): Compare and swap with the previous record by cid. Defaults to None.
            swapCommit (str, optional): Compare and swap with the previous commit by cid. Defaults to None.

        Returns:
            dict: The JSON response from the API containing uri and cid of the written record.

        Raises:
            InvalidSwap: If the swap commit or swap record is invalid.
        """
        request_url = f"{self.url}/com.atproto.repo.putRecord"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "repo": repo,
            "collection": collection,
            "rkey": rkey,
            "validate": validate,
            "record": record,
            "swapRecord": swapRecord,
            "swapCommit": swapCommit
        }
        response = requests.post(request_url, headers=headers, json=json_data)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data)
        else:
            json_response = response.json()
            if "error" in json_response:
                if json_response["error"]["name"] == "InvalidSwap":
                    raise InvalidSwap(json_response["error"]["message"])
            else:
                return json_response

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