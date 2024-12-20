a = {'h1': {'0_python3 /as_exec_file/worker_node_script_1.py': {'exit_code': 0, 'output': "{'grad_size': '524288\\n', 'time_info': '51378000'}\n"}}, 'h2': {'0_python3 /as_exec_file/worker_node_script_2.py': {'exit_code': 0, 'output': "{'grad_size': '524288\\n', 'time_info': '51378000'}\n"}}, 'h3': {'0_python3 /as_exec_file/worker_node_script_3.py': {'exit_code': 0, 'output': "{'grad_size': '524288\\n', 'time_info': '51378000'}\n"}}, 'h4': {'0_python3 /as_exec_file/worker_node_script_4.py': {'exit_code': 0, 'output': "{'grad_size': '524288\\n', 'time_info': '51378000'}\n"}}}
worker_exec_res = str(a)

import ast

grad_list = []
time_list = []


worker_exec_res_dict = ast.literal_eval(worker_exec_res)
for index in range(len(worker_exec_res_dict)):
    node_exec_res = worker_exec_res_dict[f"h{index+1}"][f"0_python3 /as_exec_file/worker_node_script_{index+1}.py"]["output"]
    print(node_exec_res)
    node_exec_res_dict = ast.literal_eval(node_exec_res)
    grad_list.append(int(node_exec_res_dict.get("grad_size")))
    time_list.append(int(node_exec_res_dict.get("time_info")))