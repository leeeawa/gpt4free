import os
import g4f
import requests
import json
import time
import pytz
from datetime import datetime

while True:
  files = os.listdir("g4f/Provider/Providers")
  files = [f for f in files if os.path.isfile(os.path.join("g4f/Provider/Providers", f))]
  files.sort(key=str.lower)
  status = {'data':[]}
  for file in files:
      if file.endswith(".py"):
          name = file[:-3]
          try:
              p = getattr(g4f.Provider,name)
              status['data'].append({
              "provider": name,
              "model": [],
              "url":p.url
              })
              for i in p.model:
                  status['data'][-1]['model'].append({i:{'status':''}})
                  try:
                      response = g4f.ChatCompletion.create(model=i, provider=p, messages=[{"role": "user", "content": "Say 'Hello World!'"}], stream=False)
                      if 'Hello World' in response or 'Hello' in response or 'hello' in response or 'world' in response:
                          status['data'][-1]['model'][-1][i]['status'] = 'Active'
                      else:
                          status['data'][-1]['model'][-1][i]['status'] = 'Inactive'
                  except:
                      status['data'][-1]['model'][-1][i]['status'] = 'Inactive'
              
          except:
              pass
            
  print(status)
  status['key'] = "test"
  tz = pytz.timezone('Asia/Shanghai')
  now = datetime.now(tz)
  print(now)
  status['time'] = now.strftime("%Y-%m-%d %H:%M:%S")
  r = requests.post("https://gpt.lemonsoftware.eu.org/v1/status",data=json.dumps(status),headers={"content-type": "application/json"})
  print(r.text)
  time.sleep(900)
