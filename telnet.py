import getpass
import telnetlib
import os
import sys
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s : %(levelname)s : %(message)s',
    filename='test.log',
    filemode='w',
) 

HOST = "127.0.0.1"
logging.info('host: 127.0.0.1')
user = input("Enter your remote account: ")
logging.info('user: %s' % user)
password = getpass.getpass()
logging.info('password: %s' % password)
tn = telnetlib.Telnet(HOST,timeout=10)

tn.set_debuglevel(10)

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\r\n")
if password:
    tn.read_until(b"password: ")
    tn.write(password.encode('ascii') + b"\r\n")


res = tn.read_some()
if b'Login Failed' in res:
    print('Login Failed')
    logging.error('Login Failed')
    sys.exit()
else:
    print('login ok')
    logging.info('login ok')

# tn.write(b"show version\n\r")
# tn.write(b"exit\n\r")

print(tn.read_all().decode('ascii'))