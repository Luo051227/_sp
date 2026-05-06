# 行程與檔案 - 初學者教學

這份文件用簡單的方式說明 Linux/Unix 的重要概念。其實這些概念跟我們日常生活中做的事情很像！

---

## 什麼是行程 (Process)？

想象一下：
- 你有一間工廠（這就是一個**行程**）
- 工廠裡有很多機器在運作（就像程式碼在執行）

在電腦中，**行程 = 正在執行的程式**。

---

## 1. fork() - 複製一個自己

### 什麼是 fork？

`fork()` 就像是**影印**。它會複製現在的行程，變成兩個一樣的行程。

### 生活中的例子

想象你有一張照片，你按下影印機，得到兩張一樣的照片：
- 原本的照片（父行程）
- 影印出來的照片（子行程）

兩張照片內容相同，但後續可以在上面寫不同的東西，互不影响。

### Python 範例

```python
import os

pid = os.fork()  # 影印一份自己

if pid > 0:
    print(f"我是原本的程式（父行程），PID={os.getpid()}")
    print(f"我生了一個小孩，他的 PID={pid}")
elif pid == 0:
    print(f"我是被複製出來的程式（子行程），PID={os.getpid()}")
    print(f"我的爸爸 PID={os.getppid()}")
else:
    print("糟糕！影印失敗了！")
```

### fork() 的返回值（重要！）

| 返回值 | 意思 |
|--------|------|
| 正整數 (>0) | 你在**父行程**中，這個數字是**子行程的 PID** |
| 0 | 你在**子行程**中 |
| -1 | **失敗**了！ |

### 為什麼子行程返回 0？

因為子行程不需要知道自己的 PID（它可以用 `os.getpid()` 取得），父行程返回子行程的 PID 是為了**之後可以追蹤和管理這個孩子**。

---

## 2. execvp() - 執行新程式

### 什麼是 execvp？

`execvp()` 就像走進一間已經開著的工廠，然後把裡面的機器全部換成新的！

原本的程式會被**完全覆蓋**，就像：
- 你的程式是個房子
- execvp 把房子裡的東西全部清空，放進新的東西
- 但房子還在（PID 不變）

### Python 範例

```python
import os

print("我要執行 ls 指令了...")

# execvp("程式名稱", [參數列表])
# 這裡會執行 ls -l
os.execvp("ls", ["ls", "-l"])

# 這行不會執行！因为上面已经替换了整个程序
print("這行永遠不會出現")
```

### 重要特性

1. **成功不會返回** - 整個程式被換掉了，當然不會繼續執行後面的程式碼
2. **PID 不變** - 還是同一個行程，只是內容變了

---

## 3. fork() + execvp() - 一起使用

這是 Unix/Linux 最常見的用法！

### 為什麼要這樣做？

想象你要啟動一個新的應用程式（如記事本），你會：
1. 先複製一份自己（fork）
2. 在複製品中啟動新程式（execvp）

這樣父行程可以繼續做其他事情，子行程去執行新任務。

### Python 範例

```python
import os
import sys

pid = os.fork()

if pid == 0:
    # 子行程：執行新程式
    os.execvp("ls", ["ls", "-l"])
    # 如果 execvp 失敗才會執行下面
    sys.exit(1)
elif pid > 0:
    # 父行程：等待子行程完成
    os.wait()
    print("子行程執行完了！")
else:
    print("fork 失敗！")
```

### 運作流程

```
[父行程]
   │
   ├── fork() ───> [子行程] （複製品）
   │                  │
   │                  └── execvp("ls") ───> 執行 ls 指令
   │
   └── wait() 等待
```

---

## 4. 檔案操作 - open, read, write, close

這些就像我們平時操作檔案一樣：
- **open** = 打開檔案（像打開抽屜）
- **read** = 讀取內容（看抽屜裡的東西）
- **write** = 寫入東西（把東西放進抽屜）
- **close** = 關閉檔案（關上抽屜）

### Python 範例：讀寫檔案

```python
import os

# 開啟檔案（如果不存在就建立）
# O_WRONLY = 只能寫入
# O_CREAT = 如果不存在就建立
# O_TRUNC = 如果已經存在，清空內容
fd = os.open("hello.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)

# 寫入內容
os.write(fd, b"Hello! 你好！\n")

# 關閉檔案
os.close(fd)

# 再次打開，這次讀取
fd = os.open("hello.txt", os.O_RDONLY)
content = os.read(fd, 100)  # 最多讀 100 個字節
os.close(fd)

print("讀到的內容：", content.decode())
```

### 常見的 open 模式

| 模式 | 說明 |
|------|------|
| `O_RDONLY` | 只能讀取 |
| `O_WRONLY` | 只能寫入 |
| `O_RDWR` | 可以讀也可以寫 |
| `O_CREAT` | 檔案不存在時建立 |
| `O_TRUNC` | 覆蓋現有檔案 |
| `O_APPEND` | 追加到檔案末尾 |

---

## 5. dup2() - 複製檔案描述符

### 什麼是檔案描述符？

當你打開檔案時，系統會給你一個**編號**，叫做**檔案描述符** (file descriptor)。

就像：
- 檔案 = 餐廳
- 檔案描述符 = 桌號

### dup2 是什麼？

`dup2(oldfd, newfd)` = 把**新桌號**指向**舊桌號同一個餐廳**。

簡單說：**複製一個指向同一個檔案的編號**。

### 用來做什麼？

**輸出重導向**！例如：
- 本來要顯示在螢幕上的內容，改寫到檔案裡
- `ls > output.txt` 就是這種概念

### Python 範例：輸出重導向

```python
import os
import sys

# 打開一個檔案當作輸出目標
fd = os.open("output.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)

pid = os.fork()

if pid == 0:
    # 子行程：把標準輸出 (1) 複製到 fd
    os.dup2(fd, 1)  # 1 = STDOUT_FILENO (標準輸出)
    os.dup2(fd, 2)  # 2 = STDERR_FILENO (標準錯誤)
    os.close(fd)    # 關閉原本的 fd

    # 執行 ls，輸出會寫到 output.txt 而不是螢幕
    os.execvp("ls", ["ls", "-l"])
    sys.exit(1)
elif pid > 0:
    os.close(fd)
    os.wait()
    print("完成！輸出已寫入 output.txt")
else:
    print("fork 失敗")
```

---

## 6. 標準檔案描述符 - stdin, stdout, stderr

每個程式一開始就有三個**標準**的檔案描述符：

| 編號 | 名稱 | 預設對象 | 就像... |
|------|------|----------|---------|
| 0 | stdin | 鍵盤 | 餐廳的**點餐口**（輸入） |
| 1 | stdout | 螢幕 | 餐廳的**出菜口**（正常輸出） |
| 2 | stderr | 螢幕 | 餐廳的**抱怨處理**（錯誤訊息） |

### 生活中的例子

```
你（程式）：
  ├── 輸入 (stdin=0):  鍵盤輸入資料
  ├── 輸出 (stdout=1):  螢幕顯示結果
  └── 錯誤 (stderr=2):  螢幕顯示錯誤訊息
```

### 用 dup2 做輸入重導向

```python
import os
import sys

# 先建立一個測試檔案
os.write(os.open("input.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644), b"Hello World\n")

# 打開輸入檔案
fd_in = os.open("input.txt", os.O_RDONLY)

pid = os.fork()

if pid == 0:
    # 把標準輸入 (0) 改成 input.txt
    os.dup2(fd_in, 0)
    os.close(fd_in)

    # 執行 cat，它會從 stdin 讀取並輸出
    os.execvp("cat", ["cat"])
    sys.exit(1)
elif pid > 0:
    os.close(fd_in)
    os.wait()
    print("完成！")
```

---

## 7. 完整範例：自己動手做

### 練習 1：執行 ls 命令

```python
import os
import sys

pid = os.fork()

if pid == 0:
    # 子行程執行 ls
    os.execvp("ls", ["ls", "-l"])
    print("execvp 失敗！")  # 只會在失敗時執行
    sys.exit(1)
elif pid > 0:
    # 父行程等待
    os.wait()
    print("執行完成！")
else:
    print("fork 失敗！")
```

### 練習 2：輸出到檔案

```python
import os

# 打開 output.txt
fd = os.open("result.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)

pid = os.fork()

if pid == 0:
    # 把輸出導向到檔案
    os.dup2(fd, 1)  # 標準輸出改成 fd
    os.close(fd)
    
    os.execvp("ls", ["ls", "-l"])
else:
    os.close(fd)
    os.wait()
```

---

## 8. 總結表格

| 指令 | 功能 | 生活中的比喻 |
|------|------|-------------|
| `os.fork()` | 複製一個行程 | 影印文件 |
| `os.execvp()` | 執行新程式 | 換掉工廠裡的機器 |
| `os.open()` | 開啟檔案 | 打開抽屜 |
| `os.close()` | 關閉檔案 | 關上抽屜 |
| `os.read()` | 讀取資料 | 看抽屜裡的東西 |
| `os.write()` | 寫入資料 | 把東西放進抽屜 |
| `os.dup2()` | 複製檔案描述符 | 複製桌號 |

### 標準檔案描述符

| 編號 | 常數 | 用途 |
|------|------|------|
| 0 | stdin | 標準輸入（鍵盤） |
| 1 | stdout | 標準輸出（螢幕） |
| 2 | stderr | 標準錯誤（螢幕） |

---

## 9. 進一步學習

這些概念是 Unix/Linux 系統程式的基礎，學會後你可以：

1. **自己寫 shell** - 像 bash 一樣的命令列工具
2. **管線 (pipe)** - 連接多個程式的輸出輸入
3. **行程管理** - 同時執行多個任務
4. **檔案重導向** - 自由控制輸入輸出

加油！這些概念一開始可能覺得複雜，但多練習就會越來越熟悉！