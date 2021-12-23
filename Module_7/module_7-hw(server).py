import socket


def start_server():
    host = socket.gethostname()
    port = 8080
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    conn, addr = server_socket.accept()
    print("Connected from: ", addr)

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("From client: ", str(data))
        data = input("Type your text:\n")
        conn.send(data.encode())

    conn.close()


if __name__ == '__main__':
    start_server()
