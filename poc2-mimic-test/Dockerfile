FROM python:3.10.3-slim-buster

ADD main.py /app/
ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt

ENTRYPOINT [ "python", "/app/main.py" ]
