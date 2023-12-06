FROM python:3.10.3-slim-buster

# This directory is setup to persist between VM restarts in GCP
RUN mkdir -p /etc/hackathon

ADD main.py /etc/hackathon/
ADD requirements.txt /etc/hackathon/
RUN pip install -r /etc/hackathon/requirements.txt

CMD [ "python", "/etc/hackathon/main.py" ]
