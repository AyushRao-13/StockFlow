# StockFlow – Stock Management System

A Django-based stock management application designed to manage inventory purchases, item issuance, and available stock through a centralized dashboard.

## Features

- Inventory dashboard to monitor available stock.
- Record inventory purchases.
- Faculty-wise item issuance.
- Stock availability validation.
- Quantity tracking and database transaction management.
- Staff-only access control.
- Active/inactive management for items and faculty.
- Export purchase and issued-item histories to CSV.
- Django administration panel.

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, Django |
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| Database | SQLite |
| Development Environment | VS Code |

## Project Structure

```text
Stock-management-system-msi--main/
│
├── README.md
│
└── backend/
    ├── manage.py
    ├── requirements.txt
    ├── sms/
    │   ├── migrations/
    │   ├── static/
    │   ├── templates/
    │   ├── admin.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── urls.py
    │   └── views.py
    │
    └── stockflow/
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Stock-management-system-msi--main
```

### 2. Navigate to backend

```bash
cd backend
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```powershell
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Create an administrator account

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open the application:

http://127.0.0.1:8000/

Django administration:

http://127.0.0.1:8000/admin/

## Database

The project uses SQLite as its database.

Django manages database models and migrations through its ORM.

## Developer

**StockFlow – Stock Management System**

Developed as a Django-based inventory management project.