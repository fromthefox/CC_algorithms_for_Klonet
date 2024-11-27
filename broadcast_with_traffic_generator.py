from traffic_generator import traffic_generator_init

class broadcast_emulator():
    def __init__(self, nodes_list, father_node, data_size, user_id="yhbian", topo_id="traffic_generator_test"):
        self.son_nodes_list = nodes_list
        self.father_node = father_node
        self.data_size = str(data_size) + "G"
        self.user_id = user_id
        self.topo_id = topo_id

    def tree_sync_mode(self):
        father_nodes_list = [self.father_node]
        son_nodes_list = self.son_nodes_list
        user_id = self.user_id
        topo_id = self.topo_id
        SUM_TIME = 0
        NODES_CNT = 1
        # print(self.nodes_list)
        # print(father_nodes_list)
        NODES_NUM = len(father_nodes_list) + len(son_nodes_list)
        step = 0
        while NODES_CNT < NODES_NUM:
            step += 1
            temp_father_nodes_list = []
            max_time = 0
            for father_node in father_nodes_list:
                for index, son_node in enumerate(son_nodes_list):
                    traffic_generator = traffic_generator_init(user_id=user_id, topo_id=topo_id, src_node=father_node, dst_node=son_node, data_size="1G")
                    time = traffic_generator.generate()
                    if time > max_time:
                        max_time = time
                    NODES_CNT += 1
                    _ = son_nodes_list.pop(index)
                    temp_father_nodes_list.append(son_node)
                    break
            print(f"tree_level:{step}, exec_time:{max_time}")
            SUM_TIME += max_time
            father_nodes_list += temp_father_nodes_list
        return SUM_TIME
    
    def tree_async_mode(self):
        pass

    def standard_mode(self):
        pass

emulator = broadcast_emulator(["h2", "h3", "h4", "h5"],"h1",1)
print("SUM TIME:", emulator.tree_sync_mode())
