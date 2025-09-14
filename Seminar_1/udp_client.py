import socket as sk
 
HOST = '0.0.0.0'
PORT = 2001
 
s = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
s.bind((HOST, PORT))
while 1:
    payload, client_address = s.recvfrom(65536)
    print('Received:', payload)
    sent = s.sendto(payload, client_address)