KanMind Backend
About the Project

KanMind is a task and project management application developed as part of the Developer Akademie Backend course.

This repository contains the Django REST Framework backend of the KanMind application. It provides the REST API for user authentication, boards, tasks, comments, and related functionality.

The corresponding frontend is available here:

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

The KanMind backend provides the following functionality:

Authentication
User registration
User login
Token-based authentication
Email address lookup
Boards
Create boards
List boards
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
Update comments
Delete comments
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

On Windows:

.venv\Scripts\activate

On macOS/Linux:

source .venv/bin/activate
4. Install the dependencies
pip install -r requirements.txt
5. Apply database migrations
python manage.py migrate
6. Start the development server
python manage.py runserver

The development server will normally be available at:

http://127.0.0.1:8000/
Running Tests

The project contains automated tests for the authentication, board, and task functionality.

To run the complete test suite:

python manage.py test

The current test suite contains more than 100 automated tests.

Test Coverage

The project uses Coverage.py to measure test coverage.

Run the tests with coverage:

coverage run manage.py test

Display the coverage report:

coverage report

The current project reaches 99% overall test coverage.

The project therefore exceeds the required minimum test coverage of 95%.

Code Quality

The project follows common Python and Django coding conventions.

The codebase is structured into separate Django applications:

auth_app – authentication and user functionality
board_app – board management
task_app – task and comment functionality
core – Django project configuration

The project also uses pycodestyle for Python code style checks.

API Structure

The API is organized into the following main areas:

/api/registration/
/api/login/
/api/email-check/

/api/boards/

/api/tasks/
/api/tasks/assigned-to-me/
/api/tasks/reviewing/

/api/tasks/<task_id>/
/api/tasks/<task_id>/comments/
/api/tasks/<task_id>/comments/<comment_id>/

Authentication is required for protected API endpoints.

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

.venv\Scripts\activate

Useful commands:

python manage.py check
python manage.py test
coverage run manage.py test
coverage report
python manage.py runserver
License

This project was developed as part of the Developer Akademie Backend course.