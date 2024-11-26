from traffic_generator import traffic_generator_init
import time

weight_dtype = "fp16"
param_size_list = {
    "fp32": 4,
    "fp16": 2,
    "int8": 1,
    "int4": 0.5
}
model_param_list = {
    "Llama-3-8B": 8029995008,
    "GPT-2-small": 124439808,
    "GPT-2-medium": 355000000,
    "GPT-2-large": 774000000,
    "GPT-2-xl": 1591101440
}
model_param_num = model_param_list["Llama-3-8B"]
param_size = param_size_list["fp16"]
grad_size = model_param_num * param_size / (1024**3) # GB

circle_topo = ["h1", "h2", "h3", "h4", "h5"]
NODES_NUM = len(circle_topo)
segment_grad_size = grad_size / NODES_NUM #单个梯度块的size
segment_grad_size = "10M"

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
        traffic_generator = traffic_generator_init("yhbian", "traffic_generator_test",src_node, dst_node, segment_grad_size)
        send_time = traffic_generator.generate()
        if send_time > max_time:
            max_time = send_time
    allreduce_sum_time += max_time

print(allreduce_sum_time)