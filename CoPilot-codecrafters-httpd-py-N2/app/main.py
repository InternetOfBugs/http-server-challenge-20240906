import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    import socket
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept()  # wait for client
    
    # return 'HTTP/1.1 200 OK\r\n\r\n' to the client
    client_socket.send(b'HTTP/1.1 200 OK\r\n\r\n')
    
    # Close the client socket
    client_socket.close()



if __name__ == "__main__":
    main()
