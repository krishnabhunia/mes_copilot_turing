#service/Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app1

# Copy the test script and test data
# COPY test_service.py .
# COPY test_data /test_data

COPY . .

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 7500

# Set the entry point for the container
CMD ["uvicorn", "test_service:app1", "--host", "0.0.0.0", "--port", "7500"]
