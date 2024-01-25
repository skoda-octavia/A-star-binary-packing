FROM python:3.10
WORKDIR /app
COPY requirements.txt .
COPY files .
RUN apt-get update && apt-get install -y python3-tk
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3", "main.py" ]