FROM node:18.17.1-alpine3.18
RUN apk update
RUN apk add --no-cache git 
RUN cd / && git clone https://github.com/saityyy/Linkelli.git
WORKDIR /Linkelli/frontend
RUN npm install 
EXPOSE 3000
CMD ["/bin/sh"]
