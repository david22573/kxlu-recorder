from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


credentials = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('google_token.json'):
    credentials = Credentials.from_authorized_user_file(
        'google_token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        credentials = flow.run_local_server(host='localhost', port=8080)
    # Save the credentials for the next run
    with open('google_token.json', 'w') as token:
        token.write(credentials.to_json())

try:
    service = build('drive', 'v3', credentials=credentials)
except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f'An error occurred: {error}')


class DriveAPI:
    """A class for interacting with the Google Drive API.

    Args:
        credentials (Credentials): The credentials to use for authentication.
    """

    def __init__(self, credentials):
        self.credentials = credentials

    def list_files(self, page_size=10):
        """Lists the first `page_size` files that the user has access to.

        Args:
            page_size (int): The number of files to list.

        Returns:
            A list of dicts, each of which contains the following keys:
                * `id`: The ID of the file.
                * `name`: The name of the file.
        """
        service = build('drive', 'v3', credentials=self.credentials)
        results = service.files().list(
            pageSize=page_size, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        return items

    def print_files(self):
        """Prints the names and IDs of the first 10 files that the user has access to.
        """
        files = self.list_files()
        if not files:
            print('No files found.')
            return
        print('Files:')
        for file in files:
            print(u'{0} ({1})'.format(file['name'], file['id']))

    def upload_to_folder(self, file_path, name, description, folder_id):
        """Uploads a file to a specific folder in Google Drive.

        Args:
            file_path (str): The path to the file to upload.
            name (str): The name of the file to upload.
            description (str): The description of the file to upload.
            folder_id (str): The ID of the folder to upload the file to.

        Returns:
            The ID of the uploaded file.
        """
        file_metadata = {
            'name': name,
            'description': description,
            'folderId': folder_id
        }

        response = self.service.files().create(
            body=file_metadata,
            media_body=file_path,
            fields='id, name, description').execute()
        return response['id']


if __name__ == '__main__':
    # Create a DriveAPI object.
    drive_api = DriveAPI(credentials)

    # List the first 10 files.
    drive_api.print_files()
