
# Test Task Project

This project consists of a Django backend and a Vue frontend, both of which are containerized using Docker. Additionally, there is a service for running Django tests.

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.10 or higher
- [Node.js](https://nodejs.org/) (version v20.3.1 or higher recommended for Vue 3)
- [npm](https://www.npmjs.com/) (comes with Node.js)

## Project Structure

```
.
├── TestTaskDjango
│   ├── DockerFile.django
│   ├── manage.py
│   ├── ...
│   └── initsuperuser.py
└── TestTaskVue
    ├── DockerFile.vuejs
    ├── ...
```

## Services

- **django**: Django backend service
- **vue**: Vue frontend service
- **django_test**: Service for running Django tests

## Setup and Run

### Using Docker

#### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```

#### 2. Build and Start the Services

To build and start the Django and Vue services, run the following command:

```bash
docker-compose up --build
```

This command will:

1. Build the Docker images for the Django and Vue services.
2. Start the Django service and perform the following actions:
   - Apply database migrations
   - Create a superuser using the `initsuperuser.py` script
   - Start the Django development server on `0.0.0.0:8000`
3. Start the Vue development server on `0.0.0.0:8080`

#### 3. Access the Services

- Django backend: [http://localhost:8000](http://localhost:8000)
- Vue frontend: [http://localhost:8080](http://localhost:8080)

### Without Docker

To setup and run the project without Docker:

#### 1. Set up a Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2. Install dependencies

```bash
cd TestTaskDjango
pip install -r requirements.txt
```

#### 3. Database Migrations and Superuser Creation

```bash
python manage.py migrate
python manage.py createsuperuser
```

#### 4. Run the Development Server

```bash
python manage.py runserver
```

#### 5. In a new terminal, setup and run the Vue project

```bash
cd ../TestTaskVue
npm install
npm run dev
```

### 4. Running Tests

To run the Django tests, use the following command:

```bash
docker-compose --profile test run --rm django_test
```

Or without Docker:

```bash
cd TestTaskDjango
python manage.py test
```

This will build and start the `django_test` service, which runs `pytest` for the Django application.

## Environment Variables

Configure the required environment variables for both Docker and non-Docker setups. Create a `.env` file in the root of the Django project and ensure it's listed in your `.gitignore` to secure sensitive information.

### Common Environment Variables for Django and Vue Services:
- `SECRET_KEY`: Your Django secret key, crucial for security.
- `DEBUG`: Set to `True` for development, `False` for production.
- `DJANGO_SUPERUSER_USERNAME`: Username for the Django superuser.
- `DJANGO_SUPERUSER_EMAIL`: Email for the Django superuser.
- `DJANGO_SUPERUSER_PASSWORD`: Secure password for the Django superuser.
- `NODE_ENV`: Set to `development` for the Vue service during development.

### Django-specific Environment Variables:
- `ALLOWED_HOSTS`: Host/domain names that this Django site can serve.
- `CORS_ALLOWED_ORIGINS`: Frontend hosts allowed for cross-origin requests.

### Redis and Celery Configuration for Django:
- `CELERY_BROKER_URL`: URL for the Celery message broker (Redis in this case).
- `CELERY_RESULT_BACKEND`: Backend to store Celery task results.

## Documentation

For detailed documentation on the project architecture and APIs, please refer to [Project Documentation](./docs/TestTaskDjango_Documentation.md).

## Cleaning Up

To remove all Docker containers, networks, and images created by `docker-compose`, use the command:

```bash
docker-compose down --rmi all --volumes --remove-orphans
```

Or clean up without Docker:

```bash
# Remove Python virtual environment
rm -rf venv
# Clean up node modules in Vue project
cd ../TestTaskVue
rm -rf node_modules
```

## License

This project is licensed under the [MIT License](LICENSE).
