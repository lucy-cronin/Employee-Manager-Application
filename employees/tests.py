from django.test import TestCase, Client
from django.urls import reverse
from .models import Employee
from .forms import EmployeeForm
import datetime

#model tests
class EmployeeModelTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            employee_number='E001',
            name='John Doe',
            address='123 Main St',
            salary=50000.00,
            start_date="2024-01-01",
            department='HR'
        )

    def test_employee_creation(self):
        employee = Employee.objects.get(employee_number='E001')
        self.assertEqual(employee.name, 'John Doe')
        self.assertEqual(employee.salary, 50000.00)
        self.assertEqual(employee.department, 'HR')

    def test_employee_str_(self):
        self.assertEqual(str(self.employee), 'John Doe')

    class EmployeeModelTests(TestCase):
        def setUp(self):
            self.employee = Employee.objects.create(
                employee_number='E001',
                name='John Doe',
                address='123 Main St',
                salary=50000.00,
                start_date='2024-01-01',
                department='HR'
            )

    def test_employee_creation(self):
        employee = Employee.objects.get(employee_number='E001')
        self.assertEqual(employee.name, 'John Doe')
        self.assertEqual(employee.salary, 50000.00)
        self.assertEqual(employee.department, 'HR')

    def test_employee_str(self):
        self.assertEqual(str(self.employee), 'John Doe')


#form tests
class EmployeeFormTest(TestCase):
    def test_employee_form_valid(self):
        form = EmployeeForm(data={
            'employee_number': 'E002',
            'name': 'Jane Smith',
            'address': '456 Elm St',
            'salary': 60000.00,
            'start_date': "2024-02-01",
            'department': 'Finance'
        })
        self.assertTrue(form.is_valid())

    def test_employee_form_invalid_data(self):
        form = EmployeeForm(data={
            'employee_number': '',
            'name': '',
            'address': '',
            'salary': '',
            'start_date': '',
            'department': ''
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)  # All fields are required

#integration tests
class EmployeeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee = Employee.objects.create(
            employee_number='E003',
            name='Alice Johnson',
            address='789 Oak St',
            salary=70000.00,
            start_date="2024-03-01",
            department='IT'
        )

    def test_employee_list_view(self):
        response = self.client.get(reverse('template_frontend'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/employee_list.html')
        self.assertContains(response, 'Alice Johnson')

    def test_employee_create_view(self):
        response = self.client.post(reverse('employee_create'), {
            'employee_number': 'E004',
            'name': 'Bob Brown',
            'address': '101 Pine St',
            'salary': 80000.00,
            'start_date': "2024-04-01",
            'department': 'Marketing'
        })
        self.assertEqual(response.status_code, 302)  # Created
        self.assertTrue(Employee.objects.filter(employee_number='E004').exists())

    def test_employee_update_view(self):
        response = self.client.post(reverse('employee_update', args=[self.employee.id]), {
            'employee_number': 'E003',
            'name': 'Alice Johnson Updated',
            'address': '789 Oak St',
            'salary': 75000.00,
            'start_date': "2024-03-01",
            'department': 'IT'
        })
        self.assertEqual(response.status_code, 302)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.name, 'Alice Johnson Updated')
        self.assertEqual(self.employee.address, '789 Oak St')

    def test_employee_delete_view(self):
        response = self.client.post(reverse('employee_delete', args=[self.employee.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after delete
        self.assertFalse(Employee.objects.filter(id=self.employee.id).exists())


#api integration tests

class EmployeeAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee = Employee.objects.create(
            employee_number='E005',
            name='Charlie Davis',
            address='202 Birch St',
            salary=90000.00,
            start_date="2024-05-01",
            department='Sales'
        )

    def test_api_get_employees(self):
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_api_create_employee(self):
        response = self.client.post('/api/employees/', {
            'employee_number': 'E006',
            'name': 'Diana Evans',
            'address': '303 Cedar St',
            'salary': 95000.00,
            'start_date': "2024-06-01",
            'department': 'Support'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(Employee.objects.count(), 2)
