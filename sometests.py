import subprocess

# 执行命令
result = subprocess.run(['ls', '-l'], capture_output=True, text=True)

# 打印命令的输出
print('stdout:', result.stdout)

# 打印命令的错误输出
print('stderr:', result.stderr)

# 打印命令的返回码
print('returncode:', result.returncode)