
from broadcast_with_traffic_generator import broadcast_emulator

def init_distribution_phase(nodes_list, father_node, data_size, user_id, topo_id,  algorithm="tree_sync_mode"):
    init_distribution_emulator = broadcast_emulator(nodes_list, father_node, data_size, user_id, topo_id)
    if algorithm == "tree_sync_mode":
        init_time = init_distribution_emulator.tree_sync_mode()
        return init_time
    
print(init_distribution_phase(["h1", "h2", "h3", "h4", "h5"],"h1",1,"yhbian","traffic_generator_test"))