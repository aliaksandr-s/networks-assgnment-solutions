from socket import *
from base64 import b64encode
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


MAIL_TO_ADDRESS = 'bob@bob.com'
EMAIL_TEXT = "I love computer networks!"
EMAIL_SUBJECT = "Test Message"
IMG_URL = 'rat-pepe.png'
END_MESSAGE = "\r\n.\r\n"

MAIL_HOST = 'smtp.gmail.com'
MAIL_PORT = 587

# Note that for gmail less secure app setting should be on
USERNAME = 'user@gmail.com'
PASSWORD = 'password'


# Construct multipart message
msg = MIMEMultipart()
msg["To"] = MAIL_TO_ADDRESS
msg["From"] = USERNAME
msg["Subject"] = EMAIL_SUBJECT

msgText = MIMEText(
    f'<h3>{EMAIL_TEXT}</h3><img src="cid:{IMG_URL}">', 'html')
msg.attach(msgText)

with open(IMG_URL, 'rb') as fp:
    img = MIMEImage(fp.read())
    img.add_header('Content-Disposition', 'inline', filename=IMG_URL)
    img.add_header('Content-ID', f'<{IMG_URL}>')
    msg.attach(img)

EMAIL_MESSAGE = msg.as_string()


# Create socket and establish a TCP connection
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((MAIL_HOST, MAIL_PORT))

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')


# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')


# Start a secure TLS connection
mailFromCommand = 'STARTTLS\r\n'
clientSocket.send(mailFromCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Wrap client socket with ssl
context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname=MAIL_HOST)
print(clientSocket)


# Send EHLO command
heloCommand = 'EHLO alice\r\n'
clientSocket.send(heloCommand.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
    print('250 reply not received from server.')


# Send AUTH PLAIN command with email and password base64 encoded
base64_str = b64encode(("\x00" + USERNAME + "\x00" + PASSWORD).encode())
authMsg = "AUTH PLAIN ".encode() + base64_str + "\r\n".encode()
clientSocket.send(authMsg)
recv4 = clientSocket.recv(1024)
print(recv4.decode())
if recv4[:3] != b'235':
    print('235 reply not received from server.')


# Send MAIL FROM command and print server response.
mailFromCommand = f'MAIL FROM: <{USERNAME}>\r\n'
clientSocket.send(mailFromCommand.encode())
recv5 = clientSocket.recv(1024).decode()
print(recv5)
if recv5[:3] != '250':
    print('250 reply not received from server.')


# Send RCPT TO command and print server response.
mailToCommand = f'RCPT TO: <{MAIL_TO_ADDRESS}>\r\n'
clientSocket.send(mailToCommand.encode())
recv6 = clientSocket.recv(1024).decode()
print(recv6)
if recv6[:3] != '250':
    print('250 reply not received from server.')


# Send DATA command and print server response.
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
recv7 = clientSocket.recv(1024).decode()
print(recv7)
if recv7[:3] != '354':
    print('354 reply not received from server.')


# Send a simple text message
# clientSocket.send(EMAIL_TEXT.encode())

# Send a message with an image
for i in range(len(EMAIL_MESSAGE)):
    clientSocket.send(EMAIL_MESSAGE[i].encode())

# Message ends with a single period.
clientSocket.send(END_MESSAGE.encode())

recv8 = clientSocket.recv(1024).decode()
print(recv8)
if recv8[:3] != '250':
    print('250 reply not received from server.')


# Send QUIT command and get server response.
dataCommand = 'QUIT\r\n'
clientSocket.send(dataCommand.encode())
recv9 = clientSocket.recv(1024).decode()
print(recv9)
