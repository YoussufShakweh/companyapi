from django_filters.rest_framework import FilterSet
from rest_framework.filters import SearchFilter
from .models import Employee


class EmployeeFilter(FilterSet):
    class Meta:
        model = Employee
        fields = {
            "department__name": ["iexact"],
            "gender": ["exact"],
        }


class EmployeeSearchFilter(SearchFilter):
    search_description = "A search field depends on employee's full name"
