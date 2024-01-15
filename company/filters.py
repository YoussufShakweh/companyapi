from django import forms
from django_filters.rest_framework import FilterSet, MultipleChoiceFilter
from rest_framework.filters import SearchFilter
from .models import Employee, Department


class EmployeeFilter(FilterSet):
    department = MultipleChoiceFilter(
        choices=[
            (department.pk, department.name) for department in Department.objects.all()
        ],
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Employee
        fields = ["gender", "department"]


class EmployeeSearchFilter(SearchFilter):
    search_description = "A search field depends on employee's full name"
