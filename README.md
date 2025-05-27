# Python Flask Application with Layered Architecture

This project implements a Flask application with a layered architecture, SQLite database, and comprehensive CRUD operations.

## Environment Setup

### Windows

1. Install Python 3.8 or higher from [python.org](https://www.python.org/downloads/)

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Linux/MacOS

1. Install Python 3.8 or higher:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Fedora
sudo dnf install python3 python3-pip
```

2. Create a virtual environment:
```bash
python3 -m venv venv
```

3. Activate the virtual environment:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the development server:
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
app/
├── __init__.py
├── config.py
├── business/
│   ├── controllers/
│   └── models/
├── data/
│   └── database.py
└── presentation/
    └── routes/
```

## API Documentation

The API provides CRUD operations for the following entities:
- Users
- Profiles
- Addresses
- Digital Signatures
- Sessions
- Passwords
- Devices
- Security Questions
- Answers
- Roles
- Permissions

Each entity has standard REST endpoints:
- GET /api/{entity} - List all
- GET /api/{entity}/{id} - Get one
- POST /api/{entity} - Create
- PUT /api/{entity}/{id} - Update
- DELETE /api/{entity}/{id} - Delete
