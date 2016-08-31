FROM python:2.7-slim

MAINTAINER Lin Ju <soasme@gmail.com>

RUN pip install blackgate==0.2.5

VOLUME /etc/blackgate.yml

EXPOSE 9654

CMD blackgate --no-daemon -c /etc/blackgate.yml start
