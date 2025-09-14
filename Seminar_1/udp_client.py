import socket as sk
import time

HOST = '158.174.211.54'
PORT = 2001

COUNT   = 300     # number of messages
SIZE    = 64      # payload bytes
TIMEOUT = 1.0     # seconds

s = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
s.settimeout(TIMEOUT)

payload = b'x' * SIZE
rtts = []
sent = 0
received = 0
i = 0

while i < COUNT:
    i += 1
    t0 = time.perf_counter()
    s.sendto(payload, (HOST, PORT))
    sent += 1
    try:
        data, _ = s.recvfrom(65536)
        rtt_ms = (time.perf_counter() - t0) * 1000.0
        rtts.append(rtt_ms)
        received += 1
        print(i ,'Received:', len(data), 'bytes, RTT', f'{rtt_ms:.3f} ms')
    except sk.timeout:
        print('timeout')

s.close()

print('\nsummary:')
print('sent=', sent, 'received=', received, 'loss=', f'{(sent - received) * 100.0 / sent:.1f}%')

mn = min(rtts)
avg = sum(rtts) / len(rtts)
mx = max(rtts)
print('min/avg/max:', f'{mn:.3f}/{avg:.3f}/{mx:.3f}', 'ms')
