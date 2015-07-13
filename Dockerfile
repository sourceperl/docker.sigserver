FROM python:2.7

MAINTAINER sourceperl <loic.celine@free.fr>

# install python library
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt

# add user sigserver to image
RUN groupadd -r sigserver && useradd -r -g sigserver sigserver

# process run as sigserver user
USER sigserver

# run process, expose tcp/3000 endpoint
EXPOSE 3000
CMD python sigserver.py
