import g4f

print('Test 1')
response = g4f.ChatCompletion.create(model="gpt-3.5-turbo",
                                 provider=g4f.Provider.Vercel,
                                 stream=False,
                                 messages=[{'role': 'user', 'content': 'Hi!'}])

print(response)

print('Test 2')
response = g4f.ChatCompletion.create(model="gpt-4",
                                 provider=g4f.Provider.Bing,
                                 stream=False,
                                 messages=[{'role': 'user', 'content': 'Hi!'}])

print(response)


print('Test 3')
response = g4f.ChatCompletion.create(model="gpt-4",
                                 provider=g4f.Provider.BingHuan,
                                 stream=False,
                                 messages=[{'role': 'user', 'content': 'Hi!'}])

print(response)
