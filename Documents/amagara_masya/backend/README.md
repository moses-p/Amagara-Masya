# Amagara Masya Backend

This is the backend API for the Amagara Masya rehabilitation center management system. It provides endpoints for managing children, staff, donors, and reports.

## Features

- User authentication and authorization using JWT
- Role-based access control
- Comprehensive child management
- Staff management and scheduling
- Donor management and donation tracking
- Report generation and access control
- File upload and management
- Audit logging

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Core
- `GET /api/core/users/` - List users
- `GET /api/core/groups/` - List groups
- `GET /api/core/locations/` - List locations
- `GET /api/core/documents/` - List documents
- `GET /api/core/audit-logs/` - List audit logs

### Children
- `GET /api/children/children/` - List children
- `GET /api/children/enrollments/` - List enrollments
- `GET /api/children/parent-guardians/` - List parent/guardians
- `GET /api/children/academic-records/` - List academic records
- `GET /api/children/medical-records/` - List medical records
- `GET /api/children/budget-records/` - List budget records
- `GET /api/children/location-history/` - List location history

### Staff
- `GET /api/staff/staff/` - List staff
- `GET /api/staff/roles/` - List staff roles
- `GET /api/staff/schedules/` - List staff schedules
- `GET /api/staff/attendance/` - List staff attendance
- `GET /api/staff/leaves/` - List staff leaves
- `GET /api/staff/trainings/` - List staff trainings
- `GET /api/staff/performance/` - List staff performance

### Donors
- `GET /api/donors/donors/` - List donors
- `GET /api/donors/donations/` - List donations
- `GET /api/donors/donation-types/` - List donation types
- `GET /api/donors/campaigns/` - List donation campaigns
- `GET /api/donors/communications/` - List donor communications

### Reports
- `GET /api/reports/reports/` - List reports
- `GET /api/reports/report-access/` - List report access
- `GET /api/reports/location-reports/` - List location reports
- `GET /api/reports/financial-reports/` - List financial reports
- `GET /api/reports/custom-reports/` - List custom reports
- `GET /api/reports/academic-reports/` - List academic reports

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
This project follows PEP 8 style guidelines. Use flake8 to check code style:
```bash
flake8
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 