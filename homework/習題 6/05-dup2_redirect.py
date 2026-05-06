import os
import sys

fd = os.open("output.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)

pid = os.fork()

if pid == 0:
    os.dup2(fd, 1)  # STDOUT_FILENO = 1
    os.dup2(fd, 2)  # STDERR_FILENO = 2
    os.close(fd)

    os.execvp("ls", ["ls", "-l"])
    sys.exit(1)
elif pid > 0:
    os.close(fd)
    os.wait()
    print("完成！輸出已寫入 output.txt")
else:
    os.close(fd)
    print("fork failed")