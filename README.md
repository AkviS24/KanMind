# KanMind Backend

## About the Project

KanMind is a task and project management application developed as part of the Developer Akademie Backend course.

This repository contains the Django REST Framework backend of the KanMind application. It provides the REST API for user authentication, boards, tasks, comments, and related functionality.

The corresponding frontend is maintained in a separate repository.

**Frontend Repository:**  

https://github.com/Developer-Akademie-Backendkurs/project.KanMind

**Backend Repository:**  

https://github.com/AkviS24/KanMind

---

## Technologies

The backend is built with:

- Python 3
- Django 6.1
- Django REST Framework 3.18.0
- Django REST Framework Token Authentication
- SQLite
- Coverage.py
- pycodestyle

---

## Features

### Authentication

- User registration
- User login
- Token-based authentication
- Email address lookup

### Boards

- Create boards
- List accessible boards
- View board details
- Update board members
- Update board title
- Delete boards
- Add and remove board members
- Permission handling for board members and owners
- Board task statistics

### Tasks

- Create tasks
- Retrieve task details
- Update tasks
- Delete tasks
- Assign tasks to users
- Assign reviewers to tasks
- Filter tasks assigned to the current user
- Filter tasks currently being reviewed
- Validate assignee and reviewer board membership
- Task permissions based on board membership

### Comments

- Create comments for tasks
- Retrieve task comments
- Delete comments
- Automatically assign the authenticated user as comment author
- Permission handling for comment authors

---

## Requirements

Make sure the following software is installed:

- Python 3.x
- Git

The project dependencies are listed in `requirements.txt`.

---

## Environment Variables

Create a `.env` file in the root directory of the backend project, at the same level as `manage.py`.

Add the Django secret key to the `.env` file:

    SECRET_KEY=your-secret-key-here

The `.env` file is included in `.gitignore` and must not be committed to the repository.

---

## Installation

### 1. Clone the repository

    git clone https://github.com/AkviS24/KanMind.git
    cd KanMind

### 2. Create a virtual environment

    python -m venv .venv

### 3. Activate the virtual environment

**Windows:**

    .venv\Scripts\activate

**macOS/Linux:**

    source .venv/bin/activate

### 4. Install the dependencies

    pip install -r requirements.txt

### 5. Apply database migrations

    python manage.py migrate

This creates the required SQLite database and applies all Django migrations.

### 6. Start the development server

    python manage.py runserver

The development server will normally be available at:

    http://127.0.0.1:8000/

---

## Running Tests

The project contains automated tests covering authentication, boards, tasks, permissions, serializers, and models.

To run the complete test suite:

    python manage.py test

The current test suite contains **112 automated tests**.

Expected result:

    Found 112 test(s).

    ...

    Ran 112 tests

    OK

---

## Test Coverage

The project uses Coverage.py to measure test coverage.

Run the tests with coverage:

    coverage run manage.py test

Display the coverage report:

    coverage report

The project reaches approximately **99% overall test coverage**.

This exceeds the required minimum test coverage of **95%**.

---

## Code Quality

The project follows common Python, Django, and PEP 8 coding conventions.

The codebase is structured into separate Django applications:

- `auth_app` – authentication and user functionality
- `board_app` – board management
- `task_app` – task and comment functionality
- `core` – Django project configuration

The project also uses `pycodestyle` for Python code style checks.

Relevant classes and methods are documented using Python docstrings to describe their purpose and functionality.

---

## API Structure

The API is organized into the following main areas.

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/registration/` | Register a new user |
| POST | `/api/login/` | Authenticate a user |
| GET | `/api/email-check/` | Check whether an email address belongs to an existing user |

### Boards

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/boards/` | Retrieve boards accessible to the authenticated user |
| POST | `/api/boards/` | Create a new board |
| GET | `/api/boards/<board_id>/` | Retrieve a specific board |
| PATCH | `/api/boards/<board_id>/` | Update board information and members |
| DELETE | `/api/boards/<board_id>/` | Delete a board |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks/assigned-to-me/` | Retrieve tasks assigned to the authenticated user |
| GET | `/api/tasks/reviewing/` | Retrieve tasks assigned to the authenticated user as reviewer |
| POST | `/api/tasks/` | Create a new task |
| GET | `/api/tasks/<task_id>/` | Retrieve a specific task |
| PATCH | `/api/tasks/<task_id>/` | Update a task |
| DELETE | `/api/tasks/<task_id>/` | Delete a task |

### Comments

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks/<task_id>/comments/` | Retrieve comments belonging to a task |
| POST | `/api/tasks/<task_id>/comments/` | Create a new comment |
| DELETE | `/api/tasks/<task_id>/comments/<comment_id>/` | Delete a comment |

Authentication is required for protected API endpoints.

The API uses token-based authentication. After successful registration or login, the API returns an authentication token that can be used to access protected endpoints.

For the complete endpoint specification, refer to the KanMind API endpoint documentation provided by the Developer Akademie.

---

## Project Structure

    KanMind/

    │
    ├── auth_app/
    │   ├── api/
    │   │   ├── serializers.py
    │   │   ├── urls.py
    │   │   └── views.py
    │   ├── migrations/
    │   ├── tests/
    │   ├── admin.py
    │   └── models.py
    │
    ├── board_app/
    │   ├── api/
    │   │   ├── serializers.py
    │   │   ├── urls.py
    │   │   └── views.py
    │   ├── migrations/
    │   ├── tests/
    │   ├── admin.py
    │   └── models.py
    │
    ├── task_app/
    │   ├── api/
    │   │   ├── permissions.py
    │   │   ├── serializers.py
    │   │   ├── urls.py
    │   │   └── views.py
    │   ├── migrations/
    │   ├── tests/
    │   ├── admin.py
    │   └── models.py
    │
    ├── core/
    │   ├── settings.py
    │   └── urls.py
    │
    ├── manage.py
    ├── requirements.txt
    └── README.md

---

## Frontend

The KanMind frontend is maintained in a separate repository.

**KanMind Frontend:**  

https://github.com/Developer-Akademie-Backendkurs/project.KanMind

The frontend communicates with this Django REST API.

---

## Development

When working on the project, make sure the virtual environment is activated before running Django commands.

**Windows:**

    .venv\Scripts\activate

### Useful commands

Check the Django project:

    python manage.py check

Run the test suite:

    python manage.py test

Run tests with coverage:

    coverage run manage.py test

Display the coverage report:

    coverage report

Start the development server:

    python manage.py runserver

---

## License

This project was developed as part of the Developer Akademie Backend course.