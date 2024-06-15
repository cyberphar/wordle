FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libssl-dev \
    libffi-dev \
    python3-dev \
    build-essential \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#RUN mkdir -p /app/flask_session

#RUN chown -R 1000:1000 /app/flask_session
#RUN chmod -R 700 /app/flask_session

# Set the user to use when running the image
#USER 1000:1000

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5005

CMD ["python3", "app.py"]
