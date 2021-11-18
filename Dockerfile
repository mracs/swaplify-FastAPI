FROM python:3.9-slim

RUN apt-get -y update && \
    apt-get install -y libpq-dev

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip3 install --upgrade pip && pip3 install -r /app/requirements.txt

COPY . .

ENTRYPOINT ["bash", "entrypoint.sh"]
