import socket  # noqa: F401

def main():
    # You can use print statements as follows; they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_connection, client_address = server_socket.accept()
        with client_connection:
            # Read the request
            request = client_connection.recv(1024)
            # Decode the request from bytes to string
            request_str = request.decode('utf-8')
            # Split the request into lines
            request_lines = request_str.split('\r\n')
            # Get the request line (first line)
            request_line = request_lines[0]
            # Split the request line into its components
            request_parts = request_line.split(' ')
            if len(request_parts) >= 2:
                method, path = request_parts[0], request_parts[1]
                # Check the path
                if path == '/':
                    response = b"HTTP/1.1 200 OK\r\n\r\n"
                else:
                    response = b"HTTP/1.1 404 Not Found\r\n\r\n"
            else:
                # Malformed request
                response = b"HTTP/1.1 400 Bad Request\r\n\r\n"
            # Send the HTTP response
            client_connection.sendall(response)
            # Close the connection
            client_connection.close()

if __name__ == "__main__":
    main()


