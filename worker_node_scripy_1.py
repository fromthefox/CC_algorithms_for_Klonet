import socket
import json

def astra_sim_api(config=0):
    """
    这里写Astra-Sim的调用Api, 参数就是ini文件中给的参数, 返回值就是时间即可.
    """
    return 30

def worker_node_socket(socket, ip, port):
    ip_port = (ip, port)
    socket.connect(ip_port)
    print("Worker Node 连接成功!")
    while True:
        data = socket.recv(1024).decode()
        data_dict = json.loads(data)
        print(type(data_dict))
        print(data_dict)
        as_simu_time = astra_sim_api()
        socket.send(str(as_simu_time).encode())
        if as_simu_time != None:
            break

def main():
    client = socket.socket()
    worker_node_socket(socket=client, ip = "127.0.0.1", port = 8889)

if __name__ == "__main__":
    main()