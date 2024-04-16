FROM python:3.8

RUN apt-get -y update

ENV PYTHONUNBUFFERED 1

COPY . /app/
WORKDIR /app/

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --clear --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
