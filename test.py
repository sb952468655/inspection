import re
import logging
import datetime
from warn import *
logging.basicConfig(level=logging.INFO)
a = '''Power supply number               : 2
    Defaulted power supply type     : dc
    Power supply model              : pem-3
    Status                          : up'''

print(mobile_warn2(a))