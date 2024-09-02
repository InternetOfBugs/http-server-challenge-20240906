import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    request_str = request.decode()
    if request_str.startswith("GET /echo/"):
        response_str = request_str[12:request_str.find(" ", 12)]
        conn.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response_str)}\r\n\r\n{response_str}".encode())
    else:
        conn.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')
    conn.close()


if __name__ == "__main__":
    main()
