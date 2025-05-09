# Amagara Masya Rehabilitation Center Database System

A comprehensive database system for managing street children rehabilitation and donor engagement.

## Project Overview

Amagara Masya is a rehabilitation center focused on caring for street children. This database system aims to improve transparency and donor engagement by providing detailed tracking of children's progress and financial management.

## Features

### Three-Tier Access System
1. **Admin Interface**
   - Full access to all system features
   - Sensitive information management
   - System configuration
   - Report generation

2. **Staff Interface**
   - Limited access to children's information
   - Daily operations management
   - Progress tracking
   - Basic reporting

3. **Donor Interface**
   - View sponsored children's progress
   - Track financial contributions
   - Access to non-sensitive information
   - Progress reports

### Core Functionality
- Complete child profile management
- Academic progress tracking
- Financial tracking and budgeting
- Location tracking
- Group management (starting from Group A, 2007)
- Report generation
- Donor engagement tools
- Parent/guardian information management

## Technical Stack

### Backend
- Django 4.2.7
- Django REST Framework
- PostgreSQL Database
- AWS S3 for media storage

### Frontend
- React.js
- Material-UI
- Redux for state management

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL
- AWS Account (for media storage)

### Installation
1. Clone the repository
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
4. Set up environment variables
5. Run migrations
6. Start the development servers

## Security Features
- Role-based access control
- Data encryption
- Secure authentication
- Audit logging
- Regular backups

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details. 