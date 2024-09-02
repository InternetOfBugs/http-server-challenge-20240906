import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    conn, addr = server_socket.accept()
    request = conn.recv(1024)
    if b"GET /" in request:
        conn.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
    else:
        conn.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')
    conn.close()

    server_socket.close() # close the server


if __name__ == "__main__":
    main()
