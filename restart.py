from time import sleep
import sys
import os
os.system('kill 1')
sleep(10)
os.execv(sys.executable, ['python'] + sys.argv)