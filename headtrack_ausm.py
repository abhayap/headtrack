import mido
from pythonosc.udp_client import SimpleUDPClient


ip_out = '127.0.0.1'
port_out = range(2346, 2356)  # ports 2346-2355

clients = []
for port in port_out:
    clients.append(SimpleUDPClient(ip_out, port))


def convert(msb, lsb):
    i = (128 * msb) + lsb
    if i >= 8192:
        i -= 16384
    return i * 0.02797645484


def readtracker():
    with mido.open_input('Head Tracker') as inport:
        for msg in inport:
            if msg.data[3] == 64 and msg.data[4] == 0:
                y = convert(msg.data[5], msg.data[6])
                p = convert(msg.data[7], msg.data[8])
                r = convert(msg.data[9], msg.data[10])
                for client in clients:
                    client.send_message('/trackingdata/yawpitchroll', [-y, p, r])
                # print(f'YPR: {y:7.2f} {p:7.2f} {r:7.2f}', end='\r')


if __name__ == '__main__':
    try:
        readtracker()
    except (EOFError, KeyboardInterrupt):
        print("\nBye.")
