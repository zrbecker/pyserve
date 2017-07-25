from pyserve import Client

client = Client('localhost', 5050)
print('sending message')
client.send('Hello World!')
print('recieved')
print(client.recv(512).decode('utf-8'))
