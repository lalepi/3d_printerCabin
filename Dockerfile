FROM python:3

WORKDIR  /usr/src/app


#RUN pip install pipreqs
#RUN python -m  pipreqs.pipreqs --encoding utf-8
#RUN pip3 install -r requirements.txt

COPY measurements/requirements.txt ./
COPY .env ./

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install python-dotenv

COPY . .


CMD ["python", "readMeasurements.py" ]





