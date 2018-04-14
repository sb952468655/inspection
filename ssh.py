import paramiko

host = '202.102.19.253'
port = 9527
username = 'alang'
password = 'May4th@)!%'

# 实例化一个transport对象
trans = paramiko.Transport((host, port))
# 建立连接
trans.connect(username=username, password=password)

# 将sshclient的对象的transport指定为以上的trans
ssh = paramiko.SSHClient()
ssh._transport = trans

stdin, stdout, stderr = ssh.exec_command('61.155.123.20\r')
result = stdout.read().decode()
print(result)

ssh.close()