import socket
import threading
import workload_input
import json
import ast
from broadcast_with_traffic_generator import broadcast_emulator
from allreduce_with_traffic_generator import allreduce_emulator


SUM_TIME = 0
CONNECT_NUM = 0


def init_distribution_phase(nodes_list, father_node, data_size, user_id, topo_id,  algorithm="tree_sync_mode"):
    init_distribution_emulator = broadcast_emulator(nodes_list, father_node, data_size, user_id, topo_id)
    if algorithm == "tree_sync_mode":
        init_time = init_distribution_emulator.tree_sync_mode()
        return init_time

def gradient_aggregation_phase(nodes_num, data_size, user_id, topo_id, circle_topo, algorithm="ring_sync_mode"):
    gradient_aggregation_emulator = allreduce_emulator(nodes_num, data_size, user_id, topo_id)
    if algorithm == "ring_sync_mode":
        aggregation_time = gradient_aggregation_emulator.ring_sync_mode(circle_topo)
        return aggregation_time
        




def main():

    wide_area_time = 0
    path = "./input.ini"
    config = workload_input.config_ini(path)

    user_id = config["user"]["user-id"]
    topo_id = config["user"]["topo-id"]

    model = config["wide_area_topo"]["model"]
    dataset = config["wide_area_topo"]["dataset"]
    dtype = config["wide_area_topo"]["dtype"]
    nodes_num = int(config["wide_area_topo"]["nodes-num"])
    circle_topo = config["wide_area_topo"]["circle-topo"]
    circle_topo = ast.literal_eval(circle_topo)

    nodes_list = config["wide_area_topo"]["nodes-list"]
    nodes_list = ast.literal_eval(nodes_list)
    father_node = config["wide_area_topo"]["father-node"]

    initial_distribution_phase = config["wide_area_topo"]["initial-distribution-phase"]
    initial_distribution_algorithm = config["wide_area_topo"]["initial-distribution-algorithm"]
    gradient_convergence_algorithm = config["wide_area_topo"]["gradient-convergence-algorithm"]

    init_dict = workload_input.model_ini(model, dataset, dtype)
    initial_distribution_phase_data_size = init_dict["model_size"] + init_dict["dataset_size"]
    gradient_convergence_phase_data_size = init_dict["model_params"] * init_dict["dtype_size"] / (1024 ** 3)

    # if initial_distribution_phase:
    #     wide_area_time += init_distribution_phase(nodes_list=nodes_list, father_node=father_node, data_size=initial_distribution_phase_data_size, user_id=user_id, topo_id=topo_id, algorithm=initial_distribution_algorithm)
    
    # wide_area_time += gradient_aggregation_phase(nodes_num=nodes_num, data_size=gradient_convergence_phase_data_size, user_id=user_id, topo_id=topo_id, circle_topo=circle_topo, algorithm=gradient_convergence_algorithm)
    print("wide_area_time:", wide_area_time)
    def root_node_socket(socket, port, ip="0.0.0.0"):
        ip_port = (ip,port)
        socket.bind(ip_port)
        socket.listen(1)
        global SUM_CIRCLE
        global CONNECT_NUM
        while True:
            print("等待连接...")
            conn, address = socket.accept()
            CONNECT_NUM += 1
            print(f"连接{CONNECT_NUM}成功")
            section_data = {key: config["node1"][key] for key in config["node1"]}
            json_data = json.dumps(section_data, indent=4)
            conn.send(json_data.encode())

            while True:
                data = conn.recv(1024)
                if data is not None:
                    simu_info_json = data.decode()
                    simu_info_dict = json.loads(simu_info_json)
                    simu_circle = simu_info_dict.get("time_info")
                    print(f"NODE:{CONNECT_NUM} \n SIMU_CIRCLE: {simu_circle}")
                    SUM_CIRCLE += int(simu_circle)
                    break
            conn.close()
            break
        print("wide_area_time: ", wide_area_time)
        print("SUM_CIRCLE: ", SUM_CIRCLE)


    for i in range(int(nodes_num)):
        exec('root_socket_{}=socket.socket()'.format(i))
        exec('thread{}=threading.Thread(target=root_node_socket,args=(root_socket_{},{}))'.format(i, i, 8888+i))
        exec('thread{}.start()'.format(i))


    global SUM_TIME
    SUM_TIME += wide_area_time
    FINAL_TIME = SUM_TIME
    return FINAL_TIME

if __name__ == "__main__":
    FINAL_TIME = main()
    print(f"整体训练时间为: {FINAL_TIME}")