FROM python:2.7

MAINTAINER sourceperl <loic.celine@free.fr>

# install python library
RUN mkdir -p /opt/sigserver
WORKDIR /opt/sigserver/
COPY requirements.txt /opt/sigserver/
COPY sigserver.py /opt/sigserver/
RUN pip install -r requirements.txt

# add user sigserver to image
RUN groupadd -r sigserver && useradd --shell /usr/sbin/nologin -d /opt/sigserver/ -r -g sigserver sigserver

# process run as sigserver user
USER sigserver

# run process, expose tcp/3000 endpoint
EXPOSE 3000
CMD python sigserver.py
