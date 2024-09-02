import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept()  # wait for client

    # Parse the request to get the path
    request = client_socket.recv(1024).decode('utf-8')
    request_line = request.split('\n')[0]
    path = request_line.split()[1]

    # Prepare the response based on the path
    if path == '/':
        response = b'HTTP/1.1 200 OK\r\n\r\n'
    else:
        response = b'HTTP/1.1 404 Not Found\r\n\r\n'

    # Send the response to the client
    client_socket.sendall(response)
    client_socket.close()
    server_socket.close()
    
if __name__ == "__main__":
    main()
