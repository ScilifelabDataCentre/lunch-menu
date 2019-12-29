#!/bin/sh

echo $API_URL

variable=VUE_APP_API_URL
sed -i "s,$variable,$API_URL,g" /usr/share/nginx/html/js/app.*

nginx -g 'daemon off;'
