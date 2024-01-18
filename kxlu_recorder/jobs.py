from kxlu import *
from time import sleep
from scheduler import Scheduler
import scheduler.trigger as trigger
import datetime as dt
import pytz


class DJSetScheduler:
    def __init__(self):
        self.la_tz = pytz.timezone('US/Pacific')
        self.schedule = Scheduler(tzinfo=self.la_tz)
        self.day_to_trigger = {
            0: trigger.Monday,
            1: trigger.Tuesday,
            2: trigger.Wednesday,
            3: trigger.Thursday,
            4: trigger.Friday,
            5: trigger.Saturday,
            6: trigger.Sunday,
        }

    def add_schedule(self, day, show, time, duration):
        day_trigger = self.day_to_trigger.get(day)
        if day_trigger:
            self.schedule.weekly(day_trigger(dt.time(hour=time[0], minute=time[1], tzinfo=self.la_tz)), record_playlist, kwargs={
                                 'show': show, 'duration': duration})

    def run_scheduler(self, dj_sets):
        for dj_set in dj_sets:
            show = dj_set.name
            sched_day = dj_set.day
            time = dj_set.time
            duration = dj_set.duration
            self.add_schedule(day=sched_day, show=show,
                              time=time, duration=duration)

        while True:
            self.schedule.exec_jobs()
            sleep(1)


# Example usage
if __name__ == "__main__":
    dj_set_scheduler = DJSetScheduler()
    dj_set_scheduler.run_scheduler(schedules.schedules)
