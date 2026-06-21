# Workforce Management ERP

A Django-based enterprise resource planning system for manpower operations. It includes company and client management, employee records, project assignments, attendance, timesheets, invoicing, payroll, user accounts, and dashboard reporting.

## Features

- User Authentication
- Role-Based Access Control
- Company Management
- Client Management
- Employee Management
- Project/Site Management
- Timesheet Management
- Invoice Management
- Payroll Processing
- Dashboard Reporting
- PDF Reports

## Technology Stack

- Python 3.13
- Django 6.0.5
- SQLite3
- Bootstrap 5
- HTML
- CSS
- JavaScript
## Requirements

- Python 3.12 or newer
- pip
- Dependencies listed in `requirements.txt` (`Django==6.0.5`)

## Local setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the dependency:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Set the environment values shown in `.env.example`, or use the development defaults.

4. Prepare the database:

   ```powershell
   python manage.py migrate
   ```

5. Create the documented demo administrator:

   ```powershell
   $env:DJANGO_SUPERUSER_USERNAME="admin"
   $env:DJANGO_SUPERUSER_EMAIL="admin@example.com"
   $env:DJANGO_SUPERUSER_PASSWORD="Admin@12345"
   python manage.py createsuperuser --noinput
   ```

6. Start the application:

   ```powershell
   python manage.py runserver
   ```

Open `http://127.0.0.1:8000/` in a browser.

## Admin login credentials

- Application login: `http://127.0.0.1:8000/accounts/login/`
- Django administration: `http://127.0.0.1:8000/admin/`
- Username: `admin`
- Password: `Admin@12345`

These are demonstration credentials created during setup. Change the password before using the application outside a local assessment environment.

## Commands summary

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Privacy

Local databases, uploaded employee documents, photographs, and environment secrets are intentionally excluded from version control. Add test data after setting up a local database.
