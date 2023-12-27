from django.db.models.aggregates import Count
from rest_framework.viewsets import ModelViewSet
from .models import Employee, Department, Dependent
from .serializers import (
    EmployeeSerializer,
    DepartmentSerializer,
    DependentSerializer,
    UpdateDependentSerializer,
)


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.annotate(dependents_count=Count("dependents")).all()
    serializer_class = EmployeeSerializer


class DependentViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateDependentSerializer
        else:
            return DependentSerializer

    def get_serializer_context(self):
        return {"employee_id": self.kwargs["employee_pk"]}

    def get_queryset(self):
        return Dependent.objects.filter(employee_id=self.kwargs["employee_pk"])
