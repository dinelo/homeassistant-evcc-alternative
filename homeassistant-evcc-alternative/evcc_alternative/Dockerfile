FROM python:3.9-slim

COPY run.sh /run.sh
COPY evcc_alternative.py /evcc_alternative.py
RUN chmod a+x /run.sh

RUN pip install flask

CMD [ "/run.sh" ]
