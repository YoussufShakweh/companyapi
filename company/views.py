from django.db.models import F
from django.db.models.aggregates import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_yasg import openapi
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
        operation_summary="Retrieve a list of dependents.",
        operation_description="Retrieve list of all dependents associated with an employee.",
        responses={
            200: openapi.Response(
                description="List of dependents.",
                schema=openapi.Schema(
                    title="Dependent",
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(
                                title="ID",
                                type=openapi.TYPE_INTEGER,
                                read_only=True,
                            ),
                            "name": openapi.Schema(
                                title="Name",
                                type=openapi.TYPE_STRING,
                                max_length=150,
                                min_length=1,
                            ),
                            "gender": openapi.Schema(
                                title="Gender",
                                type=openapi.TYPE_STRING,
                                read_only=True,
                                enum=["m", "f"],
                                default="m",
                            ),
                            "birth_date": openapi.Schema(
                                title="Birth date",
                                type=openapi.TYPE_STRING,
                                format="date",
                            ),
                            "relationship": openapi.Schema(
                                title="Relationship",
                                type=openapi.TYPE_STRING,
                                enum=["husband", "wife", "son", "daugther"],
                            ),
                        },
                        required=["name", "birth_date", "relationship"],
                    ),
                ),
            ),
            404: "Employee not found.",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
