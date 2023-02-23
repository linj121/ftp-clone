import sys
import threading
from pathlib import Path
import socket

HOST: str = socket.gethostbyname("localhost")
PORT: int = 50000


def get_data_if_valid(file_path: Path) -> str:
    try:
        print(f"Checking for the existence of file {file_path} ...")
        with open(file_path, "r") as input_file:
            print(f"File {file_path} exists [OK]")
            content = input_file.read()
            if len(content) <= 80:
                return content
            else:
                print(f"ERR: number of char exceeds 80, {len(content)} given")
                exit(0)
    except FileNotFoundError:
        print(f"ERR: File {file_path} does not exist!")
        exit(0)


def on_new_client(client_socket: socket, addr: tuple, data: str):
    with client_socket as s:
        s.sendall(data.encode())
        print(f"Data successfully sent to {addr} [OK]")


def start_server(host: str, port: int, data: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server started, listening on {host}:{port}")
        while True:
            print(f"Waiting for connection...")
            conn = None
            try:
                # s.accept(): tuple -> (socket, (host, port))
                conn, addr = s.accept()
                print(f"Connected from {addr}")
                thread = threading.Thread(target=on_new_client, args=(conn, addr, data))
                thread.start()
            except KeyboardInterrupt:
                if conn:
                    conn.close()
                break


if __name__ == "__main__":

    arguments = sys.argv[1:]
    if len(arguments) == 1:
        print("Number of arguments is 1 [OK]")
        FILE_PATH = Path.cwd() / 'input_file' / arguments[0]

    else:
        print(f"ERR: 1 argument expected, but {len(arguments)} given!")
        exit(0)

    DATA = get_data_if_valid(FILE_PATH)

    start_server(HOST, PORT, DATA)
