async function fetchEmployees() {
    const response = await fetch('/api/employees/');
const employees = await response.json();
const employeeList = document.getElementById('employee-list');
employeeList.innerHTML = ''; // Clear existing employees
employees.forEach(employee => {
const employeeCard = `
<div class="col-md-6 mb-3">
<div class="card">
<div class="card-body">
<h5 class="card-title">${employee.name}</h5>
<h6 class="card-subtitle mb-2 text-muted">${employee.employee_number}</h6>
<p class="card-text"><strong>Address:</strong> ${employee.address}</p>
<p class="card-text"><strong>Salary:</strong> €${employee.salary}</p>
<p class="card-text"><strong>Start Date:</strong> ${employee.startdate}</p>
<p class="card-text"><strong>Department:</strong> ${employee.department}</p>
<button class="btn btn-danger" onclick="openDeleteModal(${employee.id},
'${employee.name}')">Delete</button>
<button class="btn btn-warning" onclick="openEditModal(${employee.id})">Edit</button>
</div>
</div>
</div>
`;
employeeList.insertAdjacentHTML('beforeend', employeeCard);
});
}
// Add new employee
document.getElementById('employee-form').addEventListener('submit', async function(event) {
event.preventDefault();
const employeeData = {
employee_number: document.getElementById('employeeNumber').value,
name: document.getElementById('name').value,
address: document.getElementById('address').value,
salary: parseFloat(document.getElementById('salary').value),
startdate: document.getElementById('startdate').value,
department: document.getElementById('department').value,
};
const response = await fetch('/api/employees/', {method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify(employeeData)
});
if (response.ok) {
fetchEmployees(); // Refresh employee list
document.getElementById('employee-form').reset(); // Clear form
} else {
alert('Error adding employee.');
}
});
// Open Edit Modal and Populate Form
async function openEditModal(employeeId) {
const response = await fetch(`/api/employees/${employeeId}/`);
const employee = await response.json();
// Populate form fields with employee data
document.getElementById('editEmployeeId').value = employee.id;
document.getElementById('editEmployeeNumber').value = employee.employee_number;
document.getElementById('editName').value = employee.name;
document.getElementById('editAddress').value = employee.address;
document.getElementById('editSalary').value = employee.salary;
document.getElementById('editStartDate').value = employee.startdate;
document.getElementById('editDepartment').value = employee.department;
// Show the modal
const editModal = new bootstrap.Modal(document.getElementById('editEmployeeModal'));
editModal.show();
}
// Handle form submission for updating an employee
document.getElementById('editEmployeeForm').addEventListener('submit', async function(event) {
event.preventDefault();
const employeeId = document.getElementById('editEmployeeId').value;
const data = {
employee_number: document.getElementById('editEmployeeNumber').value,
name: document.getElementById('editName').value,address: document.getElementById('editAddress').value,
salary: parseFloat(document.getElementById('editSalary').value),
startdate: document.getElementById('editStartDate').value,
department: document.getElementById('editDepartment').value,
};
const response = await fetch(`/api/employees/${employeeId}/`, {
method: 'PUT',
headers: {
'Content-Type': 'application/json',
},
body: JSON.stringify(data),
});
if (response.ok) {
// Close the modal and refresh the employee list
const editModal = bootstrap.Modal.getInstance(document.getElementById('editEmployeeModal'));
editModal.hide();
fetchEmployees();
} else {
console.error('Failed to update employee');
}
});
let employeeToDelete = null; // Variable to store the employee ID to be deleted
// Function to open the delete confirmation modal
function openDeleteModal(employeeId, employeeName) {
employeeToDelete = employeeId; // Set the employee ID to delete
document.getElementById('deleteEmployeeName').textContent = employeeName; // Set employee name in the modal
// Show the delete confirmation modal
const deleteModal = new bootstrap.Modal(document.getElementById('deleteEmployeeModal'));
deleteModal.show();
}
// Function to confirm and delete the employee
async function confirmDeleteEmployee() {
if (!employeeToDelete) return;const response = await fetch(`/api/employees/${employeeToDelete}/`, {
method: 'DELETE',
});
if (response.ok) {
// Close the modal and refresh the employee list
const deleteModal = bootstrap.Modal.getInstance(document.getElementById('deleteEmployeeModal'));
deleteModal.hide();
fetchEmployees();
} else {
console.error('Failed to delete employee');
}
// Reset the employee ID to delete
employeeToDelete = null;
}
// Initialize the employee list on page load
document.addEventListener('DOMContentLoaded', fetchEmployees);