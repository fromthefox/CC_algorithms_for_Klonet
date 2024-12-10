import configparser
import json
import os



def convert_value(value):
    """Convert string values into appropriate types (int, float, or list)."""
    if ',' in value:
        return [convert_value(v.strip()) for v in value.split(',')]
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value  # Default is to return the value as a string

def read_node_ini_file(node_ini_file_path):
    config = configparser.ConfigParser()
    config.read(node_ini_file_path)
    
    node_data = {}

    for section in config.sections():
        data = {}
        for key, value in config.items(section):
            data[key] = convert_value(value)
        node_data[section] = data
    
    return node_data

def generate_node_files_for_single_node(node_data, project_output_folder_path, node_name):
    # 获取节点的数据
    # node_data is a dict
    # and test
    node_data_for_node = node_data.get(node_name)
    # get the config for one node
    if not node_data_for_node:
        raise ValueError(f"Node {node_name} not found in provided data.")

    # 可能存在嵌套情况，我们需要进一步展开字典
    if isinstance(node_data_for_node, dict):
        # 如果嵌套层次为两层，我们选择获取嵌套字典的第一层
        if len(node_data_for_node) == 1:
            node_data_for_node = list(node_data_for_node.values())[0]
    
    # 网络部分的处理
    network_section = {
        "topology": node_data_for_node.get("topologies"),
        "npus_count": node_data_for_node.get("npus-count"),
        "bandwidth": node_data_for_node.get("bandwidth"),
        "latency": node_data_for_node.get("latency"),
    }

    # 确保每个字段都为列表
    for key in ["topology", "npus_count", "bandwidth", "latency"]:
        if network_section[key] is not None and not isinstance(network_section[key], list):
            network_section[key] = [network_section[key]]
    # "topology": Ring -> "topology": ["Ring"]

    # 系统部分的处理
    system_data = {}
    possible_keys = [
        "scheduling-policy", "endpoint-delay", "active-chunks-per-dimension",
        "preferred-dataset-splits", "all-reduce-implementation", "all-gather-implementation",
        "reduce-scatter-implementation", "all-to-all-implementation", "collective-optimization",
        "local-mem-bw", "boost-mode"
    ]
    
    for key in possible_keys:
        if key in node_data_for_node:
            if key in ["all-reduce-implementation", "all-gather-implementation", "reduce-scatter-implementation", "all-to-all-implementation"]:
                # 对某些字段，确保它们是列表
                system_data[key] = [node_data_for_node[key]] if isinstance(node_data_for_node[key], str) else node_data_for_node[key]
            else:
                system_data[key] = node_data_for_node[key]

    # 创建输出文件夹
    node_output_folder_path = os.path.join(project_output_folder_path, node_name)
    os.makedirs(node_output_folder_path, exist_ok=True)

    # 文件路径
    network_output_file_path = os.path.join(node_output_folder_path, 'network.yml')
    system_output_file_path = os.path.join(node_output_folder_path, 'system.json')

    # 写入 network.yml 文件
    with open(network_output_file_path, 'w') as yml_file:
        yml_content = (
            f"topology: [{', '.join(map(str, network_section['topology']))}]\n"
            f"npus_count: [{', '.join(map(str, network_section['npus_count']))}]\n"
            f"bandwidth: [{', '.join(map(str, network_section['bandwidth']))}]\n"
            f"latency: [{', '.join(map(str, network_section['latency']))}]\n"
        )
        yml_file.write(yml_content)

    # 写入 system.json 文件
    with open(system_output_file_path, 'w') as json_file:
        json.dump(system_data, json_file, indent=2)

    print(f"Files for node {node_name} have been generated successfully!")

    # 处理 workload 文件
    workload_file_name = node_data_for_node.get('workload')  # 获取工作负载文件名
    if workload_file_name:
        # 判断工作负载文件是否是txt文件
        if workload_file_name.endswith('.txt'):
            workload_file_path = os.path.join(project_output_folder_path, workload_file_name)
            workload_file_name = os.path.splitext(workload_file_name)[0]
            # 检查文件是否存在
            if os.path.exists(workload_file_path):
                print(f"Workload file found: {workload_file_path}")
            else:
                print(f"Warning: Workload file {workload_file_path} does not exist.")
                workload_file_path = None
        else:
            workload_file_path = None
    else:
        workload_file_path = None
    
    return workload_file_name, workload_file_path


def astra_sim_api(config):
    node_data = read_node_ini_file("./input.ini")
    print(node_data)
    workload_file_name, workload_file_path = generate_node_files_for_single_node(node_data, "./output/", "node1")


astra_sim_api(0)