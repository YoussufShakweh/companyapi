from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Employee, Dependent, Department
from .serializers import (
    EmployeeSerializer,
    EmployeeCreateUpdateSerializer,
    EmployeeRetrieveSerializer,
    DepartmentSerializer,
    DepartmentRetrieveSerializer,
    DepartmentUpdateSerializer,
    DependentSerializer,
    DependentUpdateSerializer,
)
from .filters import EmployeeFilter, EmployeeSearchFilter
from .pagination import EmployeePagination


class DepartmentViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Department.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return DepartmentUpdateSerializer
        elif self.request.method == "GET" and self.action != "list":
            return DepartmentRetrieveSerializer
        else:
            return DepartmentSerializer

    @swagger_auto_schema(operation_summary="Retrieve a list of departments.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Add a new department.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve details of an existing department.",
        responses={200: DepartmentRetrieveSerializer, 404: "Not found."},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update details of an existing department.",
        request_body=DepartmentUpdateSerializer,
        responses={200: DepartmentUpdateSerializer, 404: "Not found."},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete an existing department.",
        responses={204: "No content.", 404: "Not found.", 405: "Method not allowed."},
    )
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
    queryset = (
        Employee.objects.select_related("department")
        .annotate(dependents_count=Count("dependents"))
        .all()
    )
    filter_backends = [DjangoFilterBackend, EmployeeSearchFilter, OrderingFilter]
    filterset_class = EmployeeFilter
    search_fields = ["first_name", "last_name"]
    pagination_class = EmployeePagination
    ordering_fields = ["first_name", "last_name"]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT"]:
            return EmployeeCreateUpdateSerializer
        elif self.request.method == "GET" and self.action != "list":
            return EmployeeRetrieveSerializer
        else:
            return EmployeeSerializer

    @swagger_auto_schema(operation_summary="Retrieve a list of employees.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Add a new employee.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrive details of an existing employee.",
        responses={200: EmployeeRetrieveSerializer, 404: "Not found."},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update details of an existing employee.",
        request_body=EmployeeCreateUpdateSerializer,
        responses={200: EmployeeCreateUpdateSerializer, 404: "Not found."},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete an existing employee.",
        operation_description="Delete an existing employee and his associated dependents.",
        responses={204: "No content.", 404: "Not found."},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


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
        manual_parameters=[
            openapi.Parameter(
                name="employee_pk",
                in_=openapi.IN_PATH,
                description="A unique integer value identifying the employee that a dependent associated with.",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a list of dependents.",
        operation_description="Retrieve list of all dependents associated with an employee.",
        manual_parameters=[
            openapi.Parameter(
                name="employee_pk",
                in_=openapi.IN_PATH,
                description="A unique integer value identifying the employee that a dependent associated with.",
                required=True,
                type=openapi.TYPE_INTEGER,
            )
        ],
        responses={
            200: DependentSerializer(many=True),
            404: "Employee not found.",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve details of an existing dependent.",
        operation_description="Retrieve details of an existing dependent associated with an employee.",
        manual_parameters=[
            openapi.Parameter(
                name="employee_pk",
                in_=openapi.IN_PATH,
                description="A unique integer value identifying the employee that a dependent associated with.",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                description="A unique integer value identifying this dependent.",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: DependentSerializer,
            404: "Not found.",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update details of an existing dependents.",
        operation_description="Update details of an existing dependent associated with an employee.",
        manual_parameters=[
            openapi.Parameter(
                name="employee_pk",
                in_=openapi.IN_PATH,
                description="A unique integer value identifying the employee that a dependent associated with.",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                description="A unique integer value identifying this dependent.",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        request_body=DependentUpdateSerializer,
        responses={
            200: DependentUpdateSerializer,
            404: "Not found.",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete an existing dependent.",
        operation_description="Delete an existing dependent associated with an employee.",
        manual_parameters=[
            openapi.Parameter(
                name="employee_pk",
                in_=openapi.IN_PATH,
                description="A unique integer value identifying the employee that a dependent associated with.",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                description="A unique integer value identifying this dependent.",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            204: "No content.",
            404: "Not found.",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
