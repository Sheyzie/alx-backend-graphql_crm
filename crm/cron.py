from django.utils import timezone
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    log = '{} CRM is alive \n'
    path = '/tmp/crm_heartbeat_log.txt'

    now = timezone.now()  # Timezone-aware datetime
    formatted_now = now.strftime("%d/%m/%Y-%H:%M:%S")


    with open(path, 'a') as f:
        f.write(log.format(formatted_now))

    # Define query (depends on your API schema!)
    query = gql(
        """
        query getHello {
            hello
        }
        """
    )

    # Setup transport
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Execute
    result = client.execute(query)
    print(result)

def update_low_stock():
    # Define query (depends on your API schema!)
    query = gql(
        """
        mutation updateStock {
            updateLowStockProducts {
                products
                success
                message
            }
        }
        """
    )

    # Setup transport
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True)

     # Execute
    result = client.execute(query)

    products = result["products"]

    path = '/tmp/low_stock_updates_log.txt'

    now = timezone.now()  # Timezone-aware datetime
    formatted_now = now.strftime("%d/%m/%Y-%H:%M:%S")

    log = '{} [UPDATE] - Updated {}\n'
    
    with open(path, 'a') as f:
        for product in products:
            f.write(log.format(formatted_now, product['name']))


