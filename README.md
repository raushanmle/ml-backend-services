# ML Backend Services

A comprehensive collection of machine learning and backend services demonstrating various technologies and architectures for building scalable ML applications.

## 📚 Table of Contents
- [Overview](#overview)
- [Services](#services)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This repository contains three main services that demonstrate different aspects of modern ML backend development:

1. **ML Prediction Service** - Flask-based machine learning model serving
2. **Celery Services** - Distributed task processing with database integration
3. **FastAPI SQLAlchemy** - Modern API framework with database ORM

Each service is designed to be educational and production-ready, showcasing best practices for building scalable ML backend systems.

## 🚀 Services

### 1. ML Prediction Service (`ml-prediction/`)

A Flask-based web application that serves a pre-trained machine learning model for salary prediction.

**Features:**
- 🤖 Pre-trained ML model (scikit-learn)
- 🌐 Web interface for predictions
- 📊 RESTful API endpoints
- 🚀 Heroku deployment ready (Procfile included)
- 📦 Pickle model serialization

**Tech Stack:**
- Flask
- NumPy, Pandas, Scikit-learn
- HTML Templates
- Gunicorn (WSGI server)

### 2. Celery Services (`celery-services/`)

A distributed task processing system with database integration, perfect for handling background jobs and long-running tasks.

**Features:**
- 🔄 Asynchronous task processing
- 🗄️ Database integration (SQL Server)
- 📊 Task monitoring and management
- 🐳 Docker containerization
- 📈 Scalable worker architecture

**Tech Stack:**
- Celery
- Redis (message broker & result backend)
- SQLAlchemy
- Docker & Docker Compose

### 3. FastAPI SQLAlchemy (`fastapi_sqlalchemy-master/`)

A modern, fast API framework with automatic documentation and database ORM integration.

**Features:**
- ⚡ High-performance async API
- 🗄️ PostgreSQL integration
- 📚 Automatic API documentation (Swagger/OpenAPI)
- 🔧 CRUD operations
- 🐳 Docker containerization
- ✅ Data validation with Pydantic

**Tech Stack:**
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Docker & Docker Compose

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ML Backend Services                      │
├─────────────────┬─────────────────┬─────────────────────────┤
│   ML Prediction │  Celery Tasks   │   FastAPI CRUD          │
│                 │                 │                         │
│  ┌───────────┐  │ ┌─────────────┐ │ ┌─────────────────────┐ │
│  │   Flask   │  │ │   Celery    │ │ │      FastAPI        │ │
│  │   App     │  │ │   Worker    │ │ │      Server         │ │
│  └───────────┘  │ └─────────────┘ │ └─────────────────────┘ │
│       │         │       │         │           │             │
│  ┌───────────┐  │ ┌─────────────┐ │ ┌─────────────────────┐ │
│  │ ML Model  │  │ │    Redis    │ │ │    PostgreSQL       │ │
│  │   (.pkl)  │  │ │   Broker    │ │ │     Database        │ │
│  └───────────┘  │ └─────────────┘ │ └─────────────────────┘ │
└─────────────────┴─────────────────┴─────────────────────────┘
```

## 📋 Prerequisites

Before running any of the services, ensure you have:

- **Python 3.8+** installed
- **Docker** and **Docker Compose** (for containerized services)
- **Redis** (for Celery services)
- **PostgreSQL** (for FastAPI service)
- **Git** for cloning the repository

## 🚀 Quick Start

### Clone the Repository
```bash
git clone https://github.com/raushanmle/ml-backend-services.git
cd ml-backend-services
```

### Option 1: Run Individual Services

#### ML Prediction Service
```bash
cd ml-prediction
pip install -r requirements.txt
python app.py
# Visit http://localhost:5000
```

#### Celery Services
```bash
cd celery-services
pip install -r requirements.txt
# Start Redis server first
redis-server
# In another terminal, start Celery worker
celery -A celery_app worker --loglevel=info
# In another terminal, run the Flask app
python app/app.py
```

#### FastAPI Service
```bash
cd fastapi_sqlalchemy-master
docker-compose up --build
# Visit http://localhost:8000/docs for API documentation
```

### Option 2: Docker Compose (Recommended)

Each service includes Docker configuration for easy deployment:

```bash
# For Celery Services
cd celery-services/deploy
docker-compose up --build

# For FastAPI Service
cd fastapi_sqlalchemy-master
docker-compose up --build
```

## 🔧 Detailed Setup

### ML Prediction Service Setup

1. **Install Dependencies**
   ```bash
   cd ml-prediction
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Test the API**
   ```bash
   curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "feature1=value1&feature2=value2"
   ```

### Celery Services Setup

1. **Install Dependencies**
   ```bash
   cd celery-services
   pip install -r requirements.txt
   ```

2. **Start Redis (Message Broker)**
   ```bash
   redis-server
   ```

3. **Configure Database** (Optional)
   - Update database connection in `celery_config.py`
   - Run database tests: `python test_db_connection.py`

4. **Start Celery Worker**
   ```bash
   celery -A celery_app worker --loglevel=info
   ```

5. **Send Tasks**
   ```bash
   python send_task.py
   ```

### FastAPI Service Setup

1. **Using Docker (Recommended)**
   ```bash
   cd fastapi_sqlalchemy-master
   docker-compose up --build
   ```

2. **Manual Setup**
   ```bash
   pip install -r requirements.txt
   # Configure PostgreSQL connection in app/config.py
   uvicorn app.main:app --reload
   ```

## 📖 API Documentation

### ML Prediction API

- **GET /** - Web interface for predictions
- **POST /predict** - Submit prediction request

### Celery API

- **POST /submit-task** - Submit background task
- **GET /task-status/{task_id}** - Check task status

### FastAPI CRUD

- **GET /docs** - Interactive API documentation (Swagger UI)
- **GET /redoc** - Alternative API documentation
- **GET /notes** - List all notes
- **POST /notes** - Create new note
- **GET /notes/{id}** - Get specific note
- **PUT /notes/{id}** - Update note
- **DELETE /notes/{id}** - Delete note

## 🚀 Deployment

### Heroku Deployment (ML Prediction)
The ML prediction service is Heroku-ready with a `Procfile`:

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git subtree push --prefix ml-prediction heroku master
```

### Docker Deployment
Each service includes Docker configurations:

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build individual containers
docker build -t service-name .
docker run -p 8000:8000 service-name
```

### Production Considerations

- **Security**: Implement authentication and authorization
- **Monitoring**: Add logging, metrics, and health checks
- **Scaling**: Use load balancers and multiple worker instances
- **Database**: Use managed database services in production
- **Secrets**: Use environment variables for sensitive data

## 🧪 Testing

### Run Unit Tests
```bash
# ML Prediction Service
cd ml-prediction
python -m pytest tests/

# Celery Services
cd celery-services
python test_db_connection.py

# FastAPI Service
cd fastapi_sqlalchemy-master
python -m pytest
```

### Load Testing
```bash
# Use tools like Apache Bench or wrk
ab -n 1000 -c 10 http://localhost:5000/
```

## 📊 Monitoring

### Celery Monitoring
```bash
# Monitor tasks in real-time
celery -A celery_app monitor

# Flower web-based monitoring
pip install flower
celery -A celery_app flower
# Visit http://localhost:5555
```

### Application Metrics
- Use tools like Prometheus, Grafana, or New Relic
- Implement health check endpoints
- Monitor database performance

## 🛠️ Development

### Project Structure
```
ml-backend-services/
├── ml-prediction/           # Flask ML service
│   ├── app.py              # Main Flask application
│   ├── model_1.pkl         # Trained ML model
│   ├── requirements.txt    # Python dependencies
│   └── templates/          # HTML templates
├── celery-services/        # Distributed task processing
│   ├── celery_app.py       # Celery application
│   ├── tasks.py            # Task definitions
│   ├── app/                # Flask web interface
│   └── deploy/             # Docker configuration
├── fastapi_sqlalchemy-master/  # Modern API service
│   ├── app/                # FastAPI application
│   ├── docker-compose.yml  # Container orchestration
│   └── requirements.txt    # Python dependencies
└── README.md               # This file
```

### Contributing Guidelines

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Code Style
- Follow PEP 8 for Python code
- Use type hints where possible
- Write comprehensive docstrings
- Add unit tests for new features

## 🐛 Troubleshooting

### Common Issues

1. **Redis Connection Error**
   ```bash
   # Make sure Redis is running
   redis-server
   # Check Redis status
   redis-cli ping
   ```

2. **Database Connection Issues**
   ```bash
   # Test database connection
   python test_db_connection.py
   ```

3. **Port Already in Use**
   ```bash
   # Find process using port
   lsof -i :5000
   # Kill process
   kill -9 <PID>
   ```

4. **Docker Issues**
   ```bash
   # Clean Docker resources
   docker system prune -a
   # Rebuild containers
   docker-compose up --build --force-recreate
   ```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- Create an [Issue](https://github.com/raushanmle/ml-backend-services/issues) for bug reports
- Start a [Discussion](https://github.com/raushanmle/ml-backend-services/discussions) for questions
- Follow [@raushanmle](https://github.com/raushanmle) for updates

## 🙏 Acknowledgments

- Thanks to the open-source community for the amazing tools and libraries
- Special thanks to contributors and users of this repository
- Inspired by real-world ML backend challenges and solutions

---

**Happy Coding! 🚀**

> Built with ❤️ by [Raushan](https://github.com/raushanmle)
