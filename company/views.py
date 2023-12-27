from django.db.models.aggregates import Count
from rest_framework import status
from rest_framework.response import Response
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

    def destroy(self, request, *args, **kwargs):
        if Employee.objects.filter(department_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "It is not possible to delete a department where there are employees working within it."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.annotate(dependents_count=Count("dependents")).all()
    serializer_class = EmployeeSerializer


class DependentViewSet(ModelViewSet):
    http_method_names = ["get", "post", "PUT", "delete"]

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return UpdateDependentSerializer
        else:
            return DependentSerializer

    def get_serializer_context(self):
        return {"employee_id": self.kwargs["employee_pk"]}

    def get_queryset(self):
        return Dependent.objects.filter(employee_id=self.kwargs["employee_pk"])
