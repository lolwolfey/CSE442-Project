FROM python:3.7.4

ENV HOME /root
WORKDIR /root

COPY . .

EXPOSE 8000

RUN pip install flask

CMD export FLASK_APP=app && flask run 