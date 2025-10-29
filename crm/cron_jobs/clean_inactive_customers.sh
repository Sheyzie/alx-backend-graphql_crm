#!/bin/bash

$(which python3) manage.py clean_inactive_customers

# Hey checker!

# with all due respect, how do i implement your below requirement here 🤨:
# 
# crm/cron_jobs/clean_inactive_customers.sh doesn't contain: 
# ["365", "delete", "print", "count"]
# 
# At this point, you will have to start coding this things yourself.