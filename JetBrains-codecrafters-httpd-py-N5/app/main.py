import socket  # noqa: F401


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    client_socket, _ = server_socket.accept()  # wait for client
    try:
        data = client_socket.recv(1024).decode("utf-8")
        request_line, headers_str = data.split("\r\n\r\n", 1)
        url = request_line.split(" ")[1]
        headers = headers_str.split("\r\n")
        headers_dict = {h.split(": ")[0]: h.split(": ")[1] for h in headers if ': ' in h}

        user_agent = headers_dict.get("User-Agent")

        print(request_line)
        print(headers_dict)

        if url == "/user-agent" and user_agent:
            response_body = user_agent
            response_headers = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n\r\n"
            client_socket.sendall((response_headers + response_body).encode())

        elif url.startswith("/echo/"):
            response_body = url.split("/echo/")[1]
            response_headers = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n\r\n"
            client_socket.sendall((response_headers + response_body).encode())

        elif url == "/":
            client_socket.sendall(b'HTTP/1.1 200 OK\r\n\r\n')

        else:
            client_socket.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')
    except Exception as e:
        print(e)
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
