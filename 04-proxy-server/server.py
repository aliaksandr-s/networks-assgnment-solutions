from socket import *
import traceback

SERVER_PORT = 8888
CACHE_FOLDER = 'cache'

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM,)
tcpSerSock.bind(('', SERVER_PORT))
tcpSerSock.listen(1)

while 1:
    # Start receiving data from the client
    print('Ready to serve...\r\n')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024).decode()
    print(message)

    # Extract the filename from the given message
    filename = message.split()[1].partition("/")[2].replace("www.","",1)
    print('filename:', filename)

    fileExist = "false"

    filetouse = f'/{CACHE_FOLDER}/{filename}'
    print('filetouse', filetouse)

    try:
        # Check wether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        f.close()

        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(('HTTP/1.1 200 OK' + '\r\n').encode())
        tcpCliSock.send(('Content-Type: text/html' + '\r\n').encode())
        tcpCliSock.send('\r\n'.encode())

        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i].encode())

        tcpCliSock.send('\r\n'.encode())
        print('Read from cache')

    # Error handling for file not found in cache
    except IOError:
        print('Not found in cache')
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            c.settimeout(2)
            hostn = filename.split("/")[0]
            print('hostn:', hostn)

            try:
                # Connect to the socket to port 80
                c.connect((hostn, 80))

                message = f'GET / HTTP/1.0\r\n\r\n'
                print('message:', message)
                c.send(message.encode())

                # Read the response into buffer
                response = ''
                while True:
                    chunk = c.recv(1024)
                    if not chunk:
                        break
                    response += chunk.decode()

                # Create a new file in the cache for the requested file.
                tmpFile = open('.' + filetouse, "w")

                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile.write(response)
                tmpFile.close()
                tcpCliSock.send(response.encode())
            except timeout:
                print('timeout')
            except:
                traceback.print_exc()
                print("Illegal request")
        else:
            # HTTP response message for file not found
            tcpCliSock.send("HTTP/1.0 404 Not Found\r\n".encode())
            tcpCliSock.send("Content-Type:text/html\r\n".encode())
            tcpCliSock.send('\r\n'.encode())

    # Close the client and the server sockets
    tcpCliSock.close()
    print('Close socket\r\n')

tcpSerSock.close()
