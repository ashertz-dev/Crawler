import socket

client = socket.socket()
client.connect(("192.168.1.2", 8000))
# server_data = client.recv(1024)
# print("server response : {}".format(server_data.decode("utf-8")))
while True:
    input_data = input()
    client.send(input_data.encode("utf-8"))
    server_data = client.recv(1024)
    print("server response : {}".format(server_data.decode("utf-8")))
    if input_data.endswith("#"):
        break
client.close()
