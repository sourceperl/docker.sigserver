# datastore.server
Sigfox server (HTTP callback endpoint)

Expose :

tcp/3000: HTTP callback endpoint

Build :

    docker build -t sourceperl/sigserver .

Run container :

    docker run -d -p 3000:3000 --name=sigserver sourceperl/sigserver

