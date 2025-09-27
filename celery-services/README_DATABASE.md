# Complete Celery Service Tutorial with Database Integration

A comprehensive educational repository for beginners to learn Celery distributed task processing with real-world database integration.

## 📚 Table of Contents
- [What is Celery?](#what-is-celery)
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Components Explained](#components-explained)
- [Database Integration](#database-integration)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Testing & Monitoring](#testing--monitoring)
- [Common Issues & Troubleshooting](#common-issues--troubleshooting)
- [Learning Exercises](#learning-exercises)

## 🎯 What is Celery?

**Celery** is a distributed task queue system for Python that allows you to:
- Execute tasks asynchronously (in the background)
- Scale horizontally by adding more worker processes
- Handle long-running operations without blocking your main application
- Retry failed tasks automatically
- Schedule tasks to run at specific times

### Real-world Use Cases:
- **Email sending**: Send emails without making users wait
- **Image processing**: Resize images in the background
- **Data analysis**: Process large datasets asynchronously
- **Report generation**: Create PDF reports without blocking UI
- **Web scraping**: Crawl websites in parallel

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client App    │───▶│   Message       │───▶│   Celery        │
│  (send_task.py) │    │   Broker        │    │   Worker        │
│                 │    │  (RabbitMQ)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐              │
                       │   Result        │◀─────────────┘
                       │   Backend       │
                       │   (Redis)       │
                       └─────────────────┘
                                │
                       ┌─────────────────┐
                       │   Database      │
                       │  (SQL Server)   │
                       │                 │
                       └─────────────────┘
```

### Key Components:
1. **Message Broker (RabbitMQ)**: Queues tasks for processing
2. **Result Backend (Redis)**: Stores task results and status
3. **Celery Worker**: Processes tasks from the queue
4. **Database (SQL Server)**: Persists business data and logs
5. **Client Application**: Sends tasks to the queue

## ✅ Prerequisites

### Software Requirements:
- Docker & Docker Compose
- Python 3.8+
- Basic understanding of:
  - Python functions and modules
  - Database concepts
  - Command line operations

### Knowledge Prerequisites:
- Basic Python programming
- Understanding of asynchronous vs synchronous operations
- Familiarity with Docker containers (helpful but not required)

## 📁 Project Structure

```
celery-services/
├── app/
│   ├── __init__.py
│   └── app.py                 # Main business logic
├── deploy/
│   ├── docker-compose.yml     # Multi-service orchestration
│   └── Dockerfile            # Worker container definition
├── celery_app.py             # Celery application setup
├── celery_config.py          # Celery configuration
├── tasks.py                  # Task definitions
├── send_task.py              # Client to send tasks
├── manage.sh                 # Worker startup script
├── requirements.txt          # Python dependencies
└── README_DATABASE.md        # This file
```

## 🔧 Components Explained

### 1. **Celery Application (`celery_app.py`)**
```python
from celery import Celery

celery_app = Celery(__name__, include=["tasks"])
celery_app.config_from_object("celery_config")
```
- Creates the main Celery application instance
- Includes task modules automatically
- Loads configuration from separate file

### 2. **Configuration (`celery_config.py`)**
```python
broker_url = "amqp://guest:guest@rabbitmq:5672//"
result_backend = "redis://redis:6379/0"
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
```
- **broker_url**: Where to send tasks (RabbitMQ)
- **result_backend**: Where to store results (Redis)
- **serializers**: How to convert data to/from storage

### 3. **Task Definition (`tasks.py`)**
```python
@celery_app.task(
    name="tasks.run_celery",
    queue="tasks.run_celery-queue",
    bind=True
)
def run_task(self, val: str):
    run(val)
    return "Task completed with value: %s" % val
```
- **@celery_app.task**: Decorator that makes function a Celery task
- **name**: Unique identifier for the task
- **queue**: Which queue this task belongs to
- **bind=True**: Provides access to task context (self)

### 4. **Business Logic (`app/app.py`)**
This file contains the actual work your tasks perform:
- Database connection management
- Data processing logic
- Error handling and logging
- Integration with external services

### 5. **Task Sender (`send_task.py`)**
```python
celery.send_task(
    "tasks.run_celery",
    args=("aa",),
    queue="tasks.run_celery-queue",
)
```
- Sends tasks to the queue without importing task functions
- Can be used from separate applications
- Provides loose coupling between sender and worker

## 💾 Database Integration

### Why Add Database Integration?
In real applications, tasks often need to:
- Store processing results
- Log execution history
- Update application state
- Generate reports and analytics

### Database Schema
```sql
CREATE TABLE task_logs (
    id INT IDENTITY(1,1) PRIMARY KEY,      -- Auto-increment ID
    task_value NVARCHAR(255),              -- Input parameter
    executed_at DATETIME,                  -- When task ran
    status NVARCHAR(50),                   -- Success/failure status
    metadata NVARCHAR(MAX)                 -- Additional context (JSON)
)
```

### Database Operations in Tasks
1. **Connection Management**: Establish database connection
2. **Table Creation**: Ensure required tables exist
3. **Data Writing**: Insert task execution records
4. **Error Handling**: Graceful failure handling
5. **Connection Cleanup**: Properly close connections

### Key Functions:
- `get_db_connection()`: Establishes connection to SQL Server
- `create_table_if_not_exists()`: Creates task_logs table if needed
- `write_task_data()`: Logs task execution to database
- Enhanced `run()` function: Performs database operations

## 🚀 Setup Instructions

### Step 1: Clone and Navigate
```bash
git clone <your-repo-url>
cd celery-services
```

### Step 2: Start All Services
```bash
cd deploy
docker compose up -d --build
```

This starts:
- **RabbitMQ**: Message broker (ports 5672, 15672)
- **Redis**: Result backend (port 6379)
- **SQL Server**: Database (port 1433)
- **Azurite**: Azure Storage emulator (port 10000)
- **Celery Worker**: Task processor

### Step 3: Verify Services
```bash
# Check all containers are running
docker compose ps

# Check worker logs
docker compose logs worker

# Check RabbitMQ management UI
# Visit: http://localhost:15672 (guest/guest)
```

## 🎮 Running the Application

### Send a Task
```bash
# From project root
python send_task.py
```

### Monitor Execution
```bash
# Watch worker logs in real-time
docker compose -f deploy/docker-compose.yml logs -f worker

# Check all service logs
docker compose -f deploy/docker-compose.yml logs
```

### Expected Output
```
[2025-09-27 15:35:28,905: WARNING/ForkPoolWorker-1] Task executed with value: aa
[2025-09-27 15:35:29,106: WARNING/ForkPoolWorker-1] Table 'task_logs' created or already exists
[2025-09-27 15:35:29,121: WARNING/ForkPoolWorker-1] Data written to database. Record ID: 1
[2025-09-27 15:35:29,121: WARNING/ForkPoolWorker-1] Successfully logged task execution to database (ID: 1)
```

## 📊 Testing & Monitoring

### Database Connection (DBeaver)
- **Host**: `localhost`
- **Port**: `1433`
- **Database**: `master`
- **Username**: `sa`
- **Password**: `YourStrong@Passw0rd`

### RabbitMQ Management
- **URL**: http://localhost:15672
- **Username**: `guest`
- **Password**: `guest`
- Monitor queues, exchanges, and message rates

### Redis Monitoring
```bash
# Connect to Redis
docker exec -it redisserver redis-cli

# View all keys
KEYS *

# Get task result
GET celery-task-meta-<task-id>
```

### Task Monitoring Queries
```sql
-- View all task executions
SELECT * FROM task_logs ORDER BY executed_at DESC;

-- Count tasks by status
SELECT status, COUNT(*) as count 
FROM task_logs 
GROUP BY status;

-- Recent task activity
SELECT TOP 10 task_value, executed_at, status 
FROM task_logs 
WHERE executed_at > DATEADD(hour, -1, GETDATE())
ORDER BY executed_at DESC;
```

## 🔍 Common Issues & Troubleshooting

### 1. Worker Can't Connect to Broker
**Symptoms**: `Connection refused` errors
**Solutions**:
- Ensure RabbitMQ container is running: `docker compose ps`
- Check network connectivity: `docker compose logs rabbitmq`
- Verify broker URL in configuration

### 2. Database Connection Fails
**Symptoms**: `Database connection failed` messages
**Solutions**:
- Ensure SQL Server container is running
- Check ODBC driver installation in Dockerfile
- Verify connection string parameters
- Check TrustServerCertificate setting

### 3. Tasks Don't Execute
**Symptoms**: Tasks sent but never processed
**Solutions**:
- Check queue names match between sender and worker
- Verify worker is listening to correct queues
- Check RabbitMQ management UI for queue status

### 4. Import Errors
**Symptoms**: `ModuleNotFoundError` when sending tasks
**Solutions**:
- Install requirements: `pip install -r requirements.txt`
- Check Python path configuration
- Ensure virtual environment is activated

## 🎓 Learning Exercises

### Exercise 1: Basic Task Modification
Modify the task to:
1. Accept multiple parameters
2. Perform different operations based on input
3. Return structured data

### Exercise 2: Error Handling
Add error handling to:
1. Handle database connection failures gracefully
2. Implement task retry logic
3. Log errors to separate table

### Exercise 3: Task Monitoring
Create a monitoring dashboard:
1. Build a simple web interface
2. Display real-time task statistics
3. Show recent task history

### Exercise 4: Advanced Features
Implement advanced Celery features:
1. Task routing to different queues
2. Task scheduling with Celery Beat
3. Task callbacks and chaining
4. Custom task classes

### Exercise 5: Scaling
Experiment with scaling:
1. Run multiple worker instances
2. Use different concurrency models
3. Implement task prioritization
4. Monitor performance metrics

## 📈 Production Considerations

### Security
- Change default passwords
- Use SSL/TLS for connections
- Implement proper authentication
- Secure network communications

### Performance
- Monitor queue depths
- Optimize database queries
- Use connection pooling
- Implement proper logging levels

### Reliability
- Set up health checks
- Implement backup strategies
- Use persistent message storage
- Plan for failure scenarios

### Monitoring
- Set up alerting for failed tasks
- Monitor resource usage
- Track performance metrics
- Implement distributed tracing

## 🔗 Additional Resources

### Documentation
- [Celery Official Documentation](https://docs.celeryproject.org/)
- [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials.html)
- [Redis Documentation](https://redis.io/documentation)

### Tools
- [Flower](https://flower.readthedocs.io/) - Celery monitoring tool
- [Celery Beat](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html) - Task scheduling
- [Prometheus](https://prometheus.io/) - Metrics collection

---

## 🎉 Congratulations!

You now have a complete understanding of how to build, deploy, and monitor a Celery-based distributed task processing system with database integration. This foundation will help you build scalable, asynchronous applications in production environments.
