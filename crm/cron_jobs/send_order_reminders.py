from datetime import timedelta
from django.utils import timezone
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Calculate date 7 days ago in ISO 8601 format
seven_days_ago = (timezone.now() - timedelta(days=7)).isoformat()
timestamp = timezone.now()
path = "/tmp/order_reminders_log.txt"

# Define query (depends on your API schema!)
query = gql(
    """
    query getRecentOrders($afterDate: DateTime!) {
      orders(filter: { order_date_gte: $afterDate }) {
        customer
        product
        order_date
      }
    }
    """
)

# Setup transport
transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
client = Client(transport=transport, fetch_schema_from_transport=True)

# Execute
result = client.execute(query, variable_values={"afterDate": seven_days_ago})
print(result)

orders = result.orders

for order in orders:

    with open(path, "a") as f:
        f.write(f"{timestamp} [ORDER]- {order.id} by {order.customer.id}\n")

print("Order reminders processed!")

