import requests

class traffic_generator():
    def __init__(self, user_id, topo_id, src_node, dst_node, data_size, CONFIG = {}, url = 'http://192.168.1.33:25888/master/traffic_gen/'):
        
        self.user_id = user_id
        self.topo_id = topo_id
        self.src_node = src_node
        self.dst_node = dst_node
        self.data_size = data_size
        self.CONFIG = CONFIG
        self.url = url

    def generate(self):
        data = {
            "user": self.user_id,
            "topo": self.topo_id,
            "src_node": self.src_node,
            "dst_node": self.dst_node,
            "data_size": self.data_size,
            "CONFIG": self.CONFIG
        }
        response = requests.post(self.url, json=data)
        response_json = response.json()
        print(response_json)
        return response_json


traffic_generator = traffic_generator("yhbian", "traffic_generator_test", "h1", "h2", "10M")
traffic_generator.generate()