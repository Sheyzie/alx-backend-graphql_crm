from django.core.management.base import BaseCommand, CommandError
from crm.models import Customer, Order
import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        deleted_customers = 0
        one_year_ago = datetime.date.today() - datetime.timedelta(days=365)
        path = "/tmp/customer_cleanup_log.txt"
        timestamp = datetime.date.today()

        customers = Customer.objects.all()

        if len(customers) == 0:
            with open(path, "a") as f:
                f.write(f"{timestamp} [DELETE]- {deleted_customers} inactive customer(s) deleted\n")

            return self.stdout.write(
                self.style.SUCCESS('You do not have any customer saved')
            )

        for customer in customers:
            orders = Order.objects.filter(id=customer.id)
            
            if len(orders) == 0 and customer.created_at.date() < one_year_ago:
                customer.delete()
                deleted_customers += 1

        with open(path, "a") as f:
            f.write(f"{timestamp} [DELETE]- {deleted_customers} inactive customer(s) deleted\n")

        return self.stdout.write(
            self.style.SUCCESS(f"{timestamp} [DELETE]- {deleted_customers} inactive customer(s) deleted")
        )

        
