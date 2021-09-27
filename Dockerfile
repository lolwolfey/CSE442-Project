FROM python:3.7.4

ENV HOME /root
WORKDIR /root

COPY . .

EXPOSE 8000

RUN pip3 install -r requirements.txt
RUN pip3 install flask

CMD export FLASK_APP=app && flask run 