FROM node:18.17.1-alpine3.18
RUN mkdir frontend
COPY ./frontend/package.json /frontend
WORKDIR /frontend
RUN npm install 
EXPOSE 3000
CMD ["/bin/sh"]
