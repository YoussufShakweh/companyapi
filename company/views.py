from django.db.models import F
from django.db.models.aggregates import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from .models import Employee, Department, Dependent
from .serializers import (
    EmployeeSerializer,
    EmployeeCreateUpdateSerializer,
    EmployeeRetrieveSerializer,
    DepartmentSerializer,
    DependentSerializer,
    DependentUpdateSerializer,
)


class DepartmentViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def destroy(self, request, *args, **kwargs):
        if Employee.objects.filter(department_id=kwargs["pk"]).exists():
            return Response(
                {
                    "error": "It is not possible to delete a department where there are employees working within it."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class EmployeeViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Employee.objects.annotate(
        department_name=F("department__name"), dependents_count=Count("dependents")
    ).all()

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT"]:
            return EmployeeCreateUpdateSerializer
        elif self.request.method == "GET" and self.action != "list":
            return EmployeeRetrieveSerializer
        else:
            return EmployeeSerializer


class DependentViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return DependentUpdateSerializer
        else:
            return DependentSerializer

    def get_serializer_context(self):
        return {"employee_id": self.kwargs["employee_pk"]}

    def get_queryset(self):
        return Dependent.objects.filter(employee_id=self.kwargs["employee_pk"])

    @swagger_auto_schema(
        operation_summary="Add a new dependent.",
        operation_description="Add a new dependent associated with an employee.",
        request_body=DependentSerializer,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a list of dependents.",
        operation_description="Retrieve list of all dependents associated with an employee.",
        responses={
            200: DependentSerializer,
            404: "Employee not found.",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve details of a dependent.",
        operation_description="Retrieve details of a dependent associated with an employee.",
        responses={
            200: DependentSerializer,
            404: "Not found.",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update details of a dependents.",
        operation_description="Update details of a dependent associated with an employee.",
        request_body=DependentUpdateSerializer,
        responses={
            200: DependentUpdateSerializer,
            404: "Not found.",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a dependent.",
        operation_description="Delete a dependent associated with an employee.",
        responses={
            204: "No content.",
            404: "Not found.",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
