FROM python:3.12.4
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# CMD ["python", "test_service.py", "&&", "python", "test_service02.py", "&&", "python", "retrieve_test.py"]
CMD ["sh", "-c", "python test_service.py && python test_service02.py && python retrieve_test.py"]
