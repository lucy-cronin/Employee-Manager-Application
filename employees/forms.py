from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_number', 'name', 'address', 'salary', 'start_date', 'department']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }