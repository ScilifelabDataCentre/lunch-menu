FROM node:latest as build

COPY ./frontend /code
WORKDIR /code

RUN yarn install
RUN yarn build

FROM nginx:alpine

COPY --from=build /code/dist/ /usr/share/nginx/html/
COPY ./setup_frontend.sh /

EXPOSE 80

CMD ["/setup_frontend.sh"]
