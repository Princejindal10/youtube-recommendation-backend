from google_auth_oauthlib.flow import InstalledAppFlow


def authenticate_user():
    # 'client_secret.json' is the file you downloaded from the Google Developer Console
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/youtube.force-ssl']

    )
    credentials = flow.run_local_server(port=0)  # Opens a browser for user login
    return credentials

if __name__ == "__main__":
    authenticate_user()

