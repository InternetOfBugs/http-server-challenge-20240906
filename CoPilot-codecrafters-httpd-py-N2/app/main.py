import socket
import threading
import os

def handle_files_request(path):
    # Extract the filename from the path
    filename = path.split('/')[2]

    # Check if the file exists
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        # Read the file contents
        with open(file_path, 'rb') as file:
            file_contents = file.read()

        # Set the headers
        headers = [
            b'HTTP/1.1 200 OK',
            b'Content-Type: application/octet-stream',
            b'Content-Length: ' + str(len(file_contents)).encode(),
            b'',
            file_contents
        ]

        # Send the response
        client_socket.send(b'\r\n'.join(headers))
    else:
        client_socket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')


def handle_client(client_socket):
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
     # Inside the handle_client function
    elif path.startswith('/files/'):
        handle_files_request(path)
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
        client_socket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')

    # Close the client socket
    client_socket.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket, client_address = server_socket.accept()  # wait for client
        print("Client Address:", client_address)

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()
