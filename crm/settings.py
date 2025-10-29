INSTALLED_APPS = [
    'django_crontab',
]

# for django_crontab setup
CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]
