import socket
import threading
SUM_TIME = 0
CONNECT_NUM = 0

def root_node_socket(socket, port, ip="0.0.0.0"):
    ip_port = (ip,port)
    socket.bind(ip_port)
    socket.listen(1)
    global SUM_TIME
    global CONNECT_NUM
    while True:
        print("等待连接...")
        conn, address = socket.accept()
        CONNECT_NUM += 1
        print(f"连接{CONNECT_NUM}成功")
        msg = f"连接编号:{CONNECT_NUM}"
        conn.send(msg.encode())

        while True:
            data = conn.recv(1024)
            if data is not None:
                node_time = data.decode()
                print(f"NODE:{CONNECT_NUM} \n SIMU_TIME: {node_time}")
                SUM_TIME += int(node_time)
                break
        conn.close()
        break
    
    print(SUM_TIME)

def main():
    root_socket_1 = socket.socket()
    root_socket_2 = socket.socket()
    thread1 = threading.Thread(target=root_node_socket,args=(root_socket_1,8888))
    thread2 = threading.Thread(target=root_node_socket,args=(root_socket_2,8889))
    thread1.start()
    thread2.start()

if __name__ == "__main__":
    main()