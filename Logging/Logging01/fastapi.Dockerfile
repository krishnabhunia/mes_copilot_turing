
#newlogging/Logging01/fastapi.Dockerfile for app.py
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container and install dependencies
# COPY Logging01/requirements.txt .
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy Config.json to the working directory (ensure Config.json is in the build context)
# COPY Logging01/Config.json /app/Config.json
COPY Config.json /app/Config.json

# Copy the rest of the application code
# COPY Logging01/ .  
COPY . .
# Ensure this directory contains app.py

# Define a volume for the log directory
VOLUME /app/log_directory


# Expose port 7408 for app
EXPOSE 7408

# Command to run the app application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7408"]




#"docker_volume_path": "/var/lib/docker/volumes/my_log_volume/_data/",
# "docker_volume_path": "/app/log_directory/",

# "docker_volume_path": "/app/log_directory/",