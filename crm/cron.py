from django.utils import timezone


def log_crm_heartbeat():
    log = '{} CRM is alive \n'
    path = '/tmp/crm_heartbeat_log.txt'

    now = timezone.now()  # Timezone-aware datetime
    formatted_now = now.strftime("%d/%m/%Y-%H:%M:%S")


    with open(path, 'a') as f:
        f.write(log.format(formatted_now))