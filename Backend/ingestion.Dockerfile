# Use a base image with Python
FROM python:3.12.4

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files into the container
COPY /app/database.py /app/
COPY /ingestion/ingest_data.py /app/

# Copy requirements and install dependencies
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the script
CMD ["python", "ingest_data.py"]