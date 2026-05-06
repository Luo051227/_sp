#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>

int main() {
    int fd = open("output.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    pid_t pid = fork();

    if (pid == 0) {
        dup2(fd, STDOUT_FILENO);
        dup2(fd, STDERR_FILENO);
        close(fd);

        char *args[] = {"ls", "-l", NULL};
        execvp("ls", args);
        perror("execvp failed");
        _exit(1);
    } else if (pid > 0) {
        close(fd);
        wait(NULL);
        printf("完成！請查看 output.txt\n");
    } else {
        close(fd);
        perror("fork failed");
    }

    return 0;
}