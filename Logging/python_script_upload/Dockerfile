FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY upload_documents.py upload_documents.py
COPY sample.pdf sample.pdf

CMD ["python", "upload_documents.py"]
