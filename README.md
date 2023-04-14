# blue-pyinthe-sky

This is a set of functions to help with the management of atprotocols, and bluesky. It's a work in progress, especially as things change within the [atproto repo](https://github.com/bluesky-social/atproto). 

My goal is to eventually package this up into a python library but for now, this will do. 

## Getting Started

Auth is handled by using your identifier / username and password and using those to create a session, however as to not store credentials in cleartext, we encrypt them using fernet. You'll find the steps below to get up and running:

### Step 1: Handling of Creds

In the [tools](./tools/) directory, you'll find a script called [crypto_helper.py](./tools/crypto_helper.py) that handles the creation of a key that will be used to encrypt and decrypt your credentials (so they're not in plaintext). It'll create a corresponding `.secrets` folder where it'll store a `secret.key`

Once its done, it'll output a string that looks like this `b'<randomjunk>'`, copy and paste the entire thing into [self.encrypted_credentials](https://github.com/robcerda/blue-pyinthe-sky/blob/f70e631ecf05421c7b64d1a6e5abb6f30f0a70a7/blue-pyinthe-sky/api_handler.py#L10)

### Step 2: Running of class functions

This was created as just a collection of functions, in the APIHandler class, with the intention of making this its own Python package. I haven't looked too hard into how to make that work with the way I handle creds, but thats my next to do.

You should be able to call that class and its corresponding functions, and if your credentials are correct, everything should just work.