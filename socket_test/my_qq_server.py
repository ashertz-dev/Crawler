import socket
import json
from collections import defaultdict
import threading


def handle_sock(_sock, _addr):
    while True:
        data = _sock.recv(1024)
        json_data = json.loads(data.decode("utf-8"))
        action = json_data.get("action", "")
        if action == "login":
            online_users[json_data["user"]] = _sock
            _sock.send("登陆成功".encode("utf-8"))
        elif action == "list_user":
            all_users = [user for user, sock_ip in online_users.items()]
            _sock.send(json.dumps(all_users).encode("utf-8"))
        elif action == "history_msg":
            _sock.send(json.dumps(user_msgs.get(json_data["user"], [])).encode("utf-8"))
        elif action == "send_msg":
            if json_data["to"] in online_users:
                online_users[json_data["to"]].send(json.dumps(json_data).encode("utf-8"))
            user_msgs[json_data["to"]].append(json_data)
        elif action == "exit":
            del online_users[json_data["user"]]
            _sock.send("退出成功!".encode("utf-8"))


if __name__ == '__main__':
    # 维护用户连接
    online_users = defaultdict(dict)
    # 维护用户的历史消息
    user_msgs = defaultdict(list)
    server = socket.socket()
    server.bind(("0.0.0.0", 8000))
    server.listen()
    while True:
        sock, addr = server.accept()
        # 阻塞等待连接
        client_thread = threading.Thread(target=handle_sock, args=(sock, addr))
        client_thread.start()
