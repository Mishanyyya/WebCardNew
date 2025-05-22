FROM python:3.12-slim

RUN pip install --upgrade pip && apt-get update && apt-get install -y gcc libpq-dev python3-dev libjpeg-dev zlib1g-dev

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py makemigrations main

RUN python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "WebCardNew.wsgi", "--bind", "0.0.0.0:8000"]
