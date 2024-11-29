import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

def authenticate_user():
    # Get the client_secret from the environment variable
    client_secret_json = os.getenv('CLIENT_SECRET_JSON')

    if client_secret_json:
        # Parse the JSON string into a Python dictionary
        client_secret = json.loads(client_secret_json)
    else:
        raise Exception("CLIENT_SECRET_JSON environment variable not set")

    # Use the parsed client secret to initiate the OAuth flow
    flow = InstalledAppFlow.from_client_config(
        client_secret,
        scopes=['https://www.googleapis.com/auth/youtube.force-ssl']
    )
    credentials = flow.run_local_server(port=0)  # Opens a browser for user login
    return credentials

if __name__ == "__main__":
    authenticate_user()
