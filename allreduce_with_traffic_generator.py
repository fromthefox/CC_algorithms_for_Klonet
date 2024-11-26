from traffic_generator import traffic_generator_init

class allreduce_emulator():
    def __init__(self, nodes_num, data_size, user_id="yhbian", topo_id="traffic_generator_test"):
        # data_size double GB
        # nodes_num int
        self.nodes_num = nodes_num
        self.data_size = data_size
        self.user_id = user_id
        self.topo_id = topo_id

    def ring_sync_mode(self, circle_topo):
        NODES_NUM = self.nodes_num
        segment_grad_size = self.data_size / NODES_NUM
        segment_grad_size = str(segment_grad_size) + "G"
        MAX_STEPS = 2 * (NODES_NUM - 1)
        ring_sync_time = 0
        for step in range(MAX_STEPS):
            max_time = 0
            for node_index, node in enumerate(circle_topo):
                if node_index == NODES_NUM - 1:
                    src_node = node
                    dst_node = circle_topo[0]
                else:
                    src_node = node
                    dst_node = circle_topo[node_index+1]
                traffic_generator = traffic_generator_init(self.user_id, self.topo_id, src_node, dst_node, segment_grad_size)
                send_time = traffic_generator.generate()
                if send_time > max_time:
                    max_time = send_time
            print(f"step:{step+1} exec_time:{max_time}")
            ring_sync_time += max_time
        return ring_sync_time
    
    def ring_async_mode(self, circle_topo):
        pass

    def butterfly_sync_mode(self):
        pass

    def tree_sync_mode(self):
        pass

