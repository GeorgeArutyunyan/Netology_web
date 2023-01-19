FROM python:alpine
WORKDIR /app

COPY . /app
COPY /Users/georgearutyunyan/netology_web/Docker_task/task1/index.html /usr/share/nginx/html
RUN pip install -r requirements.txt
EXPOSE 7777

CMD ['python', 'main.py']