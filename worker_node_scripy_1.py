import socket

# 服务端为tcp方式，客户端也采用tcp方式  默认参数即为tcp
client = socket.socket()
# 访问的服务器的ip和端口
ip_port = ('127.0.0.1', 8888)
# 连接主机
client.connect(ip_port)
# 定义发送消息循环
print("Worker Node 连接成功!")
while True:
    # 接受主机信息   每次接收缓冲区1024个字节
    data = client.recv(1024)
    # 打印接受的数据
    print(data.decode())
    msg_input = input("请输入发送的消息：")
    # msg_input = "i have slept"
    client.send(msg_input.encode())
    if msg_input != None:
        break