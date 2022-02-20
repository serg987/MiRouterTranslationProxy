FROM python:3.8-alpine3.15
RUN mkdir /app
WORKDIR /app
ENV VIRTUAL_ENV=/app/venv
COPY ./*.py /app/
COPY requirements.txt .
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -r requirements.txt
ENV FLASK_ENV development
# ENV MI_ROUTER_IP 192.168.1.1      # uncomment it if you need to set up IP address of router explicitely
# ENV MI_ROUTER_TRANSLATION_LANG en      # uncomment it if you need to set up language explicitely
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
