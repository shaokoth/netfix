# Netfix - Service Request Platform

A Django-based web application for connecting customers with service providers.

## Features

- User registration and authentication for both customers and companies
- Service creation and management for companies
- Service browsing and requesting for customers
- User profiles with service history
- Service categorization and filtering
- Most requested services tracking

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```## Starting the server
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
Activate the virtual environment
