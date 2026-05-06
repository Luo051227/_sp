import os
import sys

pid = os.fork()

if pid > 0:
    print(f"Parent: PID={os.getpid()}, Child PID={pid}")
elif pid == 0:
    print(f"Child: PID={os.getpid()}, Parent PID={os.getppid()}")
else:
    print("fork failed")
    sys.exit(1)