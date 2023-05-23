from datetime import datetime
from pytz import timezone
import ffmpeg
from threading import Thread
from dropbox_api import upload_file
import os
from datetime import timedelta
import json

schedules = dict()

schedules['test3'] = {'day': 0, 'time': '12:30', 't': 3600}
schedules['gail'] = {'day': 0, 'time': '06:00', 't': 10800}
schedules['ecliptic'] = {'day': 0, 'time': '09:00', 't': 5400}
schedules['the-message'] = {'day': 0, 'time': '18:00', 't': 7600}
schedules['melody-fair'] = {'day': 0, 'time': '20:00', 't': 7320}
schedules['twh'] = {'day': 3, 'time': '22:00', 't': 7320}
schedules['reggae-show'] = {'day': 5, 'time': '19:00', 't': 10800}
schedules['mystery-machine'] = {'day': 4, 'time': '21:00', 't': 7320}
schedules['serenata-de-trios'] = {'day': 6, 'time': '18:00', 't': 7320}


def local_now():
    now = datetime.now(timezone('US/Pacific'))
    return now


def record_playlist(show, duration):
    music_folder = "./music/"
    if not os.path.exists(music_folder):
        os.mkdir(music_folder)

    td = local_now().strftime("%m_%d_%Y")

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
        json_obj['djs'] = [{k: schedules[k]} for k in schedules]

        json.dump(json_obj, f)


create_json()
