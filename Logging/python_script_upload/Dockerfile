FROM python:3.10-slim

WORKDIR /app
COPY upload_documents.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "upload_documents.py"]
