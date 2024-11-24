class traffic_generator():
    """
    定义简化版的traffic_generator来验证CC Demo
    """
    def __init__(self, user_id, proj_id, src_node_id, dst_node_id, data_size, run_time, CONFIG):
        """
        这里的src_node_id <-> dst_node_id之间的链路带宽和流量分布应该是从用户给出的CONFIG文件中获取, 但是为了演示Demo这里直接给出
        """
        self.src_node_id = src_node_id
        self.dst_node_id = dst_node_id
        self.data_size = data_size
        self.traffic_distribution = "uniform"
        self.link_bandwidth = 2 #kbps
    
    def traffic_generate(self):
        time = self.data_size / self.link_bandwidth
        performance_indicators = {"Test":"Test"}

        return time, performance_indicators