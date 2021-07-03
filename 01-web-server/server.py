from socket import *
import sys
import threading
import time

serverPort = 12000

# prepare socker
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print('Ready to serve...')

def handle_request(connectionSocket, addr):
    try:
        message = connectionSocket.recv(1024).decode()

        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()

        # Status line
        connectionSocket.send(('HTTP/1.1 200 OK' + '\r\n').encode())

        # Headers
        connectionSocket.send(('Content-Type: text/html' + '\r\n').encode())
        connectionSocket.send("\r\n".encode())

        # Content
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send('\r\n'.encode())

        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        connectionSocket.send(('HTTP/1.1 400 Bad Request' + '\r\n').encode())
        connectionSocket.send(('Content-Type: text/plain' + '\r\n').encode())
        connectionSocket.send('\r\n'.encode())
        connectionSocket.send(('No such file').encode())

        connectionSocket.close()

while True:
    #Establish the connection
    connectionSocket, addr = serverSocket.accept()
    threading.Thread(target = handle_request, args = (connectionSocket, addr)).start()

    # serverSocket.close()
    # sys.exit() #Terminate the program after sending the corresponding data
