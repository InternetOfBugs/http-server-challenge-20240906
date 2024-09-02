import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    conn, addr = server_socket.accept()
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
    else:
        conn.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')
    conn.close()

    server_socket.close() # close the server


if __name__ == "__main__":
    main()

