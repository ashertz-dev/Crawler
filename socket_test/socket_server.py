import socket
import threading


def handle_sock(_sock, _addr):
    # _sock.send("Welcome Server!".encode("utf-8"))
    while True:
        # temp_data方法是阻塞的
        temp_data = _sock.recv(1024)
        print(temp_data.decode("utf-8"))
        input_data = input()
        _sock.send(input_data.encode("utf-8"))
        if input_data.endswith("#"):
            sock.close()


if __name__ == '__main__':
    server = socket.socket()
    # 绑定到0.0.0.0:8000端口上
    server.bind(("0.0.0.0", 8000))
    server.listen()
    while True:
        # 阻塞等待连接
        sock, addr = server.accept()
        # 启动一个线程去处理新的用户连接
        client_thread = threading.Thread(target=handle_sock, args=(sock, addr))
        client_thread.start()
