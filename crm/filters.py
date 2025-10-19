import django_filters
from django.db.models import Q
from .models import Customer, Product, Order

class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    created_at_max = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    created_at_min = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    phone = django_filters.CharFilter(method='filter_phone')

    def filter_phone(self, queryset, phone, value='+1'):
        return queryset.filter(
             Q(phone__istartwith=value)
        )

    class Meta:
        model = Customer
        fields = ['name', 'email', 'created_at_max', 'created_at_min', 'phone']


class ProductFilter(django_filters.FilterSet):
    stock = django_filters.NumberFilter(method='filter_stock')

    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'price': ['gte', 'lte'],
        }

    def filter_stock(self, queryset, stock, value):
        return queryset.filter(
            Q(stock__lte=value) | Q(stock__gte=value)
        )

  
class OrderFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(method='filter_customer_name')

    class Meta:
        model = Order
        fields = {
            'total_amount': ['gte', 'lte'],
            'order_date': ['gte', 'lte'],
        }

    def filter_customer_name(self, queryset, customer_name, value):
        return queryset.filter(
            Q(customer_id__customer_name__icontains=value) | Q(customer_id__customer_name__istartwith=value)
        )
