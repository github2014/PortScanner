"""
Port Scanners are primarily used for Penetration Testing and Information Gathering.

A port scanner tries to connect to an IP-Address on a certain port.
Usually, when we surf the web, we connect to servers via port 80 (HTTP) or port 443 (HTTPS).
But there are also a lot of other crucial ports like 21 (FTP), 22 (SSH), 25 (SMTP) and many more.
In fact, there are more than 130,000 ports of which 1,023 are standardized and 48,128 reserved.

To get open ports on windows use "netstat -aon"
"""
import socket
import threading
from queue import Queue

targetIpAddress = "127.0.0.1"
port_list = range(1, 1024)


def portscan(port):
    try:
        # INET = socket is Internet socket and not UNIX
        # SOCK_STREAM = using TCP instead of UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((targetIpAddress, port))
        return True                          # If now errors returned, connection successful - open port found
    except Exception as e:
        #print(e)                            # Every port that can't be connected to returns "[WinError 10061] No connection could be made because the target machine actively refused it"
        return False


queue = Queue()


def fill_queue(port_list):
    for port in port_list:
        queue.put(port)


open_ports = []


def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print("Port {} is open".format(port))
            open_ports.append(port)


fill_queue(port_list)

thread_list = []
# Create 1000 new threads
for t in range(1000):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

# Start threads
for thread in thread_list:
    thread.start()

# Wait till all threads are finished
for thread in thread_list:
    thread.join()

print("Open ports are: ", open_ports)
