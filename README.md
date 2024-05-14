
# Test Task Project

This project consists of a Django backend and a Vue frontend, both of which are containerized using Docker. Additionally, there is a service for running Django tests.

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

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

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Build and Start the Services

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

### 3. Access the Services

- Django backend: [http://localhost:8000](http://localhost:8000)
- Vue frontend: [http://localhost:8080](http://localhost:8080)

### 4. Running Tests

To run the Django tests, use the following command:

```bash
docker-compose --profile test run --rm django_test pytest -v
```

This will build and start the `django_test` service, which runs `pytest` for the Django application.

## Environment Variables

The following environment variables are used in the `docker-compose.yml` file:

- **Django Service**:
  - `SECRET_KEY`: Your Django secret key.
  - `DEBUG`: Set to `True` for development.
  - `DJANGO_SUPERUSER_USERNAME`: Username for the Django superuser.
  - `DJANGO_SUPERUSER_EMAIL`: Email for the Django superuser.
  - `DJANGO_SUPERUSER_PASSWORD`: Password for the Django superuser.

- **Vue Service**:
  - `NODE_ENV`: Set to `development` for development.

## Cleaning Up

To remove all Docker containers, networks, and images created by `docker-compose`, use the command:

```bash
docker-compose down --rmi all --volumes --remove-orphans
```

This command will:

- Remove all containers created by `docker-compose up`
- Remove all images built by `docker-compose`
- Remove all volumes created by `docker-compose`
- Remove any orphaned containers

## License

This project is licensed under the [MIT License](LICENSE).
