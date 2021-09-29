FROM python:3.6-slim
COPY app/ /app/
COPY classifier/ /classifier/
COPY requirements.txt /
WORKDIR /
RUN apt update
RUN apt install -y git
RUN apt-get install -y libglib2.0-0
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT uvicorn app.main:app --host 0.0.0.0 --port 5000 --workers 1