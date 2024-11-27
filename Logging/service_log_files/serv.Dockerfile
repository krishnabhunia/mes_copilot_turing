#service/Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.12.4

# Set the working directory in the container
WORKDIR /app

COPY ./service_log_files .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the entry point for the container
CMD ["python", "test_service01.py"]
