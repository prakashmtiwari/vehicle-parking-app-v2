from celery.schedules import crontab
import os 

def parse_cron_string(cron_str):
    """Parse cron string like '50 14 * * *' into crontab object"""
    parts = cron_str.split()
    return crontab(
        minute=parts[0],
        hour=parts[1],
        day_of_month=parts[2],
        month_of_year=parts[3],
        day_of_week=parts[4]
    )

# add task schedule to this dictionary

beat_schedule={
            # "daily-gchat-reminder": {
            #     "task": "vpa.beserver.tasks.reminder_tasks.send_gchat_daily_reminders_for_all_lots",
            #     "schedule": parse_cron_string(os.environ.get("REMINDER_CRON", "50 14 * * *")),  
            #     "args": (),
            # },
            # "daily-gmail-reminder": {
            #     "task": "vpa.beserver.tasks.reminder_tasks.send_gmail_daily_reminders_for_all_lots",
            #     "schedule": parse_cron_string(os.environ.get("REMINDER_CRON", "50 14 * * *")),  
            #     "args": (),
            # },
            # "daily-sms-reminder": {
            #     "task": "vpa.beserver.tasks.reminder_tasks.send_sms_daily_reminders_for_all_lots",
            #     "schedule": parse_cron_string(os.environ.get("REMINDER_CRON", "50 14 * * *")),  
            #     "args": (),
            # },
            "monthly-activity-report": {
            "task": "vpa.beserver.tasks.reports.send_monthly_activity_report",
            "schedule": parse_cron_string(os.environ.get("MONTHLY_REPORT_CRON", "0 1 1 * *")),
            "args": (), 
            }
        }