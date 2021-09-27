FROM python:3.7.4

ENV HOME /root
WORKDIR /root

COPY . .

EXPOSE $PORT

RUN pip3 install -r requirements.txt
RUN pip3 install flask

CMD python3 app.py $PORT