FROM python:3.10.3-slim-buster

# This directory is setup to persist between VM restarts in GCP
RUN mkdir -p /etc/hackathon

ADD main.py /etc/hackathon/

CMD [ "python", "/etc/hackathon/main.py" ]
