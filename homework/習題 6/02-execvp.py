import os

print(f"執行 os.execvp 之前，PID={os.getpid()}")

os.execvp("ls", ["ls", "-l"])