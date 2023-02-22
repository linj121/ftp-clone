import socket
import sys
from pathlib import Path
import re
import errno

HOST: str = ""
PORT: int


def start_client(host: str, port: int) -> str:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        # s.sendall(b"Hello World")
        file_data = s.recv(1024).decode()

    print(f"Received:\n{file_data!r}\nEOF")

    return file_data


arguments = sys.argv[1:]

if len(arguments) == 2:
    print("Number of arguments is 2 [OK]")
    address = arguments[0]
    # ipv4 addr OR hostname validation, port number between 49152 - 65535
    if match := re.match(r"^([a-zA-Z0-9\-\.]+)(?::(\d{1,5}))$", address):
        HOST = match.group(1)
        PORT = int(match.group(2))
        print(f"Provided with HOST: {HOST}, and PORT: {PORT}")
        ipv4_hostname_regex = r"^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$ \
                               |^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$"
        if not re.match(ipv4_hostname_regex, HOST):
            print(f"ERR: Invalid host: {HOST}")
        elif not 49152 <= int(PORT) <= 65535:
            print(f"ERR: Invalid port number: {PORT}")
    else:
        print(f"ERR: Invalid server address: {address}")
        exit(0)
    file_name = arguments[1]
    file_path = Path.cwd() / 'output_file' / file_name
else:
    print(f"ERR: 2 argument expected, but {len(arguments)} given!")
    exit(0)

data = start_client(HOST, PORT)

try:
    with open(file_path, "w") as output:
        output.write(data)
except IOError as x:
    print('error ', x.errno, ',', x.strerror)
    if x.errno == errno.EACCES:
        print(file_path, 'no permissions')
    elif x.errno == errno.EISDIR:
        print(file_path, 'is directory')

