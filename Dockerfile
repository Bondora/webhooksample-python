FROM python:3

RUN pip install flask waitress

WORKDIR /app

ADD . .

ENTRYPOINT ["waitress-serve", "app:app"]
