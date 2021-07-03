from socket import *

serverName = '0.0.0.0'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

message = input('Input lowercase sentence:')

clientSocket.send(message.encode())
modifiedSentence = clientSocket.recv(1024)

print('From Server: ', modifiedSentence.decode())
clientSocket.close()
