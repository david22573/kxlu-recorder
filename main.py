from jobs import run_scheduler
from kxlu import record_playlist

print("schedule running")
record_playlist('test_title', 60 * 5)

run_scheduler()
