#참고: https://yongbeomkim.github.io/django/dj-scheduler/
# https://github.com/LuxunHuang/DjangoApscheduler101/blob/master/weather/views.py

import time
from app.webpush import episode_webpush
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore,\
    register_events, register_job

# thread 실행 인스턴스 생성하기
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


# 실행할 함수 Sample
class TT:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def update_a(self, Time):
        self.a = str(Time)


# 스케줄링의 적용함수 (interval)
@register_job(scheduler, "interval", seconds=10, replace_existing=True)
def test_job():
    print("task: " + str(time.time()))
    TT(1 ,2).update_a(int(time.time()))
    episode_webpush()


# 스케줄링의 적용함수 (cron)
# 0:00, 6:00, 12:00, 18:00 정시에 실행
@register_job(scheduler, "cron", hour='0,6,12,18', replace_existing=True)
def test_job_hourly():
    print("task: " + str(time.time()))
    TT(1 ,2).update_a(int(time.time()))

# 스케줄링 시작
def start_schedule():
    print("Starting")
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started!")
