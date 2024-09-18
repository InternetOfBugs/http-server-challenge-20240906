
import socket  # noqa: F401

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_connection, client_address = server_socket.accept()
        with client_connection:
            # Read the request (you can ignore the content)
            request = client_connection.recv(1024)
            # Prepare the HTTP response
            response = b"HTTP/1.1 200 OK\r\n\r\n"
            # Send the HTTP response
            client_connection.sendall(response)
            # Close the connection
            client_connection.close()

if __name__ == "__main__":
    main()

