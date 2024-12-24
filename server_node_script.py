"""
该脚本运行于服务器
"""
import workload_input
from allreduce_with_traffic_generator import allreduce_emulator
from broadcast_with_traffic_generator import broadcast_emulator
import ast
from vemu_as_api import upload_file_to_container
from vemu_api import *
import json
import time

def read_ini_config(ini_path="./input.ini"):
    """
    读取本地的ini文件, 返回两个dict: 服务器需要的值
    """
    config = workload_input.config_ini(path=ini_path)
    server_config = {
        "user_id": config["user"]["user-id"],
        "topo_id": config["user"]["topo-id"],
        "backend_ip": config["user"]["backend-ip"],
        "backend_port": config["user"]["backend-port"],

        "model": config["server-control"]["model"],
        "dataset": config["server-control"]["dataset"],
        "dtype": config["server-control"]["dtype"],
        "nodes_num": config["server-control"]["nodes-num"],
        "initial_distribution_phase": config["server-control"]["initial-distribution-phase"], 
        "initial_distribution_algorithm": config["server-control"]["initial-distribution-algorithm"],
        "gradient_convergence_algorithm": config["server-control"]["gradient-convergence-algorithm"],
        "circle_topo": config["server-control"]["circle-topo"],
        "nodes_list": config["server-control"]["nodes-list"],
        "father_node": config["server-control"]["father-node"]
    }

    return server_config

def initial_distribution_phase_emulation(server_config):
    """               
    根据配置文件模拟集合通信并返回时间
    """
    nodes_list = server_config["nodes_list"]
    nodes_list = ast.literal_eval(nodes_list)

    father_node = server_config["father_node"]

    user_id = server_config["user_id"]
    topo_id = server_config["topo_id"]

    init_dict = workload_input.model_ini(server_config["model"], server_config["dataset"], server_config["dtype"])
    
    init_data_size = init_dict["model_size"] + init_dict["dataset_size"]
    initial_phase_emulator = broadcast_emulator(nodes_list, father_node, init_data_size, user_id, topo_id)
    if server_config["initial_distribution_phase"]:
        # 如果用户enable初始分发阶段
        if server_config["initial_distribution_algorithm"] == "tree_sync_mode":
            initial_phase_time = initial_phase_emulator.tree_sync_mode()
        elif server_config["initial_distribution_algorithm"] == "tree_async_mode":
            initial_phase_time = 1
            # 异步的广播初始分发待开发
    else:
        # 如果用户disable初始分发阶段
        initial_phase_time = 0

    return initial_phase_time
        

def download_config_to_root(server_config, config_file_path="./input.ini", dst_path="/as_exec_file/"):
    """
    调用as中的api
    """
    container_ip = server_config["backend_ip"]
    container_port = server_config["backend_port"]
    container_user = server_config["user_id"]
    container_topo = server_config["topo_id"]
    container_root_node = server_config["father_node"]

    upload_file_to_container(container_ip, container_port, container_user, container_topo, container_root_node, config_file_path, dst_path)    


def exec_root_cmd(cmd_manager, cmd_dict):
    """
    server给root node下发指令调用root node的一个脚本
    """
    exec_res = cmd_manager.exec_cmds_in_nodes(
        cmd_dict
    )
    return exec_res

def exec_worker_cmd(cmd_manager, cmd_dict):
    """
    server给worker node下发指令调用worker node的一个脚本
    """
    exec_res = cmd_manager.exec_cmds_in_nodes(
        cmd_dict
    )
    return exec_res


def grad_aggregation_phase_emulation(server_config, grad_size):
    nodes_num = int(server_config["nodes_num"])
    data_size = int(grad_size)

    user_id = server_config["user_id"]
    topo_id = server_config["topo_id"]

    grad_phase_emulator = allreduce_emulator(nodes_num, data_size, user_id, topo_id)

    circle_topo = server_config["circle_topo"]
    circle_topo = ast.literal_eval(circle_topo)

    if server_config["gradient_convergence_algorithm"] == "ring_sync_mode":
        grad_aggregation_phase_time = grad_phase_emulator.ring_sync_mode(circle_topo)
    elif server_config["gradient_convergence_algorithm"] == "ring_async_mode":
        grad_aggregation_phase_time = grad_phase_emulator.ring_async_mode(circle_topo)
    else:
        grad_aggregation_phase_time = 1

    return grad_aggregation_phase_time

def extract_exec_res(worker_exec_res):
    grad_list = []
    time_list = []

    # worker_exec_res_dict = ast.literal_eval(worker_exec_res)
    for index in range(len(worker_exec_res)):
        node_exec_res = worker_exec_res[f"h{index+1}"][f"0_python3 /as_exec_file/worker_node_script_{index+1}.py"]["output"]
        print(node_exec_res)
        node_exec_res_dict = ast.literal_eval(node_exec_res)
        grad_list.append(int(node_exec_res_dict.get("grad_size")))
        time_list.append(int(node_exec_res_dict.get("time_info")))
    return grad_list, time_list

def main():
    server_config = read_ini_config()
    # server_config is a dict

    user_id = server_config["user_id"]
    topo_id = server_config["topo_id"]
    backend_ip = server_config["backend_ip"]
    backend_port = int(server_config["backend_port"])
    # user层面配置文件
    
    initial_phase_time = initial_distribution_phase_emulation(server_config)

    # download_config_to_root(server_config)
    # 从server将ini文件下发到root node
    time.sleep(10)
    cmd_manager = CmdManager(user_id, topo_id, backend_ip, backend_port)

    root_cmd_dict = {
        "h5": ["python3 /as_exec_file/Multi-DataCenter-Test-for-Klonet/root_node_script.py"]
    }
    root_exec_res = exec_root_cmd(cmd_manager, root_cmd_dict)
    print(root_exec_res)
    worker_cmd_dict = {
        "h1": ["python3 /as_exec_file/worker_node_script_1.py"],
        "h2": ["python3 /as_exec_file/worker_node_script_2.py"],
        "h3": ["python3 /as_exec_file/worker_node_script_3.py"],
        "h4": ["python3 /as_exec_file/worker_node_script_4.py"],
    }
    worker_exec_res = exec_worker_cmd(cmd_manager, worker_cmd_dict)
    # 在root node和worker node执行脚本
    print(worker_exec_res)
    grad_list, time_list = extract_exec_res(worker_exec_res)
    # grad_size = grad_size / (1024 ** 3)
    # Bytes -> GBytes
    print("grad_list:", grad_list)
    print("time_list:", time_list)
    grad_size = grad_list[0] / (1024 ** 3)
    phase_grad_aggregation_time = grad_aggregation_phase_emulation(server_config, grad_size)
    
    COMM_emulation_time = initial_phase_time + phase_grad_aggregation_time
    COMP_simulation_circle = max(time_list)
    # sum_time = phase_initial_distribution_time + phase_comp_simulation_info + phase_grad_aggregation_time
    print(f"COMM_emulation_time:{COMM_emulation_time} \n COMP_simulation_circle:{COMP_simulation_circle}")


if __name__ == "__main__":
    main()
