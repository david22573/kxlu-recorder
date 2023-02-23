import json
from datetime import datetime
from pytz import timezone
import ffmpeg
from threading import Thread
from dropbox_api import upload_file
import os

schedules = dict()
schedules['melody-fair'] = {'day': 0, 'time': '21:00', 't': 7600}
schedules['twh'] = {'day': 3, 'time': '22:00', 't': 7600}
schedules['reggae-show'] = {'day': 5, 'time': '20:00', 't': 10800}
schedules['mystery-machine'] = {'day': 4, 'time': '21:00', 't': 7600}
schedules['serenata-de-trios'] = {'day': 6, 'time': '18:00', 't': 3600}
schedules['gail'] = {'day': 0, 'time': '06:00', 't': 10800}
schedules['ecliptic'] = {'day': 0, 'time': '09:00', 't': 5400}
schedules['mon-opera'] = {'day': 0, 'time': '18:00', 't': 7600}
schedules['test3'] = {'day': 0, 'time': '12:30', 't': 3600}


def local_now():
    return datetime.now(timezone('US/Pacific'))


def record_playlist(show, duration):
    td = local_now().strftime("%m_%d_%Y")

    def download():
        file_name = f'{show}_{td}.mp3'
        ffmpeg.input('https://kxlu.streamguys1.com/kxlu-hi',
                     t=duration).output(file_name).run()
        with open(file_name, 'rb') as f:
            file = f.read()
            upload_file(file, show, file_name)
        os.remove(file_name)
    t = Thread(target=download)
    t.start()


# save dictionary to json file
with open("./schedules.json", 'w+') as json_file:
    json.dump(schedules, json_file)
