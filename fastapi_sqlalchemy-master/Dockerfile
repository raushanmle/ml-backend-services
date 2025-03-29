FROM python:3.12

# Set the working directory to the root of the project
WORKDIR /fastapi

# Install PostgreSQL client tools
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Add the root directory as a watch directory for uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "fastapi"]