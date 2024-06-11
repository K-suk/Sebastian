from apscheduler.schedulers.background import BackgroundScheduler
from .views import assign_jobs

def start():
    """
    Automatic assign
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(assign_jobs, 'interval', days=3)  # schedule
    scheduler.start()