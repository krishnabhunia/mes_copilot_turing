# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set the working directory in the container
WORKDIR /trans

# Copy the current directory contents into the container at /app
COPY . /trans

# Install any dependencies specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements_transform.txt
RUN pip install --upgrade pip

# Define the command to run the Python script
CMD ["python", "translator.py", "en","fr","--input_folder","inp eng","--output_folder", "Translated_Docs"]
