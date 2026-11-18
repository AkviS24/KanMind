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
- Django 6.1.3
- Django REST Framework 3.18.0
- Django REST Framework Token Authentication
- Gunicorn
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

For local development, configure the required variables:

    SECRET_KEY=your-local-development-secret
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    CORS_ALLOWED_ORIGINS=http://127.0.0.1:5500,http://localhost:5500

For production, copy `.env.example` to `.env` and replace the example secret with a newly generated key:

    python -c "import secrets; print(secrets.token_urlsafe(64))"

The `.env` file is included in `.gitignore` and must not be committed to the repository. Never use the example secret in a live deployment.

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

The public login and registration endpoints use scoped request limits (10 login attempts per minute and 5 registrations per hour per client IP). These limits apply independently to both the production and demo backend. DRF token authentication still uses the project's existing non-expiring tokens; token lifecycle changes are intentionally not introduced as part of this deployment preparation.

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

## Production Deployment (T-95)

The production setup uses Docker Compose, Gunicorn, and SQLite. The database and collected static files are stored in persistent directories on the Toshiba storage.

### 1. Prepare the environment

Copy `.env.example` to `.env` and generate a unique `SECRET_KEY`. Keep `DEBUG=False` and configure the production domains in `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`. Verify that HTTPS is already working before starting the service because the production configuration forces `SECURE_SSL_REDIRECT=True`.

The example paths point to:

- Database: `/srv/storage/webhosting/projects/KanMind/data`
- Static files: `/srv/storage/webhosting/projects/KanMind/staticfiles`
- Demo database: `/srv/storage/webhosting/projects/KanMind/demo-data`
- Demo static files: `/srv/storage/webhosting/projects/KanMind/demo-staticfiles`

Do not commit the production `.env` file.

### 2. Prepare persistent directories

Create the directories on the T-95:

    sudo mkdir -p /srv/storage/webhosting/projects/KanMind/data
    sudo mkdir -p /srv/storage/webhosting/projects/KanMind/staticfiles
    sudo mkdir -p /srv/storage/webhosting/projects/KanMind/demo-data
    sudo mkdir -p /srv/storage/webhosting/projects/KanMind/demo-staticfiles

If an existing SQLite database should be retained, back it up and copy it into the persistent `data` directory before the first container start. Do not overwrite an existing production database.

After copying the database, grant the container user (UID/GID 10001) access to both directories:

    sudo chown -R 10001:10001 /srv/storage/webhosting/projects/KanMind/data
    sudo chown -R 10001:10001 /srv/storage/webhosting/projects/KanMind/staticfiles
    sudo chown -R 10001:10001 /srv/storage/webhosting/projects/KanMind/demo-data
    sudo chown -R 10001:10001 /srv/storage/webhosting/projects/KanMind/demo-staticfiles

### 3. Build and start the backend

Run these commands from the backend repository directory:

    docker compose up --build -d
    docker compose logs -f kanmind-backend

The production container applies migrations and collects static files before starting Gunicorn. It listens only on `127.0.0.1:8002`. The separate demo container listens only on `127.0.0.1:8003` and uses its own database and static directory. On first start it creates the configured guest account and three sample tasks in the demo database. The guest account is never created in the production database.

Set `KANMIND_DEMO_SECRET_KEY` to a second generated secret. Set `KANMIND_GUEST_EMAIL` and `KANMIND_GUEST_PASSWORD` to exactly the existing public guest-login values in the frontend config. Keep these values in the server-side `.env` file; do not commit it.

The service uses `restart: "no"` and therefore does not start automatically after a server reboot. Start it when the KanMind demo is needed:

    docker compose start

Stop it when it is no longer needed:

    docker compose stop

The database and static files remain in the host directories when the container is stopped or removed.

### 4. Configure Nginx

Add the following locations inside the existing HTTPS `server` block. Do not replace the existing Portfolio configuration:

    location ^~ /kanmind-api/static/ {
        alias /srv/storage/webhosting/projects/KanMind/staticfiles/;
        access_log off;
        expires 1h;
    }

    location /kanmind-api/ {
        proxy_pass http://127.0.0.1:8002/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ^~ /kanmind-demo-api/static/ {
        alias /srv/storage/webhosting/projects/KanMind/demo-staticfiles/;
        access_log off;
        expires 1h;
    }

    location /kanmind-demo-api/ {
        proxy_pass http://127.0.0.1:8003/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

Nginx maps both public API prefixes to the same Django `/api/` routes, but to different backend containers and databases. Normal registration and login use `/kanmind-api/` and the production database. The guest login uses `/kanmind-demo-api/` and the isolated demo database. The demo database contains only the demo guest and its sample data; changes made by visitors cannot alter production users or data. The frontend stores the selected guest-session mode locally so subsequent board, task, and comment requests continue to use the demo backend until logout.

The `SECURE_SSL_REDIRECT` setting relies on Nginx forwarding the original protocol through `X-Forwarded-Proto`. HSTS remains disabled until HTTPS has been checked in production.

### 5. Run the production configuration check

After the environment and Nginx configuration are in place, run:

    docker compose run --rm --entrypoint python kanmind-backend manage.py check --deploy

Review all warnings before making the service publicly available. The HSTS warning is expected while `SECURE_HSTS_SECONDS=0`; enable HSTS only after HTTPS has been verified.

---

## License

This project was developed as part of the Developer Akademie Backend course.