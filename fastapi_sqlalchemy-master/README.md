# FastAPI CRUD App with SQLAlchemy and PostgreSQL

This project is a CRUD (Create, Read, Update, Delete) application built with **FastAPI** and **SQLAlchemy**. The application uses **PostgreSQL** as the database and is containerized using **Docker** for easy deployment.

## Features

- **FastAPI** for building the backend API.
- **SQLAlchemy** for database ORM.
- **PostgreSQL** as the database.
- **Docker Compose** for containerized deployment.
- **Pydantic** for data validation.
- Automatic database initialization on the first run.

---

## Project Structure

---

## Prerequisites

- **Docker** and **Docker Compose** installed on your system.
- Python 3.12+ installed (for local development).

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ml-backend-servicesDATABASE_PORT=5432
POSTGRES_PASSWORD=password123
POSTGRES_USER=postgres
POSTGRES_DB=notedb
POSTGRES_HOSTNAME=postgres
COMPOSE_PROJECT_NAME=fastapi-postgres-project
docker-compose up --build
pip install -r requirements.txt