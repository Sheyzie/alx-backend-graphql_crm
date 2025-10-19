from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100, null=False)
    price = models.DecimalField(max_digits=9, decimal_places=2, null=False)
    stock = models.PositiveIntegerField(default=0)


class Order(models.Model):
    customer_id = models.ForeignKey('customer', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    order_date = models.DateTimeField(auto_now=True)
