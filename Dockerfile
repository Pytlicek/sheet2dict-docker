FROM python:3.10-slim
COPY ./app /app
RUN pip install -r /app/requirements.txt

WORKDIR /app
EXPOSE 5000
CMD ["python3", "main.py"]

LABEL name=sheet2dict-api
LABEL version=0.1




faas-cli new --lang dockerfile sample-flask-service
