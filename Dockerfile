# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_ENV development
# ENV MI_ROUTER_IP 192.168.1.1      # uncomment it if you need to set up IP address of router explicitely
# ENV MI_ROUTER_TRANSLATION_LANG en      # uncomment it if you need to set up language explicitely
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
