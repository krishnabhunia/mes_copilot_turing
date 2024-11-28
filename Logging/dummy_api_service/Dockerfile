# Use a base image with Python
FROM python:3.12.4
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8005
CMD ["uvicorn", "api_dummy:app", "--host", "0.0.0.0", "--port", "8005", "--reload"]