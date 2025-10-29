from django.utils import timezone
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from celery import shared_task
from datetime import datetime 

import requests


@shared_task
def generate_crm_report():
    log = '{} - Report: {} customers, {} orders, {} revenue \n'
    path = '/tmp/crm_report_log.txt'

    now = timezone.now()  # Timezone-aware datetime
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")


    # Define query (depends on your API schema!)
    query = gql(
        """
        query getReport {
            totalCustomers
            totalOrders
            totalRevenue
        }
        """
    )

    # Setup transport
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Execute
    result = client.execute(query)

    with open(path, 'a') as f:
        f.write(log.format(formatted_now, result['totalCustomers'], result['totalOrders'], result['totalRevenue']))

