import os
from dropbox_api import upload_file

files = [file for file in os.listdir('./') if file.endswith('mp3')]

for file in files:
    print(file)
    with open(f'./{file}', 'rb') as data:
        upload_file(data.read(), 'Missed', file)
    print('Done uploading')
    os.remove(file)
