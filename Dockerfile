FROM python:3

RUN pip install pipreqs
RUN python -m  pipreqs.pipreqs --encoding utf-8  /var/printer/measurements
RUN pip3 install -r requirements.txt

WORKDIR  /var/printer/measurements

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install python-dotenv

CMD ["python", "./readMeasurements.py" ]

