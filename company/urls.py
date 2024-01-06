from django.urls import path
from rest_framework import permissions
from rest_framework_nested import routers
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="Company Database API Documentation",
        default_version="v1",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# ----------------------------------------------------------------------------- #
# Routers
# ----------------------------------------------------------------------------- #
router = routers.DefaultRouter()
router.register("employees", views.EmployeeViewSet, basename="employees")
router.register("departments", views.DepartmentViewSet, basename="departments")
# ----------------------------------------------------------------------------- #
# Nested_Routers
# ----------------------------------------------------------------------------- #
employees_router = routers.NestedDefaultRouter(router, "employees", lookup="employee")
employees_router.register(
    "dependents", views.DependentViewSet, basename="employee-dependents"
)
# ----------------------------------------------------------------------------- #
urlpatterns = (
    router.urls
    + employees_router.urls
    + [
        path(
            "docs/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger",
        ),
    ]
)
