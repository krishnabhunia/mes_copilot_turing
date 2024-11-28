FROM python:3.10-slim

WORKDIR /app
COPY upload_document.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "upload_document.py"]
