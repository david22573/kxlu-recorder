import dropbox
from dropbox import dropbox_client
from datetime import datetime
import json

app_key = 'w1xmfhioc29bz09'
app_secret = '0vju2twdrt8ao1v'


with open('token.json') as f:
    data = json.load(f)
    access_token = data['access_token']
    expires_at = datetime.strptime(data['expires_at'], '%Y-%m-%d %H:%M:%S.%f')
    refresh_token = data['refresh_token']
    data['app_key'] = app_key
    data['app_secret'] = app_secret


try:
    dropbox_api = dropbox.Dropbox(oauth2_access_token=access_token,
                                  oauth2_access_token_expiration=expires_at,
                                  oauth2_refresh_token=refresh_token,
                                  app_key=app_key,
                                  app_secret=app_secret)
except Exception as e:
    print(e)


def upload_file(file, show, file_name):
    try:
        dropbox_api.files_upload(bytes(file), path=f'/{show}/{file_name}')
    except dropbox.exceptions.AuthError:
        token_handler = dropbox_client._DropboxTransport(data)
        token_handler.check_and_refresh_access_token()
        if token_handler.token_content:
            print(token_handler.token_content)
            with open('token.json', 'w+') as tf:
                json.dumps(token_handler.token_content)
            print('token refreshed')
        dropbox_api.files_upload(bytes(file), path=f'/{show}/{file_name}')


# def create_token():
#     auth_flow3 = dropbox.DropboxOAuth2FlowNoRedirect(app_key,
#                                                      consumer_secret=app_secret,
#                                                      token_access_type='offline',
#                                                      scope=['files.content.read',
#                                                             'files.content.write'],
#                                                      include_granted_scopes='user')

#     authorize_url = auth_flow3.start()
#     print("1. Go to: " + authorize_url)
#     print("2. Click \"Allow\" (you might have to log in first).")
#     print("3. Copy the authorization code.")
#     auth_code = input("Enter the authorization code here: ").strip()

#     try:
#         oauth_result = auth_flow3.finish(auth_code)
#         with open('token.json', 'w+', encoding='UTF-8') as f:
#             data = dict()
#             data['access_token'] = oauth_result.access_token
#             data['expires_at'] = str(oauth_result.expires_at)
#             data['refresh_token'] = oauth_result.refresh_token
#             json.dump(data, f)

#     except Exception as e:
#         print('Error: %s' % (e,))
#         exit(1)
