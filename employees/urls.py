from django.urls import path
from .views import EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView, employee_create, employee_delete, employee_list, employee_update   
from .views import employee_index 

urlpatterns = [
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroyView.as_view(), name='employee-retrieve-update-destroy'),
    path('javascript-frontend/', employee_index, name='javascript_frontend'),
    path('template-frontend/', employee_list, name='template_frontend'),
    path('template-frontend/create/', employee_create, name='employee_create'),
    path('template-frontend/update/<int:pk>/', employee_update, name='employee_update'),
    path('template-frontend/delete/<int:pk>/', employee_delete, name='employee_delete'),
]