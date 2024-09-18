import socket  # noqa: F401
import threading
import os
import argparse
from urllib.parse import unquote

def handle_client(client_connection, client_address, directory=None):
    # Handle the client connection
    with client_connection:
        try:
            # Read the request until the end of headers (\r\n\r\n)
            request_data = b""
            while True:
                chunk = client_connection.recv(1024)
                if not chunk:
                    break  # No more data from client
                request_data += chunk
                if b"\r\n\r\n" in request_data:
                    break  # End of headers

            # Decode the request from bytes to string
            request_str = request_data.decode('utf-8', errors='replace')
            # Split the request into lines
            request_lines = request_str.split('\r\n')
            # Get the request line (first line)
            request_line = request_lines[0]
            # Split the request line into its components
            request_parts = request_line.split(' ')
            if len(request_parts) >= 2:
                method, path = request_parts[0], request_parts[1]
                # Initialize headers dictionary
                headers = {}
                # Process the headers
                for header_line in request_lines[1:]:
                    if header_line == '':
                        break  # End of headers
                    header_parts = header_line.split(':', 1)
                    if len(header_parts) == 2:
                        header_name = header_parts[0].strip().lower()
                        header_value = header_parts[1].strip()
                        headers[header_name] = header_value
                # Check the path
                if path == '/':
                    response = b"HTTP/1.1 200 OK\r\n\r\n"
                elif path.startswith('/echo/'):
                    # Extract the string after '/echo/'
                    echo_str = path[len('/echo/'):]
                    # URL-decode the string
                    echo_str = unquote(echo_str)
                    # Encode the response body
                    response_body = echo_str.encode('utf-8')
                    content_length = len(response_body)
                    # Prepare headers
                    response_headers = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/plain\r\n"
                        f"Content-Length: {content_length}\r\n"
                        "\r\n"
                    )
                    response = response_headers.encode('utf-8') + response_body
                elif path == '/user-agent':
                    # Get the User-Agent header
                    user_agent = headers.get('user-agent', '')
                    # Encode the response body
                    response_body = user_agent.encode('utf-8')
                    content_length = len(response_body)
                    # Prepare headers
                    response_headers = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/plain\r\n"
                        f"Content-Length: {content_length}\r\n"
                        "\r\n"
                    )
                    response = response_headers.encode('utf-8') + response_body
                elif directory and path.startswith('/files/'):
                    # Extract the filename
                    filename = path[len('/files/'):]
                    # URL-decode the filename
                    filename = unquote(filename)
                    # Normalize the filename to prevent directory traversal attacks
                    filename = os.path.normpath(filename)
                    # Prevent access to parent directories
                    if filename.startswith('../') or '/../' in filename or filename.startswith('/'):
                        # Invalid filename
                        response = b"HTTP/1.1 403 Forbidden\r\n\r\n"
                    else:
                        # Construct the full file path
                        directory_abs = os.path.abspath(directory)
                        full_file_path = os.path.abspath(os.path.join(directory_abs, filename))
                        # Ensure that the full file path is within the directory
                        if not full_file_path.startswith(directory_abs + os.sep) and full_file_path != directory_abs:
                            # The file is outside the directory
                            response = b"HTTP/1.1 403 Forbidden\r\n\r\n"
                        else:
                            # Check if the file exists
                            if os.path.isfile(full_file_path):
                                # Read the file contents
                                with open(full_file_path, 'rb') as f:
                                    file_contents = f.read()
                                content_length = len(file_contents)
                                # Prepare headers
                                response_headers = (
                                    "HTTP/1.1 200 OK\r\n"
                                    "Content-Type: application/octet-stream\r\n"
                                    f"Content-Length: {content_length}\r\n"
                                    "\r\n"
                                )
                                response = response_headers.encode('utf-8') + file_contents
                            else:
                                # File not found
                                response = b"HTTP/1.1 404 Not Found\r\n\r\n"
                elif path.startswith('/files/'):
                    # directory not provided, cannot serve files
                    response = b"HTTP/1.1 404 Not Found\r\n\r\n"
                else:
                    response = b"HTTP/1.1 404 Not Found\r\n\r\n"
            else:
                # Malformed request
                response = b"HTTP/1.1 400 Bad Request\r\n\r\n"
            # Send the HTTP response
            client_connection.sendall(response)
        except Exception as e:
            # In case of any exception, send 500 Internal Server Error
            error_response = b"HTTP/1.1 500 Internal Server Error\r\n\r\n"
            client_connection.sendall(error_response)
        finally:
            # Close the connection
            client_connection.close()

def main():
    import argparse
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Simple HTTP Server')
    parser.add_argument('--directory', help='Directory where the files are stored')
    args = parser.parse_args()

    directory = args.directory

    # You can use print statements as follows; they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_connection, client_address = server_socket.accept()
        # Start a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_connection, client_address, directory))
        client_thread.start()

if __name__ == "__main__":
    main()


