import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.accept() # wait for client

    # return 'HTTP/1.1 200 OK\r\n\r\n' to the client
    server_socket.sendall(b'HTTP/1.1 200 OK\r\n\r\n')

    server_socket.close() # close the server


if __name__ == "__main__":
    main()
