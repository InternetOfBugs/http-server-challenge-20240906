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

    if path == '/user-agent':
        # Read the User-Agent header
        user_agent = None
        for line in request_lines:
            if line.startswith('User-Agent:'):
                user_agent = line.split(':')[1].strip()
                break

        if user_agent:
            response_body = user_agent.encode()

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
            client_socket.send(b'HTTP/1.1 400 Bad Request\r\n\r\n')
    elif path.startswith('/echo/'):
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
    elif path == '/':
        response_body = b'Hello, World!'

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
        # Echo the request back to the client
        response_body = request.encode()

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

    # Close the client socket
    client_socket.close()


if __name__ == "__main__":
    main()
