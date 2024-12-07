from traffic_generator import traffic_generator_init
from threading import Thread

class allreduce_emulator():
    def __init__(self, nodes_num, data_size, user_id="yhbian", topo_id="traffic_generator_test"):
        # data_size double GB
        # nodes_num int
        self.nodes_num = nodes_num
        self.data_size = data_size
        self.user_id = user_id

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
        node_status_matrix = {
            "h1": 1,
            "h2": 1,
            "h3": 1,
            "h4": 1,
            "h5": 1
        }
        node_time_dict = {
            "h1": 0,
            "h2": 0,
            "h3": 0,
            "h4": 0,
            "h5": 0
        }
        # 0: waiting for data
        # 1: ready to send
        # 2: finished

        segment_grad_size = self.data_size / len(circle_topo)
        segment_grad_size = str(segment_grad_size) + "G"
        
        def reduce_send(node_id, node_num):
            cnt = 0
            global circle_topo
            node_index = circle_topo.index(node_id)
            if node_index == len(circle_topo)-1:
                src_node = node_id
                dst_node = circle_topo[0]
            else:
                src_node = node_id
                dst_node = circle_topo[node_index+1]
            while True:
                if cnt == 2*(node_num - 1):
                    break
                global node_status_matrix
                global node_time_dict
                if node_status_matrix[src_node] == 1:
                    traffic_generator = traffic_generator_init(self.user_id, self.topo_id, src_node, dst_node, segment_grad_size)
                    send_time = traffic_generator.generate()
                    print(f"src:{src_node}, dst:{dst_node}, time:{send_time}")
                    node_status_matrix[src_node] = 0
                    node_status_matrix[dst_node] = 1
                    node_time_dict[src_node] += send_time
                    cnt += 1
        for i in range(len(circle_topo)):
            exec("thread{} = Thread(target=reduce_send, args=('h{}',5))".format(i+1, i+1))
        
        for i in range(len(circle_topo)):
            exec("thread{}.start()".format(i+1))
        
        for i in range(len(circle_topo)):
            exec("thread{}.join()".format(i+1))

        print(node_time_dict)
        ring_async_time = 0
        for i in node_time_dict:
            if node_time_dict[i] > ring_async_time:
                ring_async_time = node_time_dict
        return ring_async_time


    def butterfly_sync_mode(self):
        pass

    def tree_sync_mode(self):
        pass