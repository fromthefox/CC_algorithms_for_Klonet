from traffic_generator import traffic_generator

father_nodes_list = ["h1"]
son_nodes_list = ["h2", "h3", "h4", "h5"]

user_id = "yhbian"
topo_id = "traffic_generator_test"
data_size = 10 #GB, 这里理论上与模型 & 数据集有关, 后面再做封装

SUM_TIME = 0
NODES_CNT = 1
NODES_NUM = len(father_nodes_list) + len(son_nodes_list)
while NODES_CNT < NODES_NUM:
    temp_father_nodes_list = []
    max_time = 0
    for father_node in father_nodes_list:
        for index, son_node in enumerate(son_nodes_list):
            traffic_generator = traffic_generator(user_id=user_id, topo_id=topo_id, src_node=father_node, dst_node=son_node, data_size=data_size)
            time = traffic_generator.generate()
            if time > max_time:
                max_time = time
            NODES_CNT += 1
            _ = son_nodes_list.pop(index)
            temp_father_nodes_list.append(son_node)
            break
    SUM_TIME += max_time
    father_nodes_list += temp_father_nodes_list

print(SUM_TIME)