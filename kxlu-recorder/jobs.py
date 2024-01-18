from kxlu import *
from time import sleep
from scheduler import Scheduler
import scheduler.trigger as trigger
import datetime as dt
import pytz

la_tz = pytz.timezone('US/Pacific')
print(la_tz)
schedule = Scheduler(tzinfo=la_tz)

# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)


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


def run_scheduler():
    for dj_set in schedules.schedules:
        show = dj_set.name
        sched_day = dj_set.day
        time = dj_set.time
        duration = dj_set.duration
        add_schedule(day=sched_day, show=show, time=time, duration=duration)
    while True:
        schedule.exec_jobs()
        sleep(1)


# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)
