# Company Database API
This repository contains an API for the Company Database, built using the **Django framework** and **Django Rest Framework (DRF)**. The project is inspired by the concepts discussed in **Fundamentals of Database Systems** by **Ramez Elmasri**.

## Overview
The Company Database API allows users to interact with company-related data. It provides endpoints for querying, adding, updating, and deleting information related to:

1. Departments: Handle department information, including department names.
2. Employees: Manage employee records, including details such as first name, last name, email, salary, and department.
3. Dependents: Track dependents associated with employees (family members).

**Currently these entities implemented in the future I will implement the rest.**

## Feature
- Employee Information:
  - Retrieve employee details by ID.
  - Search for employees based on criteria (e.g., department, age).
  - Add new employees to the database.
  - Update employee records (e.g., salary, first_name, last_name).
- Department Management:
  - List all departments.
  - View department details.
  - Create new departments.
- Dependent Records:
  - Associate dependents with employees.
  - Retrieve dependent details for a specific employee.
  - Update dependent information.

## Installation
1. Clone this repository to your local machine:
	```
	git clone https://github.com/YoussufShakweh/companyapi.git
	cd companyapi
	```
2. Create a Virtual Environment and activate it:
	```
	virtualenv venv
	source venv/bin/activate
	```
3. Install the necessary dependencies (e.g., Python, Django, DRF) using this command:
	```python
	pip3 install -r requirements.txt
	```
4. Set up your database (e.g., PostgreSQL, MySQL) and configure Django accordingly.

## Usage
1. Run migrations to create the database schema:
	```python
	python manage.py migrate
	```
2. Start the development server:
	```python
	python manage.py runserver
	```
3. Access the API endpoints via **http://localhost:8000**

## API Docs
Will be available so soon.

## Contributing
Contributions are welcome! If you find any issues or want to enhance the API, feel free to submit a pull request.

## Credits
- **Ramez Elmasri**: Author of the book that inspired this project.
- **Youssuf Shakweh**: Creator of this API.

## License
This project is licensed under the **MIT license** - see the LICENSE file for details. 
