FROM python:3

ADD main.py /app/
ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt
WORKDIR /app/

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]