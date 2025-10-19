import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import re
from datetime import datetime
from crm.filters import CustomerFilter, ProductFilter, OrderFilter
from .models import Customer, Product, Order


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node,)

    name = graphene.String()
    email = graphene.String()
    phone = graphene.String()


class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, name, email, phone):
        customer = Customer.objects.filter(email=email).exists()
        regex = re.compile(r'^\+?\d{10}$|^\d{3}-\d{3}-\d{4}$')
        if customer:
            success = False
            message = "Email already exists"
            return CreateCustomer(success=success, message=message)
        
        if not regex.match(phone):
            success = False
            message = "Invalid phone number pattern"
            return CreateCustomer(success=success, message=message)
        
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()

        success = True
        message = 'Customer created successfully'
        return CreateCustomer(customer=customer, success=success, message=message)



class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    success = graphene.Boolean()
    message = graphene.String()
    failed = graphene.List()

    def mutate(self, info, customers):
        failed = []
        successful_customers = []

        for customer in customers:
            is_customer = Customer.objects.filter(email=customer.email).exists()
            regex = re.compile(r'^\+?\d{10}$|^\d{3}-\d{3}-\d{4}$')
            if is_customer:
                success = False
                message = f"Email already exists: {customer.email}"
                failed.append({
                    "success": success,
                    "message": message
                })

                continue
                
            
            if not regex.match(customer.phone):
                success = False
                message = f"Invalid phone '{customer.phone}' number pattern"
                failed.append({
                    "success": success,
                    "message": message
                })
                
                continue
            
            new_customer = Customer(name=customer.name, email=customer.email, phone=customer.phone)
            new_customer.save()
            successful_customers.append(new_customer)

        success = True
        message = 'Customer created successfully'
        return BulkCreateCustomers(customers=successful_customers, success=success, message=message, failed=failed)


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node,)
    name = graphene.String()
    price = graphene.Decimal()
    stock = graphene.Int()  


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int(default_value=0) 

    product = graphene.Field(ProductType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, name, price, stock):
        if price < 0 or stock < 0:
            return CreateProduct(success=False, message="Price or Stock cannot be negative")
        
        product = Product(name=name, price=price, stock=stock)
        success = True
        message = 'Product created successfully'

        return CreateProduct(product=product, success=success, message=message)


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node,)
    customer = graphene.Field(CustomerType)
    product = graphene.List(ProductType)
    order_date = graphene.DateTime() 


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.Int(required=True)
        product_ids = graphene.List(graphene.Int, required=True)
        order_date = graphene.DateTime() 

    order = graphene.Field(OrderType)
    total_amount = graphene.Decimal()
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, customer_id, product_ids):
        customer = Customer.objects.filter(id=customer_id)
        total_amount = 0.0
        products = []
        
        if not customer:
            success = False
            message = f'No customer with the ID: {customer_id}'
            return CreateOrder(success=success, message=message)
        
        order = Order.objects.create(customer=customer)
        
        for product_id in product_ids:
            product = Product.objects.filter(id=product_id)
            
            if not product:
                success = False
                message = f'Invalid product ID: {product_id}'
                order.delete()
                return CreateOrder(success=success, message=message)
            
            total_amount += product.price
            products.append({
                "name": product.name,
                "price": product.price,
                "stock": product.stock
            })

            order.products.add(product)
            
            
        order.save()
        success = True
        message = 'Order created successfully'

        return CreateOrder(order=order, total_amount=total_amount, success=success, message=message)


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()


class Query(graphene.ObjectType):
    hello = graphene.String()
    customer = graphene.relay.Node.Field(CustomerType)
    all_customers = DjangoFilterConnectionField(CustomerType)

    product = graphene.relay.Node.Field(ProductType)
    all_products = DjangoFilterConnectionField(ProductType)

    order = graphene.relay.Node.Field(OrderType)
    all_orders = DjangoFilterConnectionField(OrderType)

    def resolve_name(self, info):
        return "Hello, GraphQL!"