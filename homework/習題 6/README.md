# 行程與檔案相關程式

本文件說明 Linux 行程 (Process) 與檔案操作的核心系統呼叫，包括 `fork`、`execvp`、`close`、`open`、`read`、`write`、`dup2`，以及標準檔案描述符 (stdin 0, stdout 1, stderr 2) 的概念。

---

## 1. fork() - 行程建立

`fork()` 是用於建立新行程的系統呼叫。它會複製目前行程 (父行程)，建立一個完全相同的子行程。

### 語法

```c
#include <unistd.h>
pid_t fork(void);
```

### 返回值

- **在父行程中**: 返回子行程的 PID (正整數)
- **在子行程中**: 返回 0
- **失敗時**: 返回 -1

### 範例

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
    pid_t pid = fork();

    if (pid > 0) {
        // 父行程
        printf("我是父行程，PID = %d，子行程 PID = %d\n", getpid(), pid);
    } else if (pid == 0) {
        // 子行程
        printf("我是子行程，PID = %d，父行程 PID = %d\n", getpid(), getppid());
    } else {
        // fork 失敗
        perror("fork failed");
        return 1;
    }

    return 0;
}
```

### 重要概念

1. **子行程是父行程的拷貝**: 子行程繼承父行程的記憶體內容 (程式碼、資料、堆疊等)
2. **獨立的位址空間**: 子行程修改變數不會影響父行程
3. **子行程先結束**: 子行程會先執行完成，父行程需要使用 `wait()` 等待

---

## 2. execvp() - 執行外部程式

`execvp()` 是 `exec` 家族成員之一，用於在目前行程中執行一個新的程式。它會用新程式完全取代目前行程的記憶體內容。

### 語法

```c
#include <unistd.h>
int execvp(const char *file, char *const argv[]);
```

### 參數

- `file`: 要執行的程式名稱 (會搜尋 PATH 環境變數)
- `argv`: 传递给新程式的參數陣列，以 NULL 結尾

### 返回值

- **成功**: 不會返回 (行程被新程式完全取代)
- **失敗**: 返回 -1

### 重要特性

- 執行成功後，原本的程式碼會被完全覆蓋，`execvp` 之後的程式碼不會執行
- PID 保持不變，只是行程的內容被換掉了

### 範例

```c
#include <stdio.h>
#include <unistd.h>

int main() {
    char *args[] = {"ls", "-l", NULL};

    printf("執行 execvp 之前...\n");

    execvp("ls", args);

    // 如果 execvp 成功，這行不會執行
    perror("execvp failed");
    return 0;
}
```

---

## 3. fork() + execvp() 組合

這是 Unix/Linux 中最常見的行程建立模式：先 fork 建立子行程，再在子行程中執行 execvp 載入新程式。

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // 子行程：執行新程式
        char *args[] = {"ls", "-l", NULL};
        execvp("ls", args);
        // 如果 execvp 失敗
        perror("execvp failed");
        _exit(1);
    } else if (pid > 0) {
        // 父行程：等待子行程結束
        int status;
        waitpid(pid, &status, 0);
        printf("子行程執行完成\n");
    } else {
        perror("fork failed");
    }

    return 0;
}
```

---

## 4. 檔案操作

### 4.1 open() - 開啟檔案

```c
#include <fcntl.h>
int open(const char *pathname, int flags, ... /* mode_t mode */);
```

### 4.2 close() - 關閉檔案

```c
#include <unistd.h>
int close(int fd);
```

### 4.3 read() - 讀取資料

```c
#include <unistd.h>
ssize_t read(int fd, void *buf, size_t count);
```

### 4.4 write() - 寫入資料

```c
#include <unistd.h>
ssize_t write(int fd, const void *buf, size_t count);
```

### 範例：複製檔案

```c
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>

int main() {
    int src = open("source.txt", O_RDONLY);
    int dst = open("dest.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);

    char buf[1024];
    ssize_t n;

    while ((n = read(src, buf, sizeof(buf))) > 0) {
        write(dst, buf, n);
    }

    close(src);
    close(dst);
    return 0;
}
```

---

## 5. dup2() - 複製檔案描述符

`dup2()` 用於複製檔案描述符，常用於重新導向標準輸入/輸出/錯誤。

### 語法

```c
#include <unistd.h>
int dup2(int oldfd, int newfd);
```

### 作用

- 將 `newfd` 指向與 `oldfd` 相同的檔案
- 如果 `newfd` 已經開啟，會先關閉它

### 範例：輸出重導向

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int fd = open("output.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    pid_t pid = fork();

    if (pid == 0) {
        // 子行程：將標準輸出重導向到檔案
        dup2(fd, STDOUT_FILENO);  // STDOUT_FILENO = 1
        close(fd);

        char *args[] = {"ls", "-l", NULL};
        execvp("ls", args);
        perror("execvp failed");
        _exit(1);
    } else {
        close(fd);
        wait(NULL);
        printf("完成！輸出已寫入 output.txt\n");
    }

    return 0;
}
```

---

## 6. 標準檔案描述符

每個行程一開始就會開啟三個標準檔案描述符：

| 常數 | 數值 | 用途 |
|------|------|------|
| `STDIN_FILENO` | 0 | 標準輸入 (stdin) - 預設鍵盤 |
| `STDOUT_FILENO` | 1 | 標準輸出 (stdout) - 預設螢幕 |
| `STDERR_FILENO` | 2 | 標準錯誤 (stderr) - 預設螢幕 |

### 重新導向範例

```c
#include <fcntl.h>
#include <unistd.h>

int main() {
    // 將標準輸入重導向到檔案
    int fd = open("input.txt", O_RDONLY);
    dup2(fd, STDIN_FILENO);
    close(fd);

    // 將標準輸出和錯誤重導向到另一個檔案
    int out = open("output.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    dup2(out, STDOUT_FILENO);
    dup2(out, STDERR_FILENO);
    close(out);

    // 之後所有 printf/ fprintf(stdout, ...) 會寫入 output.txt
    // 所有錯誤訊息也會寫入 output.txt

    return 0;
}
```

---

## 7. 完整範例：簡易 Shell

以下是一個結合所有概念的簡易 Shell 實作：

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>

void execute_command(char **args, int background) {
    pid_t pid = fork();

    if (pid == 0) {
        // 子行程

        // 處理輸出重導向 >
        for (int i = 0; args[i] != NULL; i++) {
            if (strcmp(args[i], ">") == 0) {
                args[i] = NULL;
                int fd = open(args[i+1], O_WRONLY | O_CREAT | O_TRUNC, 0644);
                if (fd < 0) {
                    perror("open");
                    _exit(1);
                }
                dup2(fd, STDOUT_FILENO);
                close(fd);
                break;
            }
        }

        // 處理輸入重導向 <
        for (int i = 0; args[i] != NULL; i++) {
            if (strcmp(args[i], "<") == 0) {
                args[i] = NULL;
                int fd = open(args[i+1], O_RDONLY);
                if (fd < 0) {
                    perror("open");
                    _exit(1);
                }
                dup2(fd, STDIN_FILENO);
                close(fd);
                break;
            }
        }

        execvp(args[0], args);
        perror("command not found");
        _exit(1);
    } else if (pid > 0) {
        // 父行程
        if (!background) {
            waitpid(pid, NULL, 0);
        }
    } else {
        perror("fork failed");
    }
}

int main() {
    char input[1024];

    while (1) {
        printf("shell> ");
        if (fgets(input, sizeof(input), stdin) == NULL) break;

        // 移除換行符號
        input[strcspn(input, "\n")] = 0;

        if (strcmp(input, "exit") == 0) break;

        // 簡單解析 (以空白分隔)
        char *args[64];
        char *token = strtok(input, " ");
        int i = 0;
        while (token != NULL && i < 63) {
            args[i++] = token;
            token = strtok(NULL, " ");
        }
        args[i] = NULL;

        if (args[0] != NULL) {
            execute_command(args, 0);
        }
    }

    return 0;
}
```

---

## 8. 總結

| 系統呼叫 | 功能 |
|----------|------|
| `fork()` | 建立子行程，複製父行程 |
| `execvp()` | 在行程中執行新程式 |
| `open()` | 開啟檔案 |
| `close()` | 關閉檔案描述符 |
| `read()` | 讀取檔案 |
| `write()` | 寫入檔案 |
| `dup2()` | 複製檔案描述符 (用於重導向) |
| `stdin/stdout/stderr` | 標準輸入/輸出/錯誤 (0/1/2) |

這些是 Unix/Linux 系統程式的基礎，熟練掌握這些概念可以幫助您理解作業系統的運作原理，並能夠開發強大的系統工具。