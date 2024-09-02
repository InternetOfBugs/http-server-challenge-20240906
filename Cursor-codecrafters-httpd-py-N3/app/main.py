import socket  # noqa: F401
import re

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:
        client_socket, client_address = server_socket.accept()
        
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
        else:
            response = b'HTTP/1.1 404 Not Found\r\n\r\n'

        # Send the response to the client
        client_socket.sendall(response)
        client_socket.close()

if __name__ == "__main__":
    main()
