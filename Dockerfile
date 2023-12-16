FROM python:3

WORKDIR  /var/printer/3d_printerCabin

RUN mkdir measurements

WORKDIR  /var/printer/3d_printerCabin/measurements

ADD readMeasurements.py ./

RUN pip install pipreqs
RUN python -m  pipreqs.pipreqs --encoding utf-8  /var/printer/3d_printerCabin/measurements
RUN pip3 install -r requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install python-dotenv

CMD ["python3", "./readMeasurements.py" ]

