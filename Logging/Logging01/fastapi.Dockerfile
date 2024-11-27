# Use a base image with Python
FROM python:3.12.4

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]