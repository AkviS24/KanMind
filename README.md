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

- Demo account login (public registration disabled)
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

The project contains automated tests covering authentication, boards, tasks, permissions, serializers, and models. The authentication tests also verify that public registration is unavailable and that the production/demo login restrictions are enforced.

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

The public demo login endpoint is limited to 10 attempts per minute per client IP. Public registration is disabled: the registration route is not included in the API URL configuration. The production backend has login disabled through `KANMIND_LOGIN_DISABLED=True`; the demo backend accepts only the configured guest account through `KANMIND_GUEST_ONLY_LOGIN=True`. Each backend instance keeps its own throttle cache. DRF token authentication continues to use the project's existing non-expiring tokens.

The API uses token-based authentication. The public demo login returns an authentication token for the configured guest account, which is then used to access protected endpoints. Public account registration is not available.

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

### 3. Build images without starting containers

Run these commands from the backend repository directory:

    docker compose --profile on-demand build kanmind-demo-backend
    docker compose config --quiet

Building the images does not start either service. The public demo backend is
`kanmind-demo-backend`; it must remain stopped until the Permission Handler
has verified the Portfolio session and the user's KanMind permission.

The production backend (`kanmind-backend`, port `127.0.0.1:8002`) is not part
of the public demo flow and has no public Nginx route. It uses the `private`
Compose profile and is not started by default. Do not start it as part of the
demo launch.

The demo backend listens only on `127.0.0.1:8003` and uses the `on-demand`
Compose profile. It uses its own database and static directory. On first start it applies migrations, creates the
configured guest account and three sample tasks, and collects static files.
The guest account is never created in the production database.

The demo service has a Docker health check. It reports healthy only after
Gunicorn responds and the demo database accepts a query. The health check uses
the private `/internal/health/` route, which is not part of the public API
proxy configuration.

Set `KANMIND_DEMO_SECRET_KEY` to a second generated secret. Set
`KANMIND_GUEST_EMAIL` and `KANMIND_GUEST_PASSWORD` to exactly the existing
public guest-login values in the frontend config. Keep these values in the
server-side `.env` file; do not commit it.

**Important:** Do not use generic `docker compose up -d` or
`docker compose start` for normal operation. Those commands start all
services in the Compose project and would bypass the intended on-demand
startup. The future restricted start service must address only the fixed
`kanmind-demo-backend` service. The container uses `restart: "no"`, so it
does not start automatically after a server reboot.

For isolated manual testing only (not as the live access mechanism), the demo
service can be started explicitly:

    docker compose --profile on-demand up -d kanmind-demo-backend
    docker compose --profile on-demand ps
    docker compose --profile on-demand logs -f kanmind-demo-backend

Stop that service after the manual test:

    docker compose --profile on-demand stop kanmind-demo-backend

The database and static files remain in the host directories when the
container is stopped or removed. Demo changes persist across container
restarts. Resetting the demo requires stopping only the demo service and
deliberately backing up or removing only its separate `demo-data` directory
before starting it again.

### 4. Configure Nginx

**Do not expose KanMind through Nginx yet.** The Permission Handler and its
proxy authorization are not deployed and tested. A plain reverse-proxy route
to `127.0.0.1:8003` would make the demo API directly callable and would
violate the required Portfolio-only entry flow.

Before enabling public access, the final Nginx configuration must:

- Protect the KanMind SPA entry `/kanmind/` with the Permission Handler.
- Protect the complete demo API prefix `/kanmind-demo-api/` with the same
  server-side authorization check.
- Apply authorization to static/API sublocations as required; no protected
  route may be reachable by bypassing the check.
- Keep the demo backend bound to `127.0.0.1:8003`.
- Never publish the production API prefix `/kanmind-api/`.
- Route only to fixed, preconfigured upstreams after a valid grant.

The exact `auth_request` location and Handler upstream must be added only
after the Permission Handler's internal deployment interface is finalized
and tested. Do not copy an unprotected `proxy_pass` example into the live
Nginx configuration.

### 5. Run the production configuration check

After the environment and Nginx configuration are in place, run:

    docker compose run --rm --entrypoint python kanmind-backend manage.py check --deploy

Review all warnings before making the service publicly available. The HSTS warning is expected while `SECURE_HSTS_SECONDS=0`; enable HSTS only after HTTPS has been verified.

---

## License

This project was developed as part of the Developer Akademie Backend course.