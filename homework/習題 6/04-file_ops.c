#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    int fd = open("test.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    char *msg = "Hello, World!\n";
    write(fd, msg, strlen(msg));
    close(fd);

    fd = open("test.txt", O_RDONLY);
    char buf[128];
    ssize_t n = read(fd, buf, sizeof(buf) - 1);
    buf[n] = '\0';
    printf("讀取的內容: %s", buf);
    close(fd);

    return 0;
}