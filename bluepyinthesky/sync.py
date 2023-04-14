import requests
from .auth import Auth
import json

class Sync:
    '''
    https://github.com/bluesky-social/atproto/tree/main/lexicons/com/atproto/sync  
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
        
    def subscribeRepos(self, cursor):
        """
        Subscribe to repo updates.
        Args:
            cursor (int): The last known event to backfill from.
        Returns:
            str: The SSE stream of repo updates.
        """
        request_url = f"{self.url}/com.atproto.sync.subscribeRepos"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.access_jwt}"
        }
        json_data = {
            "cursor": cursor
        }
        response = requests.post(request_url, headers=headers, json=json_data, stream=True)
        if response.status_code == 401:  # Unauthorized
            self.refreshSession()
            headers['Authorization'] = f"Bearer {self.access_jwt}"
            response = requests.post(request_url, headers=headers, json=json_data, stream=True)
        else:
            return response.content