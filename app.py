import os
import time
import json
import random
import requests
import g4f
from flask import Flask, request, Response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/v1/chat/completions", methods=['POST'])
@app.route("/v1/completions", methods=['POST'])
def chat_completions():
    streaming = request.json.get('stream', False)
    streaming_ = request.json.get('stream', False)
    model = request.json.get('model', 'gpt-3.5-turbo')
    messages = request.json.get('messages')
    provider = request.json.get('provider', False)
    if not provider:
        r = requests.get('https://gpt.lemonsoftware.eu.org/v1/status')
        data = r.json()['data']
        random.shuffle(data)
        for provider_info in data:
            for model_info in provider_info['model']:
                if model in model_info and model_info[model]['status'] == 'Active':
                    if getattr(g4f.Provider,provider_info['provider']).supports_stream != streaming_:
                      streaming = False
                    else:
                      streaming = True
                    response = g4f.ChatCompletion.create(model=model, provider=getattr(g4f.Provider,provider_info['provider']),stream=streaming,
                                     messages=messages)
                    provider_name = provider_info['provider']
                    print(provider_name)
                    break
            else:
                continue
            break
    else:
        provider_name = provider
        if getattr(g4f.Provider,provider).supports_stream != streaming_:
          streaming = False
        else:
          streaming = True
        response = g4f.ChatCompletion.create(model=model, provider=getattr(g4f.Provider,provider),stream=streaming,
                                     messages=messages)
    if not provider:
      while 'curl_cffi.requests.errors.RequestsError' in response:
          random.shuffle(data)
          for provider_info in data:
              for model_info in provider_info['model']:
                  if model in model_info and model_info[model]['status'] == 'Active':
                      if getattr(g4f.Provider,provider_info['provider']).supports_stream != streaming_:
                        streaming = False
                      else:
                        streaming = True
                      response = g4f.ChatCompletion.create(model=model, provider=getattr(g4f.Provider,provider_info['provider']),stream=streaming,
                                      messages=messages)
                      provider_name = provider_info['provider']
                      print(provider_name)
                      break
              else:
                  continue
              break
                
    if not streaming_:
        completion_timestamp = int(time.time())
        completion_id = ''.join(random.choices(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))

        return {
            'id': 'chatcmpl-%s' % completion_id,
            'object': 'chat.completion',
            'created': completion_timestamp,
            'model': model,
            'provider':provider_name,
            'supports_stream':getattr(g4f.Provider,provider_name).supports_stream,
            'usage': {
                'prompt_tokens': len(messages),
                'completion_tokens': len(response),
                'total_tokens': len(messages)+len(response)
            },
            'choices': [{
                'message': {
                    'role': 'assistant',
                    'content': response
                },
                'finish_reason': 'stop',
                'index': 0
            }]
        }
    print(response)
    def stream():
        nonlocal response
        for token in response:
            completion_timestamp = int(time.time())
            completion_id = ''.join(random.choices(
                'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))

            completion_data = {
                'id': f'chatcmpl-{completion_id}',
                'object': 'chat.completion.chunk',
                'created': completion_timestamp,
                'choices': [
                    {
                        'delta': {
                            'content': token
                        },
                        'index': 0,
                        'finish_reason': None
                    }
                ]
            }
            print(token)
            print(completion_data)
            print('data: %s\n\n' % json.dumps(completion_data, separators=(',' ':')))
            yield 'data: %s\n\n' % json.dumps(completion_data, separators=(',' ':'))
            time.sleep(0.1)
    print('===Start Streaming===')
    return app.response_class(stream(), mimetype='text/event-stream')
    
@app.route("/v1/dashboard/billing/subscription")
@app.route("/dashboard/billing/subscription")
def billing_subscription():
  return jsonify({
  "object": "billing_subscription",
  "has_payment_method": True,
  "canceled": False,
  "canceled_at": None,
  "delinquent": None,
  "access_until": 2556028800,
  "soft_limit": 6944500,
  "hard_limit": 166666666,
  "system_hard_limit": 166666666,
  "soft_limit_usd": 416.67,
  "hard_limit_usd": 9999.99996,
  "system_hard_limit_usd": 9999.99996,
  "plan": {
    "title": "Pay-as-you-go",
    "id": "payg"
  },
  "primary": True,
  "account_name": "OpenAI",
  "po_number": None,
  "billing_email": None,
  "tax_ids": None,
  "billing_address": {
    "city": "New York",
    "line1": "OpenAI",
    "country": "US",
    "postal_code": "NY10031"
  },
  "business_address": None
}
)


@app.route("/v1/dashboard/billing/usage")
@app.route("/dashboard/billing/usage")
def billing_usage():
  return jsonify({
  "object": "list",
  "daily_costs": [
    {
      "timestamp": time.time(),
      "line_items": [
        {
          "name": "GPT-4",
          "cost": 0.0
        },
        {
          "name": "Chat models",
          "cost": 1.01
        },
        {
          "name": "InstructGPT",
          "cost": 0.0
        },
        {
          "name": "Fine-tuning models",
          "cost": 0.0
        },
        {
          "name": "Embedding models",
          "cost": 0.0
        },
        {
          "name": "Image models",
          "cost": 16.0
        },
        {
          "name": "Audio models",
          "cost": 0.0
        }
      ]
    }
  ],
  "total_usage": 1.01
}
)

@app.route("/v1/models")
@app.route("/models")
def models():
  import g4f.models
  model = {"data":[]}
  for i in g4f.models.ModelUtils.convert:
    model['data'].append({
            "id": i,
            "object": "model",
            "owned_by": g4f.models.ModelUtils.convert[i].base_provider,
            "tokens": 99999,
            "fallbacks": None,
            "endpoints": [
                "/v1/chat/completions"
            ],
            "limits": None,
            "permission": []
        })
  return jsonify(model)

@app.route("/v1/providers")
@app.route("/providers")
def providers():
  files = os.listdir("g4f/Provider/Providers")
  files = [f for f in files if os.path.isfile(os.path.join("g4f/Provider/Providers", f))]
  files.sort(key=str.lower)
  providers_data = {"data":[]}
  for file in files:
      if file.endswith(".py"):
          name = file[:-3]
          try:
              p = getattr(g4f.Provider,name)
              providers_data["data"].append({
              "provider": str(name),
              "model": list(p.model),
              "url": str(p.url),
              "working": bool(p.working),
              "supports_stream": bool(p.supports_stream)
              })
          except:
                pass
  return jsonify(providers_data)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({
        "error": {
            "message": f"Invalid URL ({request.method} /)",
            "type": "invalid_request_error",
            "param": None,
            "code": None
        }
    }), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({
        "error": {
            "message": "Something went wrong on our end",
            "type": "internal_server_error",
            "param": None,
            "code": None
        }
    }), 500

@app.errorhandler(415)
def unsupported_media_type(e):
    return jsonify({
        "error": {
            "message": "Unsupported media type",
            "type": "unsupported_media_type",
            "param": None,
            "code": None
        }
    }), 415
if __name__ == '__main__':
    config = {
        'host': '0.0.0.0',
        'port': 7860,
        'debug': False
    }

    app.run(**config)
