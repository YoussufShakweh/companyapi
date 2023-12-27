from rest_framework_nested import routers
from . import views

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
urlpatterns = router.urls + employees_router.urls
