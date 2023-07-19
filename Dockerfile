FROM python:latest 
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app
COPY --chown=user requirements.txt requirements.txt  
RUN pip install --no-cache-dir --upgrade pip
RUN apt-get update && \    
    apt-get install -y --no-install-recommends build-essential libffi-dev cmake libcurl4-openssl-dev nodejs screen && \    
    pip install --no-cache-dir -r requirements.txt
COPY --chown=user . $HOME/app
CMD ["python3", "./run.py"]  
