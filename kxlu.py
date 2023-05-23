from datetime import datetime
from pytz import timezone
import ffmpeg
from threading import Thread
from dropbox_api import upload_file
import os
import json
from schedules import schedules

schedules = schedules


def record_playlist(show, duration):
    music_folder = "./music/"
    if not os.path.exists(music_folder):
        os.mkdir(music_folder)

    now = datetime.now(timezone('US/Pacific'))
    td = now.strftime("%m_%d_%Y")

    def download():
        file_name = f'{show}_{td}.mp3'
        file_path = music_folder+file_name
        (ffmpeg.input('https://kxlu.streamguys1.com/kxlu-hi',
                      t=duration).output(file_path).run())
        with open(file_path, 'rb') as f:
            file = f.read()
            upload_file(file, show, file_name)
        os.remove(file_path)
    t = Thread(target=download)
    t.start()


def create_json():
    json_obj = dict()
    with open('./schedules.json', 'w+') as f:
        json_obj['djs'] = [{k.name: str(k)} for k in schedules.schedules]
        json.dump(json_obj, f)


create_json()
