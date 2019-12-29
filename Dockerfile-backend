FROM python:latest as build

RUN mkdir /code
COPY ./*.py /code/
COPY ./requirements.txt /code/
COPY ./restaurants.txt /code/
WORKDIR /code

RUN pip install -r requirements.txt
RUN pip install gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "flask_app:app"]

EXPOSE 8000