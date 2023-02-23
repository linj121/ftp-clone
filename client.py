import socket
import sys
from pathlib import Path
import re
import errno


def start_client(host: str, port: int, handle_data, **kwargs) -> str:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        # s.sendall(b"Hello World")
        kwargs["data"] = s.recv(1024).decode()
        print("Connection closed")
    handle_data(**kwargs)


def parse_addr(address: str) -> tuple:
    # ipv4 addr OR hostname validation, port number between 49152 - 65535
    if match := re.match(r"^([a-zA-Z0-9\-\.]+):(\d{1,5})$", address):
        input_host = match.group(1)
        input_port = int(match.group(2))
        ipv4_hostname_regex = \
            r"^((?:(?:[a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*(?:[A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9]))$|"\
            r"^((?:(?:25[0-5]|(?:2[0-4]|1\d|[1-9]|)\d)\.?\b){4})$"
        if r := re.match(ipv4_hostname_regex, input_host):
            host = r.group(2) if r.group(2) is not None else socket.gethostbyname(r.group(1))
        else:
            print(f"ERR: Invalid host: {input_port}")
            exit(0)
        if 49152 <= int(input_port) <= 65535:
            port = input_port
        else:
            print(f"ERR: Invalid port number: {input_port}")
            exit(0)
        return host, port
    else:
        print(f"ERR: Invalid server address: {address}")
        exit(0)


def write_to_file(path: str, data: str):

    try:
        with open(path, "w") as output:
            output.write(data)
        print(f"Data written to: {path}")
    except IOError as x:
        print('error ', x.errno, ',', x.strerror)
        if x.errno == errno.EACCES:
            print(path, 'no permissions')
        elif x.errno == errno.EISDIR:
            print(path, 'is directory')


if __name__ == "__main__":

    HOST: str = ""
    PORT: int
    FILE_PATH: Path

    arguments = sys.argv[1:]
    if len(arguments) == 2:
        print("Number of arguments is 2 [OK]")
        HOST, PORT = parse_addr(arguments[0])
        print(f"Provided HOST: {HOST}, PORT: {PORT} [OK]")
        FILE_PATH = Path.cwd() / 'output_file' / arguments[1]
    else:
        print(f"ERR: 2 argument expected, but {len(arguments)} given!")
        exit(0)

    if FILE_PATH.is_file():
        start_client(HOST, PORT, write_to_file, path=FILE_PATH)
    else:
        print(f"ERR: File {FILE_PATH} doesn't exist")
        exit(0)

