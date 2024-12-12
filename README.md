# Multi-DataCenter Test for Klonet

该Proj目的在Klonet上实现多数据中心的LLM训练模拟, 以Klonet模拟广域场景下的集合通信时间, 以单个Astra-Sim|SimAI节点作为单个数据中心的训练时间的仿真, 通过系统层的调度\数据分发\指令下达等操作, 最终实现完整的广域场景下的多数据中心的LLM训练全周期模拟.

# 实现细节

## 集合通信

1. allreduce_with_traffic_generator.py 实现常见的AllReduce集合通信模拟

2. broadcast_with_traffic_generator.py 实现常见的广播通信模拟

3. CC_algorithms.ipynb 验证上述算法的正确性

4. traffic_generator.py 提供接口供 1. 和 2. 调用


## 数据中心实现

数据中心主要分为几个部分, 体现在as_api_test.py 和 as_api.py中, 包括对配置文件的分解+写入, 对workload的处理等, 准备工作完成后通过指令运行Astra-Sim, 取出输出结果中需要的部分, 包括Circle数量和Grad Size.

## 其他

workload_input.py 用于配置文件.ini解析

vemu_api_demo.py 给出自动搭建拓扑的实例

somtests.py 用于随时测试代码

# RUN

1. 将.ini文件和必要的输入文件保存到Root Node中

2. 在Root Node上运行 root_node_script.py

3. 在各个Worker Node上运行 worker_node_script_x.py

4. Root Node输出最终结果