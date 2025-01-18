import django_filters
from .models import Todo

class TodoFilter(django_filters.FilterSet):
    completed=django_filters.BooleanFilter(field_name='completed',lookup_expr='exact',initial=True)
    created_at=django_filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model=Todo
        fields=['completed','created_at']