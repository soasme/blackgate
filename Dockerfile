FROM python:3.6-slim

MAINTAINER Lin Ju <soasme@gmail.com>

RUN pip install blackgate==0.2.6

VOLUME /etc/blackgate.yml

EXPOSE 9654

CMD blackgate --no-daemon -c /etc/blackgate.yml start
