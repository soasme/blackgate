FROM python:2.7-slim

MAINTAINER Lin Ju <soasme@gmail.com>

RUN pip install blackgate==0.2.3

VOLUME /etc/blackgate/blackgate.yml

CMD blackgate --no-daemon start
