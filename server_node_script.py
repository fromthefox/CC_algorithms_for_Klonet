"""
该脚本运行于服务器
"""
import workload_input
from allreduce_with_traffic_generator import allreduce_emulator
from broadcast_with_traffic_generator import broadcast_emulator
import ast
from vemu_as_api import upload_file_to_container
from vemu_api import *


def read_ini_config(ini_path="./input.ini"):
    """
    读取本地的ini文件, 返回两个值:
    1. 需要服务器自己拿到的值
    2. 服务器需要分发给root node的值 (直接把ini文件发给root node)
    """
    config = workload_input.config_ini(path=ini_path)
    server_config = {
        "user_id": config["user"]["user-id"],
        "topo_id": config["user"]["topo-id"], 
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
        if server_config["initial_distribution_algorithm"] == "tree_sync_mode":
            initial_phase_time = initial_phase_emulator.tree_sync_mode()
        elif server_config["initial_distribution_algorithm"] == "tree_async_mode":
            initial_phase_time = 1
    else:
        initial_phase_time = 0

    return initial_phase_time
        

def download_config_to_root(download_config, config_file_path, node_name, dst_path):
    """
    调用as中的api
    """
    container_ip = download_config["ip"]
    container_port = download_config["port"]
    container_user = download_config["user"]
    container_topo = download_config["topo"]
    upload_file_to_container(container_ip, container_port, container_user, container_topo, node_name, config_file_path, dst_path)    


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

def recv_from_worker():
    """
    worker node将仿真的结果返回给server
    问一下@ZCY是否有合适的api
    """
    pass

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



def main():
    server_config = read_ini_config()
    initial_phase_time = initial_distribution_phase_emulation(server_config)

    # download_config_to_root()
    # exec_root_cmd()
    # exec_worker_cmd()
    # phase_comp_simulation_info = recv_from_worker()
    
    """
    上面四个函数的实现主要需要接口, 分别为:
    1. 从Server向容器下发文件
    2. 从Server中向容器下发指令
    3. 容器向Server发送数据
    """
    # phase_grad_aggregation_time = grad_aggregation_phase_emulation(phase_comp_simulation_info)
    # sum_time = phase_initial_distribution_time + phase_comp_simulation_info + phase_grad_aggregation_time



if __name__ == "__main__":
    main()