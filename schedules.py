class Schedules:
    def __init__(self):
        self.schedules = []

    def add(self, schedule):
        self.schedules.append(schedule)


class Schedule:
    def __init__(self, name, day, time, duration):
        self.name = name
        self.day = day
        self.time = list(map(int, time.split(':')))
        self.duration = duration

    def __repr__(self):
        return f'Schedule(name={self.name}, day={self.day}, time={self.time}, duration={self.duration})'


TEST3 = Schedule('test3', 1, '02:30', 3600)
GAIL = Schedule('gail', 0, '06:00', 10800)
ECLIPTIC = Schedule('ecliptic', 0, '09:00', 5400)
THE_MESSAGE = Schedule('the-message', 0, '18:00', 7600)
MELODY_FAIR = Schedule('melody-fair', 0, '20:00', 7320)
TWH = Schedule('twh', 3, '22:00', 7320)
REGGAE_SHOW = Schedule('reggae-show', 5, '20:00', 10800)
MYSTERY_MACHINE = Schedule('mystery-machine', 4, '21:00', 7320)
SERENATA_DE_TRIOS = Schedule('serenata-de-trios', 6, '18:00', 7320)

dj_sets = [TEST3, GAIL, ECLIPTIC, THE_MESSAGE, MELODY_FAIR,
           TWH, REGGAE_SHOW, MYSTERY_MACHINE, SERENATA_DE_TRIOS]

schedules = Schedules()

for dj_set in dj_sets:
    schedules.add(dj_set)
