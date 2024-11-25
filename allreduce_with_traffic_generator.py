from traffic_generator import traffic_generator

weight_dtype = "fp16"
param_size = 2 if weight_dtype == "fp16" else 4
model_param_num = 8029995008
grad_size = model_param_num * param_size / (1024 * 1024 * 1024) # GB

circle_topo = ["h1", "h2", "h3", "h4", "h5"]
NODES_NUM = len(circle_topo)
segment_grad_size = grad_size / NODES_NUM #单个梯度块的size

MAX_STEPS = 2 * (NODES_NUM - 1)
allreduce_sum_time = 0
for step in range(MAX_STEPS):
    max_time = 0
    for node_index, node in enumerate(circle_topo):
        if node_index == NODES_NUM - 1:
            src_node = node
            dst_node = circle_topo[0]
        else:
            src_node = node
            dst_node = circle_topo[node_index+1]
        traffic_generator = traffic_generator("yhbian", "traffic_generator_test",src_node, dst_node, segment_grad_size)
        send_time = traffic_generator.generate()
        if send_time > max_time:
            max_time = send_time
    allreduce_sum_time += max_time

print(allreduce_sum_time)