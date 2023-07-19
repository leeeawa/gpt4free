import os
import helpers.poe
import random
from ..typing import sha256, Dict, get_type_hints

url = 'https://poe.com/'
models = {'gpt-3.5-turbo':'capybara','claude-instant':'a2','palm':'acouchy','palm2':'acouchy','bard':'acouchy','google-bard':'acouchy','google-palm':'acouchy'}
model = ['gpt-3.5-turbo','claude-instant','palm']
supports_stream = True
needs_auth = False
working = True
token = ['H959lSH8kjQ-b4K8FCrDPg%3D%3D']

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    conversation = 'This is a conversation between a human and a language model. The language model should always respond as the assistant, referring to the past history of messages if needed.\n'
    
    for message in messages:
        conversation += '%s: %s\n' % (message['role'], message['content'])
    
    conversation += 'assistant: '
    client = helpers.poe.Client(random.choice(token))

    for chunk in client.send_message(models[model], conversation, with_chat_break=True):
      yield chunk["text_new"]
    client.purge_conversation(models[model], count=3)


params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join(
        [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
