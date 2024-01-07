from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self) -> str:
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    GENDER_CHOICE_MALE = "m"
    GENDER_CHOICE_FEMALE = "f"
    GENDER_CHOICES = [
        (GENDER_CHOICE_MALE, "Male"),
        (GENDER_CHOICE_FEMALE, "Female"),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
    )
    email = models.EmailField(unique=True)
    birth_date = models.DateField()
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employees",
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Dependent(models.Model):
    name = models.CharField(max_length=150)
    GENDER_CHOICE_MALE = "m"
    GENDER_CHOICE_FEMALE = "f"
    GENDER_CHOICES = [
        (GENDER_CHOICE_MALE, "Male"),
        (GENDER_CHOICE_FEMALE, "Female"),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
    )
    birth_date = models.DateField()
    RELATIONSHIP_CHOICE_HUSBAND = "husband"
    RELATIONSHIP_CHOICE_WIFE = "wife"
    RELATIONSHIP_CHOICE_SON = "son"
    RELATIONSHIP_CHOICE_DAUGHTER = "daughter"
    RELATIONSHIP_CHOICE = [
        (RELATIONSHIP_CHOICE_HUSBAND, "Husband"),
        (RELATIONSHIP_CHOICE_WIFE, "Wife"),
        (RELATIONSHIP_CHOICE_SON, "Son"),
        (RELATIONSHIP_CHOICE_DAUGHTER, "Daughter"),
    ]
    relationship = models.CharField(max_length=8, choices=RELATIONSHIP_CHOICE)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="dependents",
        blank=True,
    )

    def __str__(self) -> str:
        return self.name
