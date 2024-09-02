import socket

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept()  # wait for client
    print("Client Address:", client_address)

    request = client_socket.recv(1024).decode()
    request_lines = request.split('\n')
    path = request_lines[0].split()[1]  # Extract the path from the request

    if path.startswith('/echo/'):
        # Extract the string from the path
        string = path.split('/')[2]
        response_body = string.encode()

        # Set the headers
        headers = [
            b'HTTP/1.1 200 OK',
            b'Content-Type: text/plain',
            b'Content-Length: ' + str(len(response_body)).encode(),
            b'',
            response_body
        ]

        # Send the response
        client_socket.send(b'\r\n'.join(headers))
    else:
        client_socket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')

    # Close the client socket
    client_socket.close()



if __name__ == "__main__":
    main()
