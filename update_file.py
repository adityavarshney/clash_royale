from apscheduler.schedulers.blocking import BlockingScheduler
from file_handler import client, save_stats, delete_stats_file
from analyze import run_all
from apscheduler.executors.pool import ProcessPoolExecutor
from pytz import utc

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=1)
def _status():
	print("working...")

@sched.scheduled_job('interval', seconds=10)
def _save():
    if save_stats(client):
    	print("stats saved")
    else:
    	print("no new info")

# @sched.scheduled_job('interval', seconds=60)
def _delete():
	delete_stats_file()
	print('refreshing file')


# configuration options
executors = {
    'default': {'type': 'threadpool', 'max_workers': 5},
    'processpool': ProcessPoolExecutor(max_workers=5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

sched.configure(executors=executors, job_defaults=job_defaults, timezone=utc)
sched.start()