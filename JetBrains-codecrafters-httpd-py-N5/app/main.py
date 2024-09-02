import socket  # noqa: F401

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, _ = server_socket.accept()  # wait for client

    try:
        data = client_socket.recv(1024).decode("utf-8")
        request_line = data.split("\n")[0]
        url = request_line.split(" ")[1]
        if url == "/":
            client_socket.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
        else:
            client_socket.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')
    except Exception as e:
        print(e)
    finally:
        client_socket.close()




if __name__ == "__main__":
    main()
