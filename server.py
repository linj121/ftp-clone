import sys
import os
from pathlib import Path
import socket

HOST = "127.0.0.1"
PORT = 27000


def start_server(file, port: int, host: str = ''):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server started, listening on {HOST}:{PORT}")
        print(f"Waiting for connection...")
        # accept() returns a socket object and a tuple containing the address
        # If it's ipv4, the tuple is (host, port)
        # If it's ipv6, the tuple is (host, port, flowinfo, scopeid)
        conn, addr = s.accept()
        # The with statement ensures the socket will be closed
        with conn:
            print('Connected by', addr)
            while True:
                # recv() is a blocking call
                # Blocking calls have to wait on system calls (I/O) to \
                # complete before they can return a value.
                data = conn.recv(1024)
                print(f"Received data: {data}")
                if not data:
                    break
                conn.sendall(data)
    return 0


arguments = sys.argv[1:]

if len(arguments) == 1:
    print("Number of arguments is 1 [OK]")
    file_name = arguments[0]
else:
    # throws an error and exit the script
    print(f"ERR: 1 argument expected, but {len(arguments)} given!")
    exit(0)

# if re.match(r'^[^/]+$', file_name):
#     print(f"Valid: {file_name}!")
# else:
#     print(f"File {file_name} invalid!")
#     exit(0)

file_path = Path.cwd() / 'input_file' / file_name

try:
    print(f"Checking for the existence of file {file_name} ...")
    file = open(file_path, "r")
    print(f"File {file_name} exists [OK]")
    start_server(file, PORT, HOST)
    file.close()
except FileNotFoundError:
    print(f"ERR: File {file_name} does not exist!")
    exit(0)





