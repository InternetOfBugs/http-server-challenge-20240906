import os
import socket
import threading


def handle_request(conn, addr, files_dir):
    request = conn.recv(1024)
    if request.startswith(b"GET / "):
        conn.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
    elif b"GET /echo/" in request:
        string = request.split()[1].split(b"/echo/")[1]
        conn.sendall(b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: ' + bytes(str(len(string)), 'utf-8') + b'\r\n\r\n' + string)
    elif b"GET /user-agent" in request:
        headers = request.split(b"\r\n")
        for header in headers:
            if header.startswith(b"User-Agent:"):
                user_agent = header.split(b": ", 1)[1]
                conn.sendall(b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: ' + bytes(str(len(user_agent)), 'utf-8') + b'\r\n\r\n' + user_agent)
    elif b"GET /files/" in request:
        filename = request.split()[1].split(b"/files/")[1]
        if os.path.isfile(os.path.join(files_dir, filename)):
            with open(os.path.join(files_dir, filename), 'rb') as f:
                file_contents = f.read()
            conn.sendall(b'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: ' + bytes(str(len(file_contents)), 'utf-8') + b'\r\n\r\n' + file_contents)
        else:
            conn.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')
    else:
        conn.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')
    conn.close()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory")
    args = parser.parse_args()

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        conn, addr = server_socket.accept()
        t = threading.Thread(target=handle_request, args=(conn, addr, args.directory))
        t.start()

    server_socket.close() # close the server


if __name__ == "__main__":
    main()

