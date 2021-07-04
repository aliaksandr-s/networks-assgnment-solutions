from socket import *
import time

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 12000
MESSAGE     = 'ping'
ITERATIONS  = 10

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

rtt_list = []
lost_packets = 0

def get_average(rtt_list):
    average = sum(rtt_list) / len(rtt_list)
    return min(rtt_list), max(rtt_list), average, (lost_packets / ITERATIONS) * 100

def ping(clientSocket, rtt_list):
    global lost_packets
    try:
        start = time.time() * 1000

        clientSocket.sendto(MESSAGE.encode(), (SERVER_HOST, SERVER_PORT))
        response, _ = clientSocket.recvfrom(2048)

        end = time.time() * 1000
        rtt = end - start
        rtt_list.append(rtt)

        print(response.decode(), rtt)
    except timeout:
        lost_packets += 1
        print('Request timed out')

for i in range(ITERATIONS):
    ping(clientSocket, rtt_list)

min_rtt, max_rtt, avg, lost_percent = get_average(rtt_list)
print('\r')
print(f'min: {min_rtt}')
print(f'max: {max_rtt}')
print(f'avg: {avg}')
print(f'lost packets: {lost_percent}%')

clientSocket.close()
