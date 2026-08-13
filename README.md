KanMind Backend
About the Project

KanMind is a task and project management application developed as part of the Developer Akademie Backend course.

This repository contains the Django REST Framework backend of the KanMind application. It provides the REST API for user authentication, boards, tasks, comments, and related functionality.

The corresponding frontend is maintained in a separate repository:

Frontend Repository:
https://github.com/Developer-Akademie-Backendkurs/project.KanMind

Backend Repository:
https://github.com/AkviS24/KanMind

Technologies

The backend is built with:

Python
Django 6.1
Django REST Framework 3.18.0
Django REST Framework Token Authentication
SQLite
Coverage.py
pycodestyle
Features
Authentication
User registration
User login
Token-based authentication
Email address lookup
Boards
Create boards
List accessible boards
View board details
Update boards
Delete boards
Add and manage board members
Permission handling for board members and owners
Tasks
Create and manage tasks
Assign tasks to users
Filter tasks assigned to the current user
Filter tasks currently being reviewed
Update task information
Delete tasks
Task permissions based on board membership
Comments
Create comments for tasks
Retrieve task comments
Delete comments
Permission handling for comment authors
Requirements

Make sure the following software is installed:

Python 3.x
Git

The project dependencies are listed in requirements.txt.

Installation
1. Clone the repository
git clone https://github.com/AkviS24/KanMind.git
cd KanMind
2. Create a virtual environment
python -m venv .venv
3. Activate the virtual environment

Windows:

.venv\Scripts\activate

macOS/Linux:

source .venv/bin/activate
4. Install the dependencies
pip install -r requirements.txt
5. Apply database migrations
python manage.py migrate

This creates the required SQLite database and applies all Django migrations.

6. Start the development server
python manage.py runserver

The development server will normally be available at:

http://127.0.0.1:8000/

Running Tests

The project contains automated tests covering authentication, boards, tasks, permissions, serializers, and models.

To run the complete test suite:

python manage.py test

The current test suite contains 112 automated tests.

Test Coverage

The project uses Coverage.py to measure test coverage.

Run the tests with coverage:

coverage run manage.py test

Display the coverage report:

coverage report

The current project reaches 99% overall test coverage.

This exceeds the required minimum test coverage of 95%.

Code Quality

The project follows common Python, Django, and PEP 8 coding conventions.

The codebase is structured into separate Django applications:

auth_app – authentication and user functionality
board_app – board management
task_app – task and comment functionality
core – Django project configuration

The project also uses pycodestyle for Python code style checks.

Relevant classes and methods are documented using Python docstrings to describe their purpose and functionality.

API Structure

The API is organized into the following main areas:

Authentication
/api/registration/
/api/login/
/api/email-check/
Boards
/api/boards/
/api/boards/<board_id>/
Tasks
/api/tasks/
/api/tasks/assigned-to-me/
/api/tasks/reviewing/
/api/tasks/<task_id>/
/api/tasks/<task_id>/comments/
/api/tasks/<task_id>/comments/<comment_id>/

Authentication is required for protected API endpoints.

The API uses token-based authentication. After successful registration or login, the API returns an authentication token that can be used to access protected endpoints.

For the complete endpoint specification, refer to the KanMind API endpoint documentation provided by the Developer Akademie.

Project Structure
KanMind/
│
├── auth_app/
│   ├── api/
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── migrations/
│   ├── tests/
│   └── models.py
│
├── board_app/
│   ├── api/
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── migrations/
│   ├── tests/
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
│   └── models.py
│
├── core/
│   ├── settings.py
│   └── urls.py
│
├── manage.py
├── requirements.txt
└── README.md
Frontend

The KanMind frontend is maintained in a separate repository.

KanMind Frontend:
https://github.com/Developer-Akademie-Backendkurs/project.KanMind

The frontend communicates with this Django REST API.

Development

When working on the project, make sure the virtual environment is activated before running Django commands:

Windows:

.venv\Scripts\activate

Useful commands:

python manage.py check
python manage.py test
coverage run manage.py test
coverage report
python manage.py runserver
License

This project was developed as part of the Developer Akademie Backend course.
