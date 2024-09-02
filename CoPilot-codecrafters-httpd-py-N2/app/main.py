import socket

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept()  # wait for client
    
    if client_address[1] == 4221:
        request = client_socket.recv(1024).decode()
        request_lines = request.split('\n')
        path = request_lines[0].split()[1]  # Extract the path from the request
        if path == '/':
            client_socket.send(b'HTTP/1.1 200 OK\r\n\r\n')
        else:
            client_socket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
    else:
        client_socket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
    
    # Close the client socket
    client_socket.close()



if __name__ == "__main__":
    main()
