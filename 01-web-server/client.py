from socket import *
import sys

_, SERVER_HOST, SERVER_PORT, FILENAME = sys.argv

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((SERVER_HOST, int(SERVER_PORT)))

httpMessage = f'GET /{FILENAME} HTTP/1.1'

clientSocket.send(httpMessage.encode())

fragments = ''
while True:
    chunk = clientSocket.recv(1024)
    if not chunk:
        break
    fragments += chunk.decode()

print('Server response:', fragments)
clientSocket.close()
