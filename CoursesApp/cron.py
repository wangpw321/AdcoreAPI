from django_cron import CronJobBase, Schedule
from django.core.management import call_command


class UpdateDataCronJob(CronJobBase):
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "your_app.update_data_cron_job"

    def do(self):
        call_command("update_data")
