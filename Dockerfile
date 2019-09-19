FROM python:3.6-slim

MAINTAINER Lin Ju <soasme@gmail.com>

RUN pip install blackgate==0.3.0

VOLUME /etc/blackgate

EXPOSE 9654

CMD blackgate --no-daemon -c /etc/blackgate/blackgate.yml start
