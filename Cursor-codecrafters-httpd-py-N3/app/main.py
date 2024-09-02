import socket  # noqa: F401
import re
import threading
import os
import sys

directory = None

def handle_client(client_socket):
    # Parse the request to get the path and headers
    request = client_socket.recv(1024).decode('utf-8')
    request_lines = request.split('\r\n')
    request_line = request_lines[0]
    path = request_line.split()[1]

    # Extract User-Agent header
    user_agent = ''
    for line in request_lines[1:]:
        if line.lower().startswith('user-agent:'):
            user_agent = line.split(':', 1)[1].strip()
            break

    # Prepare the response based on the path
    if path == '/':
        response = b'HTTP/1.1 200 OK\r\n\r\n'
    elif path.startswith('/echo/'):
        echo_str = path[6:]  # Extract the string after '/echo/'
        content = echo_str.encode('utf-8')
        response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n'.encode('utf-8') + content
    elif path == '/user-agent':
        content = user_agent.encode('utf-8')
        response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n'.encode('utf-8') + content
    elif path.startswith('/files/'):
        filename = path[7:]  # Extract the filename after '/files/'
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                content = file.read()
            response = f'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n'.encode('utf-8') + content
        else:
            response = b'HTTP/1.1 404 Not Found\r\n\r\n'
    else:
        response = b'HTTP/1.1 404 Not Found\r\n\r\n'

    # Send the response to the client
    client_socket.sendall(response)
    client_socket.close()

def main():
    global directory
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Parse command line arguments
    if len(sys.argv) > 2 and sys.argv[1] == '--directory':
        directory = sys.argv[2]

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()
