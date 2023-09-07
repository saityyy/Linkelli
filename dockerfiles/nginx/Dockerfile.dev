FROM node:lts-alpine as builder

WORKDIR /app
COPY ./frontend/package.json .

RUN npm install
# build時間が短くなる
COPY ./frontend .
RUN npm run build

FROM nginx:alpine3.18-slim
COPY --from=builder /app/build /usr/share/nginx/html
