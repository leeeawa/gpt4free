FROM python:3
USER root
RUN apt-get update && \    
    apt-get install -y --no-install-recommends build-essential libffi-dev cmake libcurl4-openssl-dev nodejs screen sudo
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod -R 777 /usr/src/app
RUN chmod -R 777 ./app.py
RUN chmod -R 777 ./check.py

CMD [ "python3", "./app.py" ]
