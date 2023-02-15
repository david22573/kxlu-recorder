from kxlu import *
from time import sleep
from scheduler import Scheduler
import scheduler.trigger as trigger
import datetime as dt


schedule = Scheduler(tzinfo=dt.timezone.utc)
la_tz = dt.timezone(dt.timedelta(hours=-8))


def add_schedule(day, show, time, duration):
    if day == 0:
        schedule.weekly(trigger.Monday(dt.time(hour=time[0], minute=time[1], tzinfo=la_tz)),
                        record_playlist, kwargs={'show': show, 'duration': duration})
    if day == 1:
        schedule.weekly(trigger.Tuesday(dt.time(hour=time[0], minute=time[1], tzinfo=la_tz)),
                        record_playlist, kwargs={'show': show, 'duration': duration})
    if day == 2:
        schedule.weekly(trigger.Wednesday(dt.time(hour=time[0], minute=time[1], tzinfo=la_tz)),
                        record_playlist, kwargs={'show': show, 'duration': duration})
    if day == 3:
        schedule.weekly(trigger.Thursday(dt.time(hour=time[0], minute=time[1], tzinfo=la_tz)),
                        record_playlist, kwargs={'show': show, 'duration': duration})
    if day == 4:
        schedule.weekly(trigger.Friday(dt.time(hour=time[0], minute=time[1], tzinfo=la_tz)),
                        record_playlist, kwargs={'show': show, 'duration': duration})
    if day == 5:
        schedule.weekly(trigger.Saturday(dt.time(hour=time[0], minute=time[1], tzinfo=la_tz)),
                        record_playlist, kwargs={'show': show, 'duration': duration})
    if day == 6:
        schedule.weekly(trigger.Sunday(dt.time(hour=time[0], minute=time[1], tzinfo=la_tz)),
                        record_playlist, kwargs={'show': show, 'duration': duration})


# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)


def run_scheduler():
    for show in schedules:
        sched_day = schedules[show]['day']
        time = list(map(int, schedules[show]['time'].split(':')))
        duration = schedules[show]['t']
        add_schedule(sched_day, show, time, duration)
    while True:
        schedule.exec_jobs()
        sleep(1)


# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)
