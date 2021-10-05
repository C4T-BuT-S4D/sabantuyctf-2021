FROM ubuntu:latest
WORKDIR /usr/local/app
RUN apt update && apt -y install python3 python3-pip
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY app.py .
COPY templates templates
ENTRYPOINT [ "python3", "app.py" ]