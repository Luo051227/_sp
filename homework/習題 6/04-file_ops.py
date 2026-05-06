import os

fd = os.open("test.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)

msg = b"Hello, World!\n"
os.write(fd, msg)
os.close(fd)

fd = os.open("test.txt", os.O_RDONLY)
buf = os.read(fd, 128)
os.close(fd)
print(f"讀取的內容: {buf.decode()}")