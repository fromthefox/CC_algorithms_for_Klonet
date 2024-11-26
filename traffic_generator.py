import requests

class traffic_generator_init():
    def __init__(self, user_id, topo_id, src_node, dst_node, data_size, CONFIG = {}, url = "http://kb310server.x3322.net:10441/master/traffic_gen/"):
        # 'http://192.168.1.33:25888/master/traffic_gen/'
        # "http://kb310server.x3322.net:10441/master/traffic_gen/"
        self.user_id = user_id
        self.topo_id = topo_id
        self.src_node = src_node
        self.dst_node = dst_node
        self.data_size = data_size
        self.CONFIG = CONFIG
        self.url = url
        self.force = 1

    def generate(self):
        data = {
            "user": self.user_id,
            "topo": self.topo_id,
            "src_node": self.src_node,
            "dst_node": self.dst_node,
            "data_size": self.data_size,
            "CONFIG": {
                "force": self.force
            }
        }
        response = requests.post(self.url, json=data)
        response_json = response.json()
        print(response_json)
        time = response_json["simple_info"]["time"]
        return time
    
# traffic_generator = traffic_generator_init("yhbian", "traffic_generator_test", "h5", "h1", "1G")
# traffic_generator.generate()


# data = {
#             "user": "yhbian",
#             "topo": "traffic_generator_test",
#             "src_node": "h5",
#             "dst_node": "h1",
#             "data_size": "1G",
#             "CONFIG": {
#                 "force": True
#             }
#         }
# response = requests.post("http://kb310server.x3322.net:10441/master/traffic_gen/", json=data)
# response_json = response.json()
# print(response_json)