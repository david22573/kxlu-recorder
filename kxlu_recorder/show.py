import os
from datetime import datetime, timedelta

from scraper import get_djs

from . import PROJECT_ROOT

print(PROJECT_ROOT)


STREAM_URL = "https://kxlu.streamguys1.com/kxlu-lo"

show_times = get_djs()


def calculate_duration(start_time, end_time):
    fmt = '%H:%M'
    start_dt = datetime.strptime(start_time, fmt)
    end_dt = datetime.strptime(end_time, fmt)
    if end_dt < start_dt:
        end_dt += timedelta(days=1)
    duration_td = end_dt - start_dt
    hours, remainder = divmod(duration_td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    # Construct the ffmpeg duration string as "hh:mm:ss"
    duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return duration_str


def get_day_number(day: str):
    return {
        "SUN": 0,
        "MON": 1,
        "TUE": 2,
        "WED": 3,
        "THU": 4,
        "FRI": 5,
        "SAT": 6,
    }[day]


class Show:
    def __init__(self, name, day, start, duration):
        self.name = name
        self.start = start
        self.duration = duration
        self.day = get_day_number(day)

    def record_show(self):
        date_str = datetime.now().strftime("%Y%m%d")
        file_name = f"{self.name.lower().replace(' ', '_')}_{date_str}.mp4"
        os.system(f"""nohup ffmpeg -y -i {STREAM_URL} -t {
                  self.duration} -c copy '{file_name}' >/dev/null 2>&1 &""")

    def __repr__(self):
        return f"""
            <Show> ({self.name} - {self.day} - {self.start} - {self.duration})
        """


def get_shows():
    shows = []

    for show, times in show_times.items():
        for day, (start, end) in times.items():
            duration = calculate_duration(start, end)
            shows.append(Show(show, day, start, duration))

    return shows
