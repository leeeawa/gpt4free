FROM python:3.10-slim-buster      
      
WORKDIR /app      
      
COPY requirements.txt requirements.txt    
  
RUN python -m venv venv  
ENV PATH="/app/venv/bin:$PATH"  
  
RUN apt-get update && \    
    apt-get install -y --no-install-recommends build-essential libffi-dev cmake libcurl4-openssl-dev && \    
    pip3 install --no-cache-dir -r requirements.txt      
      
COPY . .        
RUN chmod +x ./app.py
RUN chmod +x ./start.sh
RUN chmod -R 777 /app
CMD ["gunicorn --workers=3 app:app -b 0.0.0.0:80 -k 'gevent'"]
