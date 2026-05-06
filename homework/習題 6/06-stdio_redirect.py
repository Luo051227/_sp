import os
import sys

fdin = os.open("input.txt", os.O_RDONLY)
fdout = os.open("output.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)

pid = os.fork()

if pid == 0:
    os.dup2(fdin, 0)   # STDIN_FILENO = 0
    os.dup2(fdout, 1)  # STDOUT_FILENO = 1
    os.close(fdin)
    os.close(fdout)

    os.execvp("cat", ["cat"])
    sys.exit(1)
elif pid > 0:
    os.close(fdin)
    os.close(fdout)
    os.wait()
    print("完成！input.txt 的內容已複製到 output.txt")
else:
    os.close(fdin)
    os.close(fdout)
    print("fork failed")