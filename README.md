# CRM Task Runner Setup

## 1. Install Redis and Project Dependencies

1. Install Redis on your system  
   - **Ubuntu/Debian**  
     ```bash
     sudo apt update
     sudo apt install redis-server
     ```
   - **MacOS (Homebrew)**  
     ```bash
     brew install redis
     brew services start redis
     ```

2. Verify Redis is running  

```bash
redis-cli ping
```
- It should return `PONG`.

3. Install Python dependencies

```bash
pip install -r requirements.txt
```

## 2. Run Database Migrations

```bash
python manage.py migrate
```
- This creates the necessary database tables for the CRM application.

## 3. Start Celery Worker

- In a new terminal, start the Celery worker process:

```bash
celery -A crm worker -l info
```

- This worker will execute background tasks such as CRM report generation.

## 4. Start Celery Beat Scheduler

- In another terminal, start Celery Beat to schedule periodic tasks:

```bash
celery -A crm beat -l info
```

- Celery Beat will trigger scheduled jobs defined in the `CELERY_BEAT_SCHEDULE` setting.

## 5. Verify CRM Report Logs

- After the tasks run, check the log file at:

```plaintext
/tmp/crm_report_log.txt
```

- You should see entries confirming that scheduled CRM reports have been generated successfully.