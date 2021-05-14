import mido
from pythonosc.udp_client import SimpleUDPClient


ip_out = '127.0.0.1'
port_out = 7000
client = SimpleUDPClient(ip_out, port_out)


def convert(msb, lsb, degrees=True):
    i = (128 * msb) + lsb
    if i >= 8192:
        i -= 16384
    if degrees:
        return i * 0.02797645484
    else:
        return i * 0.00048828125


def readtracker():
    with mido.open_input('Head Tracker') as inport:
        for msg in inport:
            if msg.data[3] == 64:
                if msg.data[4] == 0:
                    y = convert(msg.data[5], msg.data[6])
                    p = convert(msg.data[7], msg.data[8])
                    r = convert(msg.data[9], msg.data[10])
                    client.send_message('/SceneRotator/ypr', [-y, p, -r])
                    # print(f'YPR: {y:7.2f} {p:7.2f} {r:7.2f}', end='\r')
                elif msg.data[4] == 1:
                    w = convert(msg.data[5], msg.data[6], False)
                    x = convert(msg.data[7], msg.data[8], False)
                    y = convert(msg.data[9], msg.data[10], False)
                    z = convert(msg.data[11], msg.data[12], False)
                    client.send_message('/SceneRotator/quaternions', [w, -y, x, -z])
                    # print(f'WXYZ: {w:7.2f} {x:7.2f} {y:7.2f} {z:7.2f}', end='\r')


if __name__ == '__main__':
    try:
        readtracker()
    except (EOFError, KeyboardInterrupt):
        print("\nBye.")
