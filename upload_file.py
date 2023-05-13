import os
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

import subprocess


path = '/home/user/Downloads/'
files = os.listdir(path)

info = subprocess.check_output(
    "gcloud auth application-default print-access-token", shell=True)
info = info.decode("utf-8").strip()
info = json.loads('{"access_token":"' + info + '"}')
creds = Credentials.from_authorized_user_info(info=info)


try:
    service = build('drive', 'v3', credentials=creds)
except HttpError as error:
    print(f'An error occurred: {error}')


for file in files:
    if file.endswith('.mp3'):
        folder_metadata = {
            'name': 'kxlu_music',
            'mimeType': 'application/vnd.google-apps.folder'
        }

        try:
            # create folder
            folder = service.files().create(body=folder_metadata, fields='id').execute()
            folder_id = f'Folder ID: {folder.get("id")}'
        except HttpError as error:
            print(f"An error occurred: {error}")

        try:
            # create drive api client
            file_metadata = {'name': file, 'parents': [folder_id]}
            # media = MediaFileUpload(path+file, mimetype='audio/mpeg')
            media = None
            file = service.files().create(body=file_metadata,
                                          media_body=media, fields='id').execute()
            print(f'File ID: {file.get("id")}')
            os.remove(path+file)
        except HttpError as error:
            print(f'An error occurred: {error}')
            file = None
