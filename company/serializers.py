from django.utils.timezone import now
from rest_framework import serializers
from .models import Department, Employee, Dependent


class SimpleEmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, employee: Employee):
        return f"{employee.first_name} {employee.last_name}"

    class Meta:
        model = Employee
        fields = ["id", "full_name", "email"]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]


class DepartmentUpdateSerializer(serializers.ModelSerializer):
    def validate(self, data):
        manager = data.get("manager")
        if manager is not None:
            if manager.department != self.instance:
                raise serializers.ValidationError(
                    "Employee not allowed to be manager of a department that he does not work in."
                )
            if manager != self.instance.manager:
                self.instance.management_start_date = now().date()
        else:
            self.instance.management_start_date = None

        return data

    class Meta:
        model = Department
        fields = ["name", "manager"]


class DepartmentRetrieveSerializer(serializers.ModelSerializer):
    manager = SimpleEmployeeSerializer()

    class Meta:
        model = Department
        fields = ["id", "name", "manager", "management_start_date"]


class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name", "gender", "email", "department"]


class EmployeeRetrieveSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()
    dependents_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "first_name",
            "last_name",
            "gender",
            "birth_date",
            "email",
            "salary",
            "department",
            "dependents_count",
        ]


class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(
        slug_field="name", queryset=Department.objects.all(), read_only=False
    )

    class Meta:
        model = Employee
        fields = [
            "first_name",
            "last_name",
            "gender",
            "birth_date",
            "email",
            "salary",
            "department",
        ]


class DependentSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        employee_id = self.context["employee_id"]
        employee = Employee.objects.get(pk=employee_id)
        relationship = self.validated_data["relationship"]

        if employee.gender == "m":
            if relationship == "husband":
                raise serializers.ValidationError(
                    "How a man can be married from a man?"
                )
            elif (
                employee.dependents.filter(relationship="wife").count() == 4
                and relationship == "wife"
            ):
                raise serializers.ValidationError(
                    "A man cannot be married from more than 4 wives."
                )
        else:
            if relationship == "wife":
                raise serializers.ValidationError(
                    "How a woman can be married from a woman?"
                )
            elif (
                employee.dependents.filter(relationship="husband").count() == 1
                and relationship == "husband"
            ):
                raise serializers.ValidationError(
                    "How a woman can be married from more than one man?"
                )

        gender = "f" if relationship in ["wife", "daughter"] else "m"
        return Dependent.objects.create(
            employee_id=employee_id,
            gender=gender,
            **validated_data,
        )

    class Meta:
        model = Dependent
        fields = ["id", "name", "gender", "birth_date", "relationship"]
        read_only_fields = ["gender"]


class DependentUpdateSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        employee_id = self.context["employee_id"]
        relationship = self.validated_data["relationship"]
        employee = Employee.objects.get(pk=employee_id)

        if employee.gender == "m":
            if relationship == "husband":
                raise serializers.ValidationError(
                    "How a man can be married from a man?"
                )
            elif (
                employee.dependents.filter(relationship="wife").count() == 4
                and relationship == "wife"
            ):
                raise serializers.ValidationError(
                    "A man cannot be married from more than 4 wives."
                )
        else:
            if relationship == "wife":
                raise serializers.ValidationError(
                    "How a woman can be married from a woman?"
                )
            elif (
                employee.dependents.filter(relationship="husband").count() == 1
                and relationship == "husband"
            ):
                raise serializers.ValidationError(
                    "How a woman can be married from more than one man?"
                )

        gender = "f" if relationship in ["wife", "daughter"] else "m"
        instance.__dict__.update(**validated_data)
        instance.gender = gender
        instance.save()
        return instance

    class Meta:
        model = Dependent
        fields = ["name", "birth_date", "relationship"]
