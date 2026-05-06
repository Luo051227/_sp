#include <stdio.h>
#include <unistd.h>

int main() {
    char *args[] = {"ls", "-l", NULL};

    printf("執行 execvp 之前，PID=%d\n", getpid());
    execvp("ls", args);
    
    perror("execvp failed");
    return 0;
}