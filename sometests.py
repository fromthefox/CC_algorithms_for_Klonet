import subprocess

def exec_as(workload_file_name):

    command = f'cd /app/astra-sim/tests/text && bash run.sh {workload_file_name}  > ./output_log/{workload_file_name}.log'
    workload_file_path = f"/app/astra-sim/tests/text/output_log/{workload_file_name}.log"
    # 使用subprocess.Popen()执行复合命令
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 等待命令执行完成并获取输出
    stdout, stderr = process.communicate()

    # 打印输出和错误
    print('stdout:', stdout)
    print('stderr:', stderr)

    # 检查返回码
    if process.returncode == 0:
        print("Command executed successfully.")
    else:
        print("Command failed with return code:", process.returncode)
    return workload_file_path


exec_as("DLRM_HybridParallel")