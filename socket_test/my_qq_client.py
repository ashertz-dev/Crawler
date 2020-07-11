import socket
import json
import threading


def handle_receive():
    while True:
        if not exit:
            try:
                res = client.recv(1024)
            except:
                break
            res = res.decode("utf-8")
            try:
                res_json = json.loads(res)
                msg = res_json["data"]
                from_user = res_json["from"]
                print("收到来自 {} 的消息 {}".format(from_user, msg))
            except:
                print(res)


def handle_send():
    while True:
        # 随时可以发消息
        # 有新消息可以随时收到
        op_type = input("请输入你要进行的操作:\n1. 发送消息\n2. 获取在线用户\n3. 退出\n")
        if op_type not in ["1", "2", "3"]:
            print("不支持该操作")
            op_type = input("请输入你要进行的操作:\n1. 发送消息\n2. 获取在线用户\n3. 退出\n")

        elif op_type == "1":
            to_user = input("请输入你要发送的用户:\n")
            msg = input("请输入你要发送的消息:\n")
            send_data_template = {
                "action": "send_msg",
                "to": to_user,
                "from": user,
                "data": msg
            }
            client.send(json.dumps(send_data_template).encode("utf-8"))

        elif op_type == "2":
            client.send(json.dumps(get_user_template).encode("utf-8"))

        elif op_type == "3":
            exit_template = {
                "action": "exit",
                "user": user
            }
            client.send(json.dumps(exit_template).encode("utf-8"))
            exit = True
            client.close()
            break


if __name__ == '__main__':
    exit = False
    client = socket.socket()
    client.connect(("127.0.0.1", 8000))
    user = "Hypnos"
    # 登陆
    login_temp = {
        "action": "login",
        "user": user
    }
    client.send(json.dumps(login_temp).encode("utf-8"))
    res = client.recv(1024)
    print(res.decode("utf-8"))
    # 获取在线用户
    get_user_template = {
        "action": "list_user"
    }
    client.send(json.dumps(login_temp).encode("utf-8"))
    res = client.recv(1024)
    print("当前在线用户: {}".format(res.decode("utf-8")))
    # 获取历史消息
    offline_msg_template = {
        "action": "history_msg",
        "user": user
    }
    client.send(json.dumps(login_temp).encode("utf-8"))
    res = client.recv(1024)
    print("历史消息: {}".format(res.decode("utf-8")))

    send_thread = threading.Thread(target=handle_send)
    receive_thread = threading.Thread(target=handle_receive)
    send_thread.start()
    receive_thread.start()
