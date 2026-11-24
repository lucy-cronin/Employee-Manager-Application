from django.db import models

# Create your models here.

class Employee(models.Model):
    employee_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    department = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name