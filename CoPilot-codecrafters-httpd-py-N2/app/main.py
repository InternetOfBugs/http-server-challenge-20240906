import os

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    request_lines = request.split('\n')
    path = request_lines[0].split()[1]  # Extract the path from the request

    if path.startswith('/files/'):
        filename = path.split('/')[2]
        file_path = os.path.join('/tmp', filename)

        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_contents = file.read()

            response_body = file_contents

            # Set the headers
            headers = [
                b'HTTP/1.1 200 OK',
                b'Content-Type: application/octet-stream',
                b'Content-Length: ' + str(len(response_body)).encode(),
                b'',
                response_body
            ]

            # Send the response
            client_socket.send(b'\r\n'.join(headers))
        else:
            client_socket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
    elif path == '/user-agent':
        # Rest of the code...
    elif path.startswith('/echo/'):
        # Rest of the code...
    elif path == '/':
        # Rest of the code...
    else:
        client_socket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')

    # Close the client socket
    client_socket.close()
