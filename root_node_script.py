import socket
import threading
import workload_input
import json
import ast
from broadcast_with_traffic_generator import broadcast_emulator
from allreduce_with_traffic_generator import allreduce_emulator

CONNECT_NUM = 0

def main():
    
    path = "./input.ini"

    config = workload_input.config_ini(path)


    port_list = config["wide-area-topo"]["port-list"]
    port_list = ast.literal_eval(port_list)

    nodes_num = config["server-control"]["nodes-num"]

    nodes_list = config["server-control"]["nodes-list"]
    nodes_list = ast.literal_eval(nodes_list)

    # 从ini文件中提取信息
    
    def root_node_socket(socket, port, ip="0.0.0.0"):
        ip_port = (ip,port)
        socket.bind(ip_port)
        socket.listen(1)
        global CONNECT_NUM
        while True:
            # 等待连接
            print("waiting connection...")
            conn, address = socket.accept()
            CONNECT_NUM += 1
            node_name = f"node{CONNECT_NUM}"
            print(f"successfully connect to {CONNECT_NUM}!")
            section_data = {key: config[node_name][key] for key in config[node_name]}
            json_data = json.dumps(section_data, indent=4)
            conn.send(json_data.encode())
            # 分发配置文件给worker_node

            while True:
                data = conn.recv(1024)
                if data is not None:
                    status_code = data.decode()
                    print("STATUS_CODE:", status_code)
                    break
            conn.close()
            break


    for i in range(int(nodes_num)):
        exec('root_socket_{}=socket.socket()'.format(i))
        exec('thread{}=threading.Thread(target=root_node_socket,args=(root_socket_{},{}))'.format(i, i, int(port_list[i])))
        exec('thread{}.start()'.format(i))


    return "ROOT NODE SUCCESSFULLY EXECUTE!"
    

if __name__ == "__main__":
    FINAL_RES = main()
    print(FINAL_RES)
    
