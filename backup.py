import os
import time

source = [r'E:\教程\C', r'E:\教程\Rust']

target_dir = r'E:\项目备份'

target = target_dir + os.sep + \
    time.strftime('%Y%m%d%H%M%S') + '.zip'


zip_command = 'zip -r {0} {1}'.format(target,
    ' '.join(source))


print('Zip command is:')
print(zip_command)
print('Running:')
if os.system(zip_command) == 0:
    print('Successful backup to', target)
else:
    print('Backup FAILED')
