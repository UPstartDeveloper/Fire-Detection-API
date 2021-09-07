FROM python:3.6-slim
COPY app/ /app/
COPY classifier/ /classifier/
WORKDIR /
RUN apt update
RUN apt install -y git
RUN apt-get install -y libglib2.0-0
RUN pip install git+https://github.com/UPstartDeveloper/Fire-Detection-API
EXPOSE 8080

ENTRYPOINT uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 1