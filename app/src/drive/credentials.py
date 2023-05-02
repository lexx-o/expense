import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from config import directories


SCOPES = ['https://www.googleapis.com/auth/drive']


def _get_credentials(scope, auth_path):
    """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(auth_path/'token.json'):
        creds = Credentials.from_authorized_user_file(auth_path/'token.json', scope)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(auth_path/'credentials.json', scope)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(auth_path/'token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


credentials = _get_credentials(scope=SCOPES, auth_path=directories.config)
