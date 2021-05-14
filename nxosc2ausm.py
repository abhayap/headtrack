from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient


ip_in = '127.0.0.1'
port_in = 8000
ip_out = '127.0.0.1'
port_out = 2346

num_clients = 10
clients = []

for idx in range(num_clients):
    clients.append(SimpleUDPClient(ip_out, port_out + idx))


def default_handler(address, *argv): 
    print(f'YPR: {-argv[1]:7.2f} {argv[0]:7.2f} {-argv[2]:7.2f}', end='\r')
    for client in clients:
        client.send_message('/trackingdata/yawpitchroll', [-argv[1], argv[0], -argv[2]])


dispatcher = Dispatcher()
dispatcher.map("/nxosc/xyz", default_handler)
print(f"Sending to {ip_out}:{port_out}-{port_out+num_clients-1}, use CTRL+C to stop")
server = BlockingOSCUDPServer((ip_in, port_in), dispatcher)
server.serve_forever()  # Blocks forever
