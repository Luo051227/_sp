#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int fdin = open("input.txt", O_RDONLY);
    if (fdin < 0) {
        perror("open input");
        return 1;
    }

    int fdout = open("output.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fdout < 0) {
        perror("open output");
        close(fdin);
        return 1;
    }

    pid_t pid = fork();

    if (pid == 0) {
        dup2(fdin, STDIN_FILENO);
        dup2(fdout, STDOUT_FILENO);
        close(fdin);
        close(fdout);

        char *args[] = {"cat", NULL};
        execvp("cat", args);
        perror("execvp failed");
        _exit(1);
    } else if (pid > 0) {
        close(fdin);
        close(fdout);
        wait(NULL);
        printf("完成！input.txt 的內容已複製到 output.txt\n");
    } else {
        close(fdin);
        close(fdout);
        perror("fork failed");
    }

    return 0;
}