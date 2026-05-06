#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        char *args[] = {"ls", "-l", NULL};
        execvp("ls", args);
        perror("execvp failed");
        _exit(1);
    } else if (pid > 0) {
        wait(NULL);
        printf("子行程執行完成\n");
    } else {
        perror("fork failed");
    }

    return 0;
}