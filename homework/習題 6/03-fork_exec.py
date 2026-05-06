import os
import sys

pid = os.fork()

if pid == 0:
    os.execvp("ls", ["ls", "-l"])
    sys.exit(1)
elif pid > 0:
    os.wait()
    print("子行程執行完成")
else:
    print("fork failed")