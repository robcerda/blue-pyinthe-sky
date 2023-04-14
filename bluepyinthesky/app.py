import requests
from .auth import Auth
import json

class App:
    '''
    https://github.com/bluesky-social/atproto/tree/main/lexicons/app/bsky 
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