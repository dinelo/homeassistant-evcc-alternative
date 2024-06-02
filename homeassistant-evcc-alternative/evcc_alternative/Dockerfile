FROM homeassistant/amd64-base-python:3.9

COPY data /data
RUN chmod a+x /data/run.sh

CMD [ "/data/run.sh" ]
