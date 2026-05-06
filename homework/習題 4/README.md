# 系統程式設計完全指南

![系統程式](https://img.shields.io/badge/系統程式-入門到進階-blue)
![適合初學者](https://img.shields.io/badge/適合-初學者-green)
![線上學習](https://img.shields.io/badge/線上-學習-orange)

---

## 目錄

1. [系統程式概述](#第一章系統程式概述)
2. [組合語言與機器碼](#第二章組合語言與機器碼)
3. [編譯器設計](#第三章編譯器設計)
4. [作業系統核心](#第四章作業系統核心)
5. [連結器與載入器](#第五章連結器與載入器)
6. [系統工具與程式開發](#第六章系統工具與程式開發)
7. [系統安全基礎](#第七章系統安全基礎)
8. [進階主題](#第八章進階主題)
9. [實作練習](#實作練習)
10. [常見問題](#常見問題)
11. [學習資源](#學習資源)

---

## 第一章：系統程式概述

### 1.1 什麼是系統程式

系統程式（System Programming）是電腦科學中專門為電腦系統硬體和軟體提供服務的程式設計領域。與一般應用程式不同，系統程式直接與硬體互動，提供作業系統、編譯器、驅動程式等基礎設施軟體。

**系統程式 vs 應用程式**

| 特性 | 系統程式 | 應用程式 |
|------|-----------|----------|
| 目標 | 為其他程式提供服務 | 解決使用者問題 |
| 硬體訪問 | 直接訪問 | 透過作業系統 |
| 效能要求 | 極高 | 適中 |
| 穩定性要求 | 極高 | 適中 |
| 範例 | OS核心、編譯器 | Word、遊戲 |

**系統程式的核心目標：**

1. **效率（Efficiency）**：系統程式必須以最少的資源完成任務
2. **控制（Control）**：精確控制硬體和系統資源
3. **穩定性（Stability）**：長時間穩定運作不出錯
4. **可移植性（Portability）**：能在不同硬體上執行

**系統程式的主要領域：**

- 作業系統核心開發
- 驅動程式開發
- 編譯器和直譯器開發
- 嵌入式系統開發
- 效能工具開發

### 1.2 系統程式的發展歷史

**第一階段：早期計算機時代（1950-1960年代）**

在1950年代，電腦程式設計完全依賴組合語言。程式設計師需要直接操作機器碼和記憶體位址，這是一項極度繁瑣且容易出錯的工作。

```
早期組合語言範例：
01000001  - 加載資料
10110010  - 儲存資料
01101100  - 跳轉
```

**第二階段：作業系統誕生（1960-1970年代）**

1960年代，IBM推出了OS/360，這是第一個大型商用作業系統。同時期，MIT開發了MULTICS作業系統。

1970年代是系統程式的重要里程碑：
- UNIX作業系統在貝爾實驗室誕生
- C語言由丹尼斯·里奇發明
- POSIX標準開始制定

**第三階段：個人電腦時代（1980-1990年代）**

個人電腦的普及帶動了系統軟體的發展：
- BIOS的發展
- 各種驅動程式的出現
- Windows作業系統的崛起

**第四階段：現代計算時代（2000-至今）**

- 虛擬化技術（VMware, VirtualBox）
- 雲端運算（AWS, Azure, GCP）
- 容器化（Docker, Kubernetes）
- 物聯網（IoT）

### 1.3 為什麼要學習系統程式

**1. 深入理解電腦運作原理**

學習系統程式讓你能夠：
- 了解程式如何被執行
- 理解記憶體管理機制
- 掌握硬體與軟體的互動方式

**2. 提升程式設計能力**

系統程式設計培養的技能：
- 對效能的敏銳感知
- 資源管理的意識
- 正確的錯誤處理方式

**3. 開啟職業發展的大門**

相關職業包括：
- 作業系統工程師
- 編譯器開發者
- 嵌入式系統工程師
- 安全研究人員
- 效能工程師

### 1.4 系統程式的分類

#### 1.4.1 作業系統核心（Kernel）

作業系統核心是系統程式中最重要的部分，它管理硬體資源並提供服務給上層軟體。

**核心的主要功能：**

```
┌─────────────────────────────────┐
│       使用者應用程式            │
├─────────────────────────────────┤
│       系統庫（System Library） │
├─────────────────────────────────┤
│       作業系統核心（Kernel）   │
├─────────────────────────────────┤
│       硬體（Hardware）         │
└─────────────────────────────────┘
```

- 程序管理：建立、終止、排程程序
- 記憶體管理：分配和回收記憶體
- 檔案系統：管理儲存裝置
- 設備驅動：控制硬體設備

#### 1.4.2 設備驅動程式（Device Drivers）

驅動程式是硬體與作業系統之間的橋樑。每種硬體設備都需要專屬的驅動程式。

**驅動程式的類型：**

1. **字符設備驅動**：鍵盤、滑鼠、序列埠
2. **區塊設備驅動**：硬碟、SSD、光碟
3. **網路設備驅動**：網卡、路由器

#### 1.4.3 編譯器（Compilers）

編譯器將高階語言（如C、C++、Java）翻譯成機器碼。

**編譯器的種類：**

- GCC（GNU Compiler Collection）
- Clang/LLVM
- MSVC（Microsoft Visual C++）
- javac（Java編譯器）

#### 1.4.4 組譯器（Assemblers）

組譯器將組合語言翻譯成機器碼。

**常用組譯器：**

- NASM（Netwide Assembler）
- MASM（Microsoft Macro Assembler）
- GAS（GNU Assembler）

#### 1.4.5 連結器（Linkers）

連結器將多個目標檔案合併成單一的可執行檔案。

**連結器的功能：**

- 符號解析
- 重定位
- 符號表生成

#### 1.4.6 載入器（Loaders）

載入器將可執行檔案載入記憶體並開始執行。

### 1.5 學習路徑建議

**初學者建議學習順序：**

1. C語言基礎（必備）
2. 組合語言基礎
3. 編譯器原理
4. 作業系統概念
5. 連結器和載入器
6. 實作練習

---

## 第二章：組合語言與機器碼

### 2.1 電腦硬體基礎

在學習組合語言之前，我們需要了解電腦的基本硬體組成。

#### 2.1.1 中央處理器（CPU）

CPU是電腦的大腦，負責執行指令。

```
CPU基本結構：
┌────────────────────────────────────┐
│           控制單元（CU）            │
├────────────────────────────────────┤
│           算術邏輯單元（ALU）       │
├────────────────────────────────────┤
│           暫存器（Registers）       │
└────────────────────────────────────┘
```

**CPU的主要組件：**

1. **控制單元**：負責指令解碼和控制信號產生
2. **算術邏輯單元（ALU）**：執行算術和邏輯運算
3. **暫存器**：高速記憶體，用於存儲臨時資料

#### 2.1.2 記憶體層次結構

電腦記憶體分為多個層次，速度和容量不同：

```
速度 ↑                    容量 ↓
┌─────────────────────────────┐
│ CPU暫存器（最快，最小）      │  ← 幾個 CPU 週期
├─────────────────────────────┤
│ L1 快取                     │  ← 幾個 CPU 週期
├─────────────────────────────┤
│ L2 快取                     │  ← 數十 CPU 週期
├─────────────────────────────┤
│ L3 快取                     │  ← 數百 CPU 週期
├─────────────────────────────┤
│ 主記憶體（RAM）             │  ← 數百 CPU 週期
├─────────────────────────────┤
│ SSD/HDD                     │  ← 微秒到毫秒
└─────────────────────────────┘
```

### 2.2 機器語言基礎

機器語言是CPU直接執行的二進制指令集，是程式設計的最低層次。

#### 2.2.1 二進制與十六進制

電腦使用二進制（0和1）表示資料。

```
十進制 → 二進制 → 十六進制
0      → 0000   → 0
1      → 0001   → 1
2      → 0010   → 2
...
15     → 1111   → F
255    → 11111111 → FF
```

**為什麼使用十六進制？**
- 二進制太長，難以閱讀
- 十六進制每個數字代表4個二進制位元
- 記憶體位址常用十六進制表示

#### 2.2.2 指令格式

機器指令由操作碼（Opcode）和運算元（Operands）組成。

**x86指令格式：**

```
[前綴] [操作碼] [ModR/M] [SIB] [位移] [立即數]
┌────────┬──────┬────────┬─────┬────────┬──────────┐
│ 可選   │ 必需  │ 可選   │可選 │ 可選   │ 可選     │
└────────┴──────┴────────┴─────┴────────┴──────────┘
```

**指令範例（x86-64）：**

```
B8 01 00 00 00    → mov eax, 1
48 89 C3          → mov rbx, rax
FF D0             → call rax
```

#### 2.2.3 常見的指令集架構

| 架構 | 公司 | 應用領域 | 特點 |
|------|------|----------|------|
| x86/x64 | Intel/AMD | PC、伺服器 | CISC，指令複雜 |
| ARM | ARM | 手機、嵌入式 | RISC，節能 |
| MIPS | Imagination | 網路設備 | RISC，簡潔 |
| RISC-V | 开源 | 研究、嵌入式 | RISC，開源 |

### 2.3 組合語言的特性

組合語言是機器語言的可讀性表示，使用助記符代替二進制操作碼。

#### 2.3.1 基本語法

**NASM語法（Linux）：**

```asm
; 這是註解
section .data
    msg db "Hello, World!", 10  ; 10 = 換行符

section .text
    global _start
_start:
    mov rax, 1        ; 系統呼叫號：sys_write
    mov rdi, 1        ; 檔案描述符：stdout
    mov rsi, msg      ; 字串位址
    mov rdx, 14      ; 字串長度
    syscall          ; 執行系統呼叫
    mov rax, 60      ; 系統呼叫號：sys_exit
    xor rdi, rdi     ; 退出碼：0
    syscall          ; 執行系統呼叫
```

#### 2.3.2 常見指令

**資料傳送指令：**

```asm
mov dest, src    ; 複製資料
push value       ; 推入堆疊
pop dest         ; 彈出堆疊
xchg a, b        ; 交換值
```

**算術運算指令：**

```asm
add a, b         ; a = a + b
sub a, b         ; a = a - b
mul reg          ; unsigned乘法
imul reg          ; signed乘法
div reg          ; unsigned除法
idiv reg         ; signed除法
inc reg          ; 遞增
dec reg          ; 遞減
neg reg          ; 取負
```

**邏輯運算指令：**

```asm
and a, b         ; 邏輯AND
or a, b          ; 邏輯OR
xor a, b         ; 邏輯XOR
not a            ; 邏輯NOT
```

**控制流指令：**

```asm
jmp label        ; 無條件跳轉
je label         ; 相等時跳轉
jne label        ; 不相等時跳轉
jg label         ; 大於時跳轉
jl label         ; 小於時跳轉
cmp a, b         ; 比較（設定標誌）
```

**函數呼叫指令：**

```asm
call label       ; 呼叫函數
ret              ; 返回
```

### 2.4 x86-64 組合語言實戰

#### 2.4.1 暫存器

x86-64架構的主要暫存器：

**通用暫存器：**

| 暫存器 | 用途 | 保存性 |
|--------|------|--------|
| RAX | 累加器，返回值 | 否 |
| RBX | 一般用途 | 是 |
| RCX | 迴圈計數器 | 否 |
| RDX | I/O指標 | 否 |
| RSI | 來源指標 | 否 |
| RDI | 目標指標 | 否 |
| RBP | 框架指標 | 是 |
| RSP | 堆疊指標 | 特殊 |
| R8-R15 | 額外暫存器 | 否 |

**特殊暫存器：**

- RIP：指令指標（下一條指令的位址）
- RFLAGS：狀態標誌（Zero, Carry, Overflow等）

#### 2.4.2 記憶體定址模式

```asm
; 直接定址
mov eax, [0x1000]          ; 從位址0x1000讀取

; 間接定址
mov eax, [rbx]            ; 使用RBX作為指標

; 基址+偏移
mov eax, [rbx + 8]        ; 基址+偏移

; 基址+索引*比例+偏移
mov eax, [rbx + rcx*4 + 8]; 陣列存取常用
```

#### 2.4.3 呼叫約定（Calling Convention）

**System V AMD64 ABI（Linux）：**

```
參數傳遞（前6個）：
  第1參數：RDI
  第2參數：RSI
  第3參數：RDX
  第4參數：RCX
  第5參數：R8
  第6參數：R9

返回值：RAX
堆疊对齐：16位元組
```

**範例：呼叫C函數**

```asm
extern printf

section .data
    fmt db "Value: %d", 10, 0

section .text
    global main
main:
    push rbp
    mov rbp, rsp
    
    ; 設定參數
    mov rdi, fmt
    mov rsi, 42
    
    ; 呼叫printf
    call printf
    
    ; 返回
    xor eax, eax
    pop rbp
    ret
```

### 2.5 組譯器原理

#### 2.5.1 組譯器的工作流程

```
原始碼 → 詞彙分析 → 語法分析 → 符號解析 → 目標碼生成 → 目標檔案
```

**兩遍掃描演算法：**

**第一遍：**
1. 讀入所有指令和偽指令
2. 建立符號表（標籤的位址）
3. 處理巨集

**第二遍：**
1. 根據符號表生成機器碼
2. 處理前向引用
3. 輸出目標檔案

#### 2.5.2 目標檔案格式

**ELF（Executable and Linkable Format）結構：**

```
┌─────────────────┐
│ ELF Header      │  - 魔數、架構、入口點
├─────────────────┤
│ Program Header  │  - 段（Segment）資訊
├─────────────────┤
│ Section 1       │  - .text（程式碼）
├─────────────────┤
│ Section 2       │  - .data（已初始化資料）
├─────────────────┤
│ Section 3       │  - .bss（未初始化資料）
├─────────────────┤
│ ...             │  - 其他區段
└─────────────────┘
```

### 2.6 組合語言實作範例

#### 範例1：Hello World

```asm
; hello.asm
; 編譯：nasm -f elf64 hello.asm -o hello.o
; 連結：ld hello.o -o hello
; 執行：./hello

section .data
    hello_msg db "Hello, World!", 10
    hello_len equ $ - hello_msg

section .text
    global _start

_start:
    ; sys_write(fd=1, buf=msg, len=14)
    mov rax, 1              ; sys_write系統呼叫號
    mov rdi, 1              ; stdout
    mov rsi, hello_msg      ; 訊息位址
    mov rdx, hello_len      ; 訊息長度
    syscall
    
    ; sys_exit(status=0)
    mov rax, 60             ; sys_exit系統呼叫號
    xor rdi, rdi            ; 退出碼0
    syscall
```

#### 範例2：陣列總和

```asm
; 計算陣列總和
section .data
    array db 1, 2, 3, 4, 5  ; 5個位元組的陣列
    array_len equ 5

section .text
    global _start

_start:
    xor rax, rax            ; sum = 0
    xor rsi, rsi            ; i = 0

loop:
    cmp rsi, array_len      ; i >= len ?
    jge done                ; 如果是，結束
    
    add al, [array + rsi]   ; sum += array[i]
    inc rsi                ; i++
    jmp loop

done:
    ; 結果在AL中
    mov rax, 60
    xor rdi, rdi
    syscall
```

---

## 第三章：編譯器設計

### 3.1 編譯器概述

編譯器是將高階語言程式翻譯成機器碼的系統軟體。它是系統程式中非常重要的一環。

#### 3.1.1 編譯器的定義

編譯器（Compiler）是一個程式，它將一種語言（源語言）的程式翻譯成另一種語言（目標語言）的等價程式。

```
┌──────────────┐     ┌──────────────┐
│   原始程式   │ ──→ │   編譯器    │ ──→ │   目標程式   │
│  (C/C++)     │     │              │     │   (機器碼)   │
└──────────────┘     └──────────────┘
```

#### 3.1.2 編譯器 vs 直譯器

| 特性 | 編譯器 | 直譯器 |
|------|--------|--------|
| 輸出 | 機器碼 | 不輸出機器碼 |
| 執行方式 | 先翻譯再執行 | 直接執行 |
| 速度 | 快（一次性翻譯） | 慢（逐行翻譯） |
| 除錯 | 較困難 | 較容易 |
| 範例 | GCC, Clang | Python, Ruby |

### 3.2 編譯器架構

#### 3.2.1 整體架構

```
┌──────────────────────────────────────────────────────────────┐
│                        原始程式                              │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                        前端（Frontend）                       │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ 詞彙分析   │→│ 語法分析   │→│ 語意分析   │            │
│  │ (Lexer)    │  │ (Parser)   │  │ (Analyzer) │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                    中間表示（IR）                             │
│  ┌────────────┐  ┌────────────┐                             │
│  │ 最佳化    │→│ 最佳化    │                              │
│  │ (優化器)  │  │ (優化器)  │                              │
│  └────────────┘  └────────────┘                             │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                       後端（Backend）                         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ 指令選擇  │→│ 暫存器    │→│ 目標碼    │            │
│  │           │  │ 分配      │  │ 生成      │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                        目標程式                              │
│                    （機器碼/位元組碼）                         │
└──────────────────────────────────────────────────────────────┘
```

#### 3.2.2 編譯器的階段

1. **詞彙分析**：將程式字元轉換為符號
2. **語法分析**：檢查語法並建立語法樹
3. **語意分析**：進行型別檢查和作用域分析
4. **中間代碼生成**：產生與平台無關的中間表示
5. **最佳化**：改進程式碼效率
6. **目標碼生成**：產生目標機器碼

### 3.3 詞彙分析

#### 3.3.1 詞彙分析器的工作

詞彙分析器（Lexer）將輸入字元流轉換為符號流。

**處理的內容：**

- 識別符號（Identifier）
- 關鍵字（Keyword）
- 運算子（Operator）
- 分隔符（Delimiter）
- 常數（Literal）
- 註解和空白

#### 3.3.2 符號（Token）

符號是詞彙分析的基本單位：

```c
// 原始程式
int x = 10 + 20;

// 符號流
[KW_INT, ID_x, OP_ASSIGN, NUM_10, OP_PLUS, NUM_20, SEMICOLON]
```

**符號的結構：**

```c
struct Token {
    enum TokenType type;  // 符號類型
    char* lexeme;         // 原始字串
    int line;             // 行號
    union {
        int intValue;
        double doubleValue;
        char* stringValue;
    } value;
};
```

#### 3.3.3 正規表示式

正規表示式描述符號的模式：

```regex
Identifier: [a-zA-Z][a-zA-Z0-9]*
Integer:    [0-9]+
Float:      [0-9]+\.[0-9]+
Keyword:    if|else|while|for|int|float|...
Operator:   \+|\-|\*|\/|=|==|<|>|...
```

#### 3.3.4 有限狀態機

有限狀態機（FSM）用於實現詞彙分析器：

```
    ┌───────┐
    │ 初始  │──[字母]──→┌────────┐──[字母/數字]──→┌────────┐
    └───┬───┘          │ 識別符  │                │識別符_OK│
        │              └────┬────┘                └────────┘
        │                   │[數字]
        │                   ↓
        │              ┌─────────┐
    [其他]              │錯誤狀態 │
        ↓              └─────────┘
    ┌───────┐
    │  忽略  │
    └───────┘
```

### 3.4 語法分析

#### 3.4.1 語法分析器的工作

語法分析器（Parser）根據文法規則檢查符號流的語法正確性，並建立語法樹或抽象語法樹（AST）。

**語法樹範例：**

```
原始程式：a = b + c * 2

語法樹：
        =
       / \
      a   +
         / \
        b   *
           / \
          c   2
```

#### 3.4.2 文法表示

**EBNF表示法：**

```ebnf
program        = statement* ;
statement      = assignment | expression ;
assignment     = identifier '=' expression ;
expression     = term (( '+' | '-') term)* ;
term           = factor (( '*' | '/') factor)* ;
factor         = number | identifier | '(' expression ')' ;
identifier     = letter (letter | digit)* ;
number         = digit+ ;
```

#### 3.4.3 語法分析方法

**自上而下分析法：**

- 遞迴下降分析法
- LL(1) 分析法

**自下而上分析法：**

- LR 分析法
- SLR 分析法
- LALR 分析法

**範例：遞迴下降**

```c
// C語言的遞迴下降分析器框架

Token lookahead;

void expr() {
    term();
    while (lookahead == PLUS || lookahead == MINUS) {
        Token op = lookahead;
        match(op);
        term();
        // 生成中間代碼
    }
}

void term() {
    factor();
    while (lookahead == MULT || lookahead == DIV) {
        Token op = lookahead;
        match(op);
        factor();
        // 生成中間代碼
    }
}

void factor() {
    if (lookahead == NUMBER) {
        match(NUMBER);
        // 生成常數節點
    } else if (lookahead == IDENT) {
        match(IDENT);
        // 生成變數節點
    } else if (lookahead == LPAREN) {
        match(LPAREN);
        expr();
        match(RPAREN);
    }
}
```

### 3.5 語意分析

#### 3.5.1 語意分析的工作

語意分析在語法分析的基礎上進行更深層的檢查，確保程式碼的意義是正確的。

**主要任務：**

1. **型別檢查**：確保運算元的型別兼容
2. **作用域解析**：確定每個識別符號的定義位置
3. **識別符號管理**：維護符號表
4. **常數折疊**：在編譯時計算常數表達式

#### 3.5.2 符號表

符號表儲存程式中的識別符號資訊：

```c
struct Symbol {
    char* name;           // 符號名稱
    enum SymbolType type; // 符號類型（函數、變數等）
    DataType dataType;    // 資料型別
    int scope;            // 作用域層級
    int address;          // 記憶體位址或偏移
    // 其他屬性...
};

struct SymbolTable {
    HashTable* table;     // 符號的雜湊表
    int scopeLevel;       // 當前作用域層級
    SymbolTable* parent;  // 父作用域
};
```

#### 3.5.3 型別檢查

**型別相容性規則：**

```c
// 類型檢查範例
Type* checkAssignment(Type* lhs, Type* rhs) {
    if (!lhs || !rhs)
        return NULL;
    
    // 檢查是否完全相同
    if (lhs->kind == rhs->kind)
        return lhs;
    
    // 檢查是否可以隱式轉換
    if (isNumeric(lhs) && isNumeric(rhs))
        return lhs; // 自動提升
    
    // 不相容
    error("type mismatch");
    return NULL;
}
```

### 3.6 中間表示與最佳化

#### 3.6.1 中間表示（IR）

中間表示是介於源語言和目標語言之間的程式表示。

**三地址碼範例：**

```
原始程式：a = b + c * 2

三地址碼：
t1 = c * 2
t2 = b + t1
a = t2
```

**常見的IR形式：**

1. **三地址碼（Three-Address Code）**
2. **靜態單一賦值（SSA）**
3. **控制流圖（CFG）**
4. **虛擬指令（Virtual Instructions）**

#### 3.6.2 常見的最佳化技術

**1. 常數折疊：**

```c
// 優化前
int x = 2 * 3 + 4;    // 結果 = 10

// 優化後
int x = 10;
```

**2. 常數傳播：**

```c
// 優化前
int a = 10;
int b = a + 5;    // a = 10 是常數

// 優化後
int b = 15;
```

**3. 死碼消除：**

```c
// 優化前
int x = 10;
if (0) {
    x = 20;  // 永遠不會執行
}

// 優化後
// x = 10 被保留，x = 20 被移除
```

**4. 迴圈不變量移動：**

```c
// 優化前
for (i = 0; i < n; i++) {
    a[i] = x + 10;  // x + 10 在迴圈中不變
}

// 優化後
t = x + 10;
for (i = 0; i < n; i++) {
    a[i] = t;
}
```

**5. 公共子表達式消除：**

```c
// 優化前
a = b + c;
d = b + c;  // 相同的計算

// 優化後
a = b + c;
d = a;
```

### 3.7 目標碼生成

#### 3.7.1 目標碼生成器的工作

目標碼生成器將最佳化後的中間表示轉換為目標機器的機器碼。

**主要任務：**

1. 指令選擇（Instruction Selection）
2. 暫存器分配（Register Allocation）
3. 指令排程（Instruction Scheduling）

#### 3.7.2 指令選擇

將IR操作對應到目標機器的指令：

```
IR: add t1, t2, t3

x86:   add rax, rbx
ARM:   add r0, r1, r2
```

#### 3.7.3 暫存器分配

**圖著色演算法：**

```c
// 簡化的圖著色概念
// 如果兩個變數同時存活（即都需要儲存），則不能使用同一個暫存器

生命週期分析：
t1: ────●────●──── t1 在 [1,4] 和 [6,7] 存活
t2: ──────●─────── t2 在 [2,5] 存活
t3: ─────────●──── t3 在 [5,8] 存活

圖著色結果：t1=紅, t2=藍, t3=紅（t1和t3可以共享）
```

---

## 第四章：作業系統核心

### 4.1 作業系統概述

#### 4.1.1 什麼是作業系統

作業系統（Operating System）是管理硬體資源並提供服務給應用程式的系統軟體。它作為硬體和應用程式之間的橋樑。

**作業系統的定義：**

1. **資源管理器**：管理CPU、記憶體、I/O設備
2. **服務提供者**：為應用程式提供介面和服務
3. **硬體抽象層**：隱藏硬體細節

#### 4.1.2 作業系統的主要功能

```
┌────────────────────────────────────────────┐
│            使用者應用程式                    │
├────────────────────────────────────────────┤
│            系統呼叫介面                      │
├────────────────────────────────────────────┤
│    ┌─────────┬─────────┬─────────┐        │
│    │ 程序管理│ 記憶體  │ 檔案系統│        │
│    │        │ 管理    │         │        │
│    └─────────┴─────────┴─────────┘        │
├────────────────────────────────────────────┤
│    ┌─────────┬─────────┐                  │
│    │ 設備驅動│ 網路    │                  │
│    │        │ 管理    │                  │
│    └─────────┴─────────┘                  │
├────────────────────────────────────────────┤
│            硬體                              │
└────────────────────────────────────────────┘
```

#### 4.1.3 常見的作業系統

| 作業系統 | 開發者 | 特點 | 應用 |
|----------|--------|------|------|
| Linux | Linus Torvalds | 開源、免費 | 伺服器、嵌入式 |
| Windows | Microsoft | 商業、圖形化 | PC、企業 |
| macOS | Apple | UNIX基礎、設計 | Apple裝置 |
| FreeRTOS | 开源 | 即時、輕量 | 嵌入式 |
| Android | Google | Linux核心、行動 | 手機 |

### 4.2 程序管理

#### 4.2.1 程序的概念

程序（Process）是作業系統資源分配的基本單位。每個程序擁有獨立的：

- 位址空間（虛擬記憶體）
- 開啟的檔案描述符
- 訊號處理器
- 環境變數

```
程序的記憶體布局：
┌─────────────────────┐ 高位址
│       堆疊          │ ← RSP
├─────────────────────┤
│                      │
│        堆           │
├─────────────────────┤
│      未初始化資料   │ ← BSS
├─────────────────────┤
│      已初始化資料   │
├─────────────────────┤
│      程式碼         │
└─────────────────────┘ 低位址
```

#### 4.2.2 程序狀態

**基本狀態：**

```
建立 → 就緒 → 執行 → 阻塞 → 終止
           ↑_________↓
```

- **建立（Created）**：程序正在被建立
- **就緒（Ready）**：等待CPU時間
- **執行（Running）**：正在CPU上執行
- **阻塞（Blocked）**：等待I/O或資源
- **終止（Terminated）**：執行完成

#### 4.2.3 程序控制塊（PCB）

每個程序在核心中有一個PCB：

```c
struct PCB {
    int pid;                    // 程序ID
    ProcessState state;        // 程序狀態
    int priority;             // 排程優先權
    uintptr_t pc;              // 程式計數器
    uintptr_t sp;              // 堆疊指標
    uintptr_t mm;              // 記憶體管理資訊
    struct files* open_files;  // 開啟的檔案
    // ...其他資源
};
```

#### 4.2.4 排程演算法

**1. 先到先服務（FCFS）：**

```
到達順序：P1, P2, P3
執行時間：10, 5, 8

時間線：|--------P1-------|--P2--|--------P3-------|
        0                10     15              23

平均等待時間：(0 + 10 + 15) / 3 = 8.33
```

**2. 最短工作優先（SJF）：**

```
執行時間：P1=10, P2=5, P3=8

排程順序：P2(5) → P3(8) → P1(10)
平均等待時間：(0 + 5 + 13) / 3 = 6
```

**3. 時間片輪轉（RR）：**

```
時間片 = 4
執行時間：P1=10, P2=5, P3=8

時間線：|P1|P2|P3|P1|P3|P1|P1|P1|
        0  4  8 12 16 18 20 22 24

平均等待時間：(0 + 4 + 10 + 12 + 16) / 3 = 14
```

### 4.3 記憶體管理

#### 4.3.1 記憶體管理的目標

1. **隔離**：每個程序有獨立的位址空間
2. **效率**：有效利用記憶體
3. **抽象**：提供簡化的程式設計介面
4. **保護**：防止未授權訪問

#### 4.3.2 分頁系統

分頁將記憶體劃分為固定大小的頁面：

```
虛擬位址：31            12 11         0
         ┌──────────────┬──────────────┐
         │  頁號（VPN） │ 頁內偏移（OFFSET） │
         └──────────────┴──────────────┘

頁表翻譯：
虛擬頁號 → 實體頁號 → 實體位址
   VPN   →   PFN   →  PFN * 4096 + OFFSET
```

**頁表結構：**

```c
struct PageTableEntry {
    uint64_t present : 1;      // 頁是否存在
    uint64_t writable : 1;    // 是否可寫
    uint64_t user : 1;        // 使用者態存取
    uint64_t accessed : 1;    // 是否被訪問
    uint64_t dirty : 1;       // 是否被修改
    uint64_t pfn : 40;        // 實體頁號
    // ...
};
```

#### 4.3.3 虛擬記憶體

虛擬記憶體提供比實際物理記憶體更大的位址空間：

```
┌─────────────────────────────────────┐
│         虛擬位址空間                │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
│  │程式A│ │程式B│ │程式C│ │ ... │  │
│  └─────┘ └─────┘ └─────┘ └─────┘  │
└─────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────┐
│         實體記憶體                   │
│  ┌─────┐ ┌─────┐                   │
│  │ 頁框 │ │ 頁框 │                   │
│  └─────┘ └─────┘                   │
└─────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────┐
│           磁碟（交換區）             │
└─────────────────────────────────────┘
```

#### 4.3.4 記憶體分配策略

**首次適應（First Fit）：**
- 選擇第一個足夠大的空閒區塊
- 速度快，但可能產生碎片

**最佳適應（Best Fit）：**
- 選擇最小的足夠大空閒區塊
- 碎片最少，但搜尋時間長

**最差適應（Worst Fit）：**
- 選擇最大的空閒區塊
- 碎片大，但分配快速

### 4.4 檔案系統

#### 4.4.1 檔案系統的概念

檔案系統提供持久資料儲存的抽象。

**核心概念：**

- **檔案**：命名的資料集合
- **目錄**：組織檔案的層次結構
- ** inode**：檔案的元資料
- **檔案描述符**：程序存取檔案的介面

#### 4.4.2 檔案系統的結構

**UNIX檔案系統布局：**

```
┌──────────────────────────────────────────┐
│            超級區塊（Superblock）         │
│  - 檔案系統大小                           │
│  - 空閒區塊列表                           │
│  - inode表位置                           │
├──────────────────────────────────────────┤
│            inode表                       │
│  - inode 0 (未使用)                      │
│  - inode 1 (根目錄)                      │
│  - inode 2 (檔案)                        │
│  - ...                                   │
├──────────────────────────────────────────┤
│            資料區                        │
│  - 檔案內容                              │
└──────────────────────────────────────────┘
```

**inode結構：**

```c
struct inode {
    mode_t i_mode;          // 檔案類型和權限
    uid_t i_uid;            // 擁有者ID
    off_t i_size;           // 檔案大小
    time_t i_mtime;         // 修改時間
    block_t i_blocks[15];   // 資料區塊指標
    // ...
};
```

#### 4.4.3 常見的檔案系統

| 檔案系統 | 作業系統 | 特點 |
|----------|----------|------|
| ext4 | Linux | 穩定、高效 |
| NTFS | Windows | 日誌、壓縮 |
| HFS+ | macOS | 日誌、加密 |
| FAT32 | 通用 | 簡單、相容 |
| Btrfs | Linux | 快照、RAID |

### 4.5 核心同步

#### 4.5.1 同步的必要性

在多程序/多執行緒環境中，需要同步來保護共享資源。

**問題範例：**

```c
// 兩個執行緒同時修改餘額
// 執行緒1: 讀取餘額(100) → 加50 → 寫回(150)
// 執行緒2: 讀取餘額(100) → 加100 → 寫回(200)
// 結果: 餘額是200，而不是150（ lost update）
```

#### 4.5.2 同步機制

**1. 互斥鎖（Mutex）：**

```c
pthread_mutex_t lock;
int balance;

void deposit(int amount) {
    pthread_mutex_lock(&lock);
    balance += amount;
    pthread_mutex_unlock(&lock);
}
```

**2. 訊號量（Semaphore）：**

```c
sem_t sem;
int resources = 3;

void acquire() {
    sem_wait(&sem);  // 遞減資源計數
}

void release() {
    sem_post(&sem);  // 遞增資源計數
}
```

**3. 條件變數：**

```c
pthread_mutex_t lock;
pthread_cond_t cond;
int ready = 0;

void wait_for_ready() {
    pthread_mutex_lock(&lock);
    while (!ready)
        pthread_cond_wait(&cond, &lock);
    pthread_mutex_unlock(&lock);
}

void signal_ready() {
    pthread_mutex_lock(&lock);
    ready = 1;
    pthread_cond_signal(&cond);
    pthread_mutex_unlock(&lock);
}
```

---

## 第五章：連結器與載入器

### 5.1 目標檔案格式

#### 5.1.1 ELF格式詳解

ELF（Executable and Linkable Format）是Unix/Linux系統的標準目標檔案格式。

**ELF檔案結構：**

```
┌──────────────────────────┐
│  ELF Header              │  魔數、架構、入口點、程式標頭偏移、區段標頭偏移
├──────────────────────────┤
│  Program Header Table    │  執行時需要的身體段
│  (Segment Table)         │
├──────────────────────────┤
│  Section 1: .text       │  程式碼
├──────────────────────────┤
│  Section 2: .data       │  已初始化資料
├──────────────────────────┤
│  Section 3: .bss        │  未初始化資料
├──────────────────────────┤
│  Section 4: .rodata     │  唯讀資料
├──────────────────────────┤
│  Section 5: .symtab     │  符號表
├──────────────────────────┤
│  Section 6: .rel/.rela  │  重工表
├──────────────────────────┤
│  ...                    │
├──────────────────────────┤
│  Section Header Table    │  區段描述
└──────────────────────────┘
```

**ELF Header結構：**

```c
struct Elf64_Ehdr {
    unsigned char e_ident[16]; // 魔數 "ELF"
    uint16_t e_type;          // 檔案類型
    uint16_t e_machine;       // 架構
    uint32_t e_version;       // 版本
    uint64_t e_entry;         // 入口點虛擬位址
    uint64_t e_phoff;         // 程式標頭偏移
    uint64_t e_shoff;         // 區段標頭偏移
    uint32_t e_flags;         // 架構旗標
    uint16_t e_ehsize;       // ELF header大小
    uint16_t e_phentsize;    // 程式標頭大小
    uint16_t e_phnum;        // 程式標頭數量
    // ...
};
```

#### 5.1.2 區段類型

| 區段 | 內容 | 屬性 |
|------|------|------|
| .text | 程式碼 | 可執行、可讀 |
| .data | 已初始化資料 | 可讀、可寫 |
| .bss | 未初始化資料 | 可讀、可寫 |
| .rodata | 常數字串 | 可讀 |
| .symtab | 符號表 | 可讀 |
| .rel/.rela | 重工表 | - |
| .comment | 編譯器資訊 | - |

### 5.2 符號管理

#### 5.2.1 符號的類型

**符號類型：**

```c
enum SymbolType {
    STT_NOTYPE,   // 未定義類型
    STT_OBJECT,   // 資料物件
    STT_FUNC,     // 函數
    STT_SECTION,  // 區段
    STT_FILE,     // 檔案名稱
    STT_TLS,      //執行緒區域儲存
};
```

**符號可見性：**

```c
enum SymbolBinding {
    STB_LOCAL,    // 區域符號
    STB_GLOBAL,   // 全域符號
    STB_WEAK,     // 弱符號
};
```

#### 5.2.2 符號表結構

```c
struct Elf64_Sym {
    uint32_t st_name;   // 符號名稱（字串表索引）
    unsigned char st_info;  // 類型和綁定
    unsigned char st_other; // 其它
    uint16_t st_shndx;  // 所屬區段
    uint64_t st_value;  // 位址或偏移
    uint64_t st_size;   // 大小
};
```

### 5.3 重定位

#### 5.3.1 重定位的概念

重工將相對位址調整為最終的執行位址。

**重工類型：**

```c
// x86-64常見重工類型
enum {
    R_X86_64_NONE,      // 無重工
    R_X86_64_64,        // 64位元絕對位址
    R_X86_64_PC32,      // 32位元相對PC
    R_X86_64_GOTPCREL,  // GOT相對位址
    R_X86_64_PLT32,     // PLT相對位址
};
```

#### 5.3.2重工表結構

```c
struct Elf64_Rela {
    uint64_t r_offset;  // 需要重工的位置
    uint64_t r_info;    // 符號索引和重工類型
    int64_t r_addend;   // 增加值
};
```

**重工過程範例：**

```asm
; 原始目標檔案中的指令
mov eax, [relocatable + 0]  ; relocatable是未解析的符號

; 連結後（假設relocatable在0x00401000）
mov eax, [rip + 0x1000]     ; 或
mov eax, [0x00401000]       ; 絕對位址
```

### 5.4 靜態連結

#### 5.4.1 連結器的工作

連結器（Linker）將多個目標檔案合併為單一可執行檔案：

1. **符號解析**：解析所有符號引用
2. **重工處理**：計算並應用重工
3. **區段合併**：合併同類區段
4. **位址分配**：分配段和符號位址
5. **符號重排**：優化排列

#### 5.4.2 連結過程

```
目標檔案1.o  ─┐
目標檔案2.o  ─┼─→ 連結器 → 可執行檔案
庫lib.a      ─┘
```

**連結器指令範例：**

```bash
# 編譯
gcc -c main.c -o main.o
gcc -c foo.c -o foo.o

# 連結（靜態）
ld main.o foo.o -o program

# 或使用gcc自動連結
gcc main.o foo.o -o program
```

### 5.5 動態連結

#### 5.5.1 動態連結的概念

動態連結在執行時解析符號，不需要將庫代碼包含在執行檔中。

**優點：**
- 多個程式共享同一庫，節省記憶體
- 庫更新不需要重新連結
- 允許動態載入

**缺點：**
- 啟動速度可能較慢
- 需要確保庫存在
- 可能遇到版本問題

#### 5.5.2 共享庫

**共享庫的建立：**

```bash
# 建立共享庫
gcc -fPIC -shared -o libfoo.so foo.c

# 使用共享庫連結
gcc -o program main.c -L. -lfoo
```

**環境變數：**

```bash
# 指定庫搜尋路徑
export LD_LIBRARY_PATH=/path/to/lib:$LD_LIBRARY_PATH

# 顯示載入的庫
ldd program
```

#### 5.5.3 延遲連結

延遲連結（Lazy Binding）推遲符號解析直到函數第一次被調用：

```asm
; PLT條目（延遲綁定）
push index           ; 函數索引
jmp [GOT + offset]  ; 跳轉到GOT
```

### 5.6 載入器

#### 5.6.1 載入器的職責

載入器負責將可執行檔案載入記憶體並開始執行：

1. 驗證檔案格式
2. 建立虛擬記憶體空間
3. 映射程式碼和資料
4. 設定堆疊
5. 初始化動態連結器
6. 跳轉到入口點

#### 5.6.2 載入過程

```
ELF Header → Program Header → 映射段 → 設定環境 → 執行
```

**記憶體映射：**

```
虛擬位址空間：
┌──────────────────────────┐ 0xFFFFFFFFFFFFFFFF
│                          │
├──────────────────────────┤
│      堆疊                │ ← 高位址， RSP
│          ↓               │
├──────────────────────────┤
│                          │
│      堆                  │
├──────────────────────────┤
│      .bss                │
├──────────────────────────┤
│      .data               │
├──────────────────────────┤
│      .text               │
├──────────────────────────┤
│      載入基址            │
└──────────────────────────┘ 0x0000000000400000
```

---

## 第六章：系統工具與程式開發

### 6.1 版本控制系統

#### 6.1.1 Git基礎

Git是目前的分散式版本控制系統。

**基本概念：**

```
工作目錄 → 暫存區（Staging） → 本地倉庫 → 遠端倉庫
```

**常用命令：**

```bash
# 初始化
git init

# 克隆
git clone https://github.com/user/repo.git

# 添加檔案
git add .
git add filename

# 提交
git commit -m "commit message"

# 推送
git push origin master

# 拉取
git pull origin master

# 分支
git checkout -b feature-branch
git checkout main
git merge feature-branch
```

#### 6.1.2 分支策略

**Git Flow：**

```
main ─────●────────●────────●────
         \        \        \
          \        \        \
feature   ●────────●────────●──
```

- main：穩定版本
- develop：開發分支
- feature/*：功能分支
- release/*：發布分支
- hotfix/*：熱修復分支

### 6.2 自動化建置

#### 6.2.1 Makefile

Make是經典的建置工具。

**基本語法：**

```makefile
# 變數
CC = gcc
CFLAGS = -Wall -g

# 目標
all: program

program: main.o foo.o bar.o
    $(CC) $(CFLAGS) -o program main.o foo.o bar.o

main.o: main.c
    $(CC) $(CFLAGS) -c main.c

foo.o: foo.c
    $(CC) $(CFLAGS) -c foo.c

clean:
    rm -f *.o program
```

#### 6.2.2 CMake

CMake是跨平台的建置系統。

**CMakeLists.txt：**

```cmake
cmake_minimum_required(VERSION 3.10)
project(MyProgram)

set(CMAKE_CXX_STANDARD 17)

add_executable(program main.cpp foo.cpp)

target_include_directories(program PRIVATE include)

find_package(Threads REQUIRED)
target_link_libraries(program Threads::Threads)
```

### 6.3 調試工具

#### 6.3.1 GDB基本使用

GDB是Linux下的命令列調試器。

**基本命令：**

```bash
# 啟動
gdb ./program

# 執行
run [args]          # 開始執行
continue            # 繼續執行
step                # 單步執行（進入函數）
next                # 單步執行（不進入函數）
finish              # 執行到函數返回

# 斷點
break function      # 設定函數斷點
break file:line     # 設定行號斷點
info breakpoints    # 查看斷點
delete n            # 刪除斷點

# 檢視
print var           # 顯示變數
backtrace           # 顯示堆疊
info locals         # 顯示區域變數
x/20x addr          # 檢視記憶體

# 修改变量
set var = value
```

**實際操作範例：**

```bash
(gdb) break main
Breakpoint 1 at 0x4005ed: file main.c, line 10.
(gdb) run
Starting program: ./program

Breakpoint 1, main () at main.c:10
10        int x = 5;
(gdb) next
11        int y = 10;
(gdb) print x
$1 = 5
(gdb) set x = 20
(gdb) continue
```

#### 6.3.2 Valgrind

Valgrind是記憶體錯誤檢測工具。

```bash
# 記憶體檢查
valgrind --leak-check=full ./program

# 輸出範例：
==12345== Memcheck, a memory error detector
==12345== Copyright (C) 2002-2013, and GNU GPL'd, by Julian Seward et al.
==12345== Using Valgrind-3.10.1 and LibVEX; rerun with: -h for copyright
==12345== Command: ./program
==12345== 
==12345== HEAP SUMMARY:
==12345==   in use at exit: 0 bytes in 0 blocks
==12345==   total heap usage: 1 allocs, 1 frees, 100 bytes allocated
==12345== 
==12345== All heap blocks were freed -- no leaks are possible
```

### 6.4 效能分析

#### 6.4.1 perf工具

perf是Linux核心的效能分析工具。

```bash
# 基本用法
perf stat ./program         # 統計資訊
perf record ./program       # 記錄事件
perf report                 # 顯示報告

# 熱點分析
perf top                    # 即時熱點

# 自定義事件
perf record -e cache-misses ./program
```

#### 6.4.2 gprof

GCC的效能分析工具。

```bash
# 編譯時加上 -pg
gcc -pg -o program main.c

# 執行
./program

# 產生分析報告
gprof program gmon.out > profile.txt
```

### 6.5 測試框架

#### 6.5.1 C單元測試框架

**Assert風格：**

```c
#include <assert.h>
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

void test_add() {
    assert(add(1, 2) == 3);
    assert(add(-1, 1) == 0);
    assert(add(0, 0) == 0);
    printf("add tests passed\n");
}

int main() {
    test_add();
    return 0;
}
```

#### 6.5.2 Google Test（C++）

```cpp
#include <gtest/gtest.h>

int add(int a, int b) {
    return a + b;
}

TEST(AddTest, PositiveNumbers) {
    EXPECT_EQ(add(1, 2), 3);
}

TEST(AddTest, NegativeNumbers) {
    EXPECT_EQ(add(-1, 1), 0);
}

int main(int argc, char** argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
```

---

## 第七章：系統安全基礎

### 7.1 記憶體安全

#### 7.1.1 緩衝區溢位

緩衝區溢位是最常見的安全漏洞。

**範例：**

```c
// 不安全的程式
void vulnerable(char* str) {
    char buffer[10];
    strcpy(buffer, str);  // 沒有邊界檢查！
}

// 攻擊：
// "AAAAAAA..." 會覆蓋返回位址
```

**防御措施：**

```c
// 安全版本
void safe(char* str) {
    char buffer[10];
    strncpy(buffer, str, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';
}
```

#### 7.1.2 常見的記憶體漏洞

| 漏洞類型 | 描述 | 範例 |
|----------|------|------|
| Buffer Overflow | 寫入超出緩衝區 | strcpy |
| Heap Overflow | 堆記憶體溢出 | 無限malloc |
| Use-after-free | 使用已釋放記憶體 | double free |
| Double-free | 釋放已釋放記憶體 | 錯誤的free順序 |
| Format String | 格式化字串漏洞 | printf(user_input) |

#### 7.1.3 安全機制

**Stack Canaries：**

```
原始堆疊：    [返回位址] [框架指標] [區域變數]
加canary：    [canary] [返回位址] [框架指標] [區域變數]
                    ↑
                編譯時插入，運行時檢查
```

**ASLR（位址空間隨機化）：**

```
隨機化：每次執行的位址不同
- 程式碼段基址
- 堆疊位置
- 函式庫位置
```

**DEP/NX（資料執行保護）：**

- 標記記憶體區域為不可執行
- 防止在資料區域執行shellcode

### 7.2 權限管理

#### 7.2.1 Unix/Linux權限模型

**基本權限：**

```bash
-rw-r--r-- 1 user group 1234 Jan 1 12:00 file
↑  ↑  ↑  ↑
擁有者 群組 其他人
```

**權限數值：**

- r（讀）= 4
- w（寫）= 2
- x（執行）= 1

```bash
# 範例
chmod 755 file     # rwxr-xr-x
chmod 644 file     # rw-r--r--
```

#### 7.2.2 特殊權限

```bash
# SetUID
chmod u+s program  # -rwsr-xr-x

# SetGID
chmod g+s directory

# Sticky bit
chmod +t directory
```

### 7.3 加密基礎

#### 7.3.1 對稱加密

**AES（Advanced Encryption Standard）：**

```c
// OpenSSL AES加密範例
#include <openssl/aes.h>

void encrypt(unsigned char* plaintext, unsigned char* key, 
             unsigned char* ciphertext) {
    AES_KEY aes_key;
    AES_set_encrypt_key(key, 256, &aes_key);
    AES_encrypt(plaintext, ciphertext, &aes_key);
}
```

#### 7.3.2 非對稱加密

**RSA：**

```c
// RSA金鑰生成
EVP_PKEY* generate_key() {
    EVP_PKEY_CTX* ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_RSA);
    EVP_PKEY_keygen_init(ctx);
    EVP_PKEY_CTX_set_rsa_keygen_bits(ctx, 2048);
    EVP_PKEY* key = NULL;
    EVP_PKEY_keygen(ctx, &key);
    return key;
}
```

#### 7.3.3 雜湊函數

```c
// SHA-256
#include <openssl/sha.h>

unsigned char* hash_data(unsigned char* data, size_t len) {
    static unsigned char digest[SHA256_DIGEST_LENGTH];
    SHA256(data, len, digest);
    return digest;
}
```

### 7.4 安全編程實踐

#### 7.4.1 輸入驗證

```c
// 不安全
char cmd[100];
sprintf(cmd, "ls %s", user_input);
system(cmd);

// 安全
if (!is_valid_filename(user_input)) {
    error("Invalid input");
    return;
}
```

#### 7.4.2 安全的字串處理

```c
// 使用安全的函數
strncpy(dest, src, n);     // 替代 strcpy
strncat(dest, src, n);     // 替代 strcat
snprintf(buf, size, fmt,); // 替代 sprintf
```

---

## 第八章：進階主題

### 8.1 虛擬化技術

#### 8.1.1 虛擬化概念

虛擬化在一台物理機器上運行多個虛擬機器。

**Hypervisor類型：**

- **Type-1（原生）**：直接運行在硬體上
  - VMware ESXi
  - Xen
  - Hyper-V
  
- **Type-2（托管）**：運行在作業系統上
  - VirtualBox
  - VMware Workstation
  - QEMU

#### 8.1.2 CPU虛擬化

硬體輔助虛擬化：
- Intel VT-x
- AMD-V

#### 8.1.3 容器

容器比虛擬機更輕量，共享主機核心：

```dockerfile
# Dockerfile範例
FROM ubuntu:20.04
RUN apt-get update
COPY . /app
WORKDIR /app
CMD ["python", "app.py"]
```

### 8.2 雲端運算

#### 8.2.1 雲端服務模型

| 模型 | 提供內容 | 範例 |
|------|----------|------|
| IaaS | 虛擬機器 | AWS EC2 |
| PaaS | 執行環境 | Heroku |
| SaaS | 完整應用 | Gmail |

#### 8.2.2 雲端部署模式

- 公有雲
- 私有雲
- 混合雲

### 8.3 即時系統

#### 8.3.1 即時系統特性

- **硬即時**：必須在期限內完成
- **軟即時**：期限後效能下降

#### 8.3.2 常用RTOS

- FreeRTOS
- VxWorks
- RT-Thread
- QNX

### 8.4 嵌入式系統

#### 8.4.1 嵌入式系統特點

- 資源受限
- 即時性要求
- 低功耗
- 可靠性要求高

#### 8.4.2 微控制器

常見的ARM Cortex-M系列：
- Cortex-M0/M0+
- Cortex-M3
- Cortex-M4
- Cortex-M7

### 8.5 分散式系統

#### 8.5.1 基礎概念

- 節點（Node）
- 網路通訊
- 一致性模型

#### 8.5.2 共識演算法

- Paxos
- Raft

---

## 實作練習

### 練習1：組合語言 Hello World

**目標**：編寫並執行一個組合語言程式

**步驟**：

1. 建立 `hello.asm`
2. 使用NASM組譯
3. 使用LD連結
4. 執行並驗證輸出

### 練習2：簡易編譯器

**目標**：實作一個簡單的計算機表達式編譯器

**步驟**：

1. 實作詞彙分析器
2. 實作語法分析器（遞迴下降）
3. 生成三地址碼

### 練習3：程序管理

**目標**：使用系統呼叫管理程序

**步驟**：

1. 使用 fork() 建立子程序
2. 使用 exec() 執行新程式
3. 使用 wait() 等待子程序

### 練習4：記憶體管理

**目標**：理解虛擬記憶體

**步驟**：

1. 使用 mmap() 映射記憶體
2. 觀察分頁行為
3. 實現簡單的記憶體池

### 練習5：連結器

**目標**：理解目標檔案和連結

**步驟**：

1. 使用 objdump 分析目標檔案
2. 使用 readelf 檢視 ELF 結構
3. 實作簡單的符號解析

---

## 常見問題

**Q1：學習系統程式需要什麼基礎？**
A：需要C語言基礎、資料結構和演算法知識。

**Q2：組合語言好難學，有什麼建議？**
A：從簡單的範例開始，逐步理解暫存器和記憶體模型。

**Q3：編譯器開發需要多長時間？**
A：取決於複雜度，簡單的編譯器可能需要數週。

**Q4：如何在Linux上調試核心？**
A：可以使用QEMU模擬，或者使用KGDB進行遠端調試。

---

## 學習資源

### 書籍

1. 《Computer Systems: A Programmer's Perspective》- Bryant & O'Hallaron
2. 《Operating System Concepts》- Silberschatz
3. 《Compilers: Principles, Techniques, and Tools》- Aho, Sethi, Ullman（龍書）
4. 《Linux Device Drivers》- Corbet, Rubini, Kroah-Hartman

### 線上資源

1. MIT 6.033（作業系統）
2. Stanford CS107（系統程式設計）
3. gcc.gnu.org（GCC文檔）
4. elfutils.github.io（ELF格式）

### 實作工具

1. GCC/Clang - C/C++編譯器
2. NASM - 組譯器
3. GDB - 調試器
4. Valgrind - 記憶體分析
5. perf - 效能分析

---

## 結語

系統程式設計是電腦科學的核心領域，它幫助我們理解電腦的運作原理。本書涵蓋了系統程式的基礎知識，從組合語言到編譯器，從作業系統到連結器。這些知識將幫助你成為更好的程式設計師。

持續學習和實踐是掌握系統程式的關鍵。建議讀者動手實作每一章的練習，並嘗試修改現有的開源專案來加深理解。

---

*本書內容適用於初學者至中階讀者，涵蓋系統程式設計的核心概念與實踐。*