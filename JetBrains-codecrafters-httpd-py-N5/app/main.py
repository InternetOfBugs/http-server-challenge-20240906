import socket  # noqa: F401
import threading
import os
from argparse import ArgumentParser

parser = ArgumentParser(description='A simple HTTP server')
parser.add_argument('--directory', type=str, help='Directory for file storage')
args = parser.parse_args()

FILES_DIR = args.directory


def handle_client(client_socket):
    try:
        data = client_socket.recv(1024).decode("utf-8")
        request_line, rest = data.split("\r\n", 1)
        url = request_line.split(" ")[1]

        headers_str, _ = rest.split("\r\n\r\n", 1)
        headers = headers_str.split("\r\n")
        headers_dict = {h.split(": ")[0]: h.split(": ")[1] for h in headers if ': ' in h}

        user_agent = headers_dict.get("User-Agent")

        print(f"request_line: {request_line}")
        print(f"headers_str: {headers_str}")
        print(f"headers_dict: {headers_dict}")

        if url == "/user-agent" and user_agent:
            response_body = user_agent
            response_headers = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n\r\n"
            client_socket.sendall((response_headers + response_body).encode())

        elif url.startswith("/echo/"):
            response_body = url.split("/echo/")[1]
            response_headers = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n\r\n"
            client_socket.sendall((response_headers + response_body).encode())

        elif url.startswith("/files/"):
            path = os.path.join(FILES_DIR, url.split("/files/")[1])
            if os.path.isfile(path):
                with open(path, "rb") as file:
                    response_body = file.read()
                response_headers = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(response_body)}\r\n\r\n"
                client_socket.sendall(response_headers.encode() + response_body)
            else:
                client_socket.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')

        elif url == "/":
            client_socket.sendall(b'HTTP/1.1 200 OK\r\n\r\n')

        else:
            client_socket.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')
    except Exception as e:
        print(e)
    finally:
        client_socket.close()


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket, _ = server_socket.accept()  # wait for client
        threading.Thread(target=handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    main()
