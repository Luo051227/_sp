# p0 編譯器 - 函數呼叫機制詳解

這份文件詳細說明 p0 編譯器的運作原理，特別是**函數呼叫機制**是如何實現的。

---

## 目錄

1. [編譯器架構概述](#1-編譯器架構概述)
2. [詞法分析 (Lexer)](#2-詞法分析-lexer)
3. [語法解析 (Parser)](#3-語法解析-parser)
4. [虛擬機 (VM) - 函數呼叫機制](#4-虛擬機---函數呼叫機制)
5. [while 迴圈的編譯](#5-while-迴圈的編譯)
6. [完整範例](#6-完整範例)
7. [動手練習](#7-動手練習)

---

## 1. 編譯器架構概述

```
原始碼 (source code)
       │
       ▼
┌──────────────────┐
│  詞法分析 (Lexer) │  → 將字元串轉換為 Token 串
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ 語法解析 (Parser) │  → 產生中間碼 (Quadruples)
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ 虛擬機 (VM)      │  → 執行中間碼
└──────────────────┘
```

### 什麼是四元組 (Quadruples)？

四元組是中間碼的一種格式：
```
(運算碼, 運算元1, 運算元2, 結果)
```

例如：
```
ADD t1, t2, t3    →  把 t1 + t2 的結果存入 t3
CALL foo, 2, t4  →  呼叫 foo 函數，傳入 2 個參數，回傳值存入 t4
```

---

## 2. 詞法分析 (Lexer)

### 什麼是 Lexer？

Lexer 就像是一個**切字機**，把一連串的字元切成一個個有意義的**Token**。

### 範例

原始碼：
```
func add(a, b) {
    return a + b;
}
```

經過 Lexer 切割後：
```
FUNC    "func"
ID      "add"
LPAREN  "("
ID      "a"
COMMA   ","
ID      "b"
RPAREN  ")"
LBRACE  "{"
RETURN  "return"
ID      "a"
PLUS    "+"
ID      "b"
SEMICOLON ";"
RBRACE  "}"
EOF
```

### Python 實作

```python
class Lexer:
    def get_next_token(self):
        # 1. 跳過空白和註解
        # 2. 辨識數字 → NUM
        # 3. 辨識識別碼/關鍵字 → ID / FUNC / RETURN / IF / WHILE
        # 4. 辨識運算符 → + - * / = == < >
        # 5. 辨識符號 → ( ) { } , ;
```

---

## 3. 語法解析 (Parser)

### 遞迴下降法

Parser 使用**遞迴下降法**，這是一種 top-down 的解析方法。

```
表達式層級（從高到低）：

expression     → 比較運算 (==, <, >, !=, <=, >=)
arith_expr     → 加減 (+, -)
term           → 乘除 (*, /)
factor         → 基礎單元 (數字、變數、函數呼叫、括號)
```

### 解析流程範例

對於 `a + b * c`：

1. **expression** 呼叫 **arith_expr**
2. **arith_expr** 呼叫 **term**
3. **term** 呼叫 **factor**，得到 `a`
4. 遇到 `+`，**arith_expr** 繼續呼叫 **term**
5. **term** 呼叫 **factor**，得到 `b`
6. 遇到 `*`，繼續呼叫 **factor**，得到 `c`
7. **term** 產生 `MUL b, c, t1`
8. **arith_expr** 產生 `ADD a, t1, t2`

---

## 4. 虛擬機 (VM) - 函數呼叫機制

### 這是最重要的部分！

函數呼叫機制是透過**堆疊幀 (Stack Frame)** 實現的。

### 生活中的比喻

想象一家餐廳：
- **全域環境** (Frame 0) = 餐廳大廳
- **函數環境** = 包廂
- 進入函數 = 進入包廂
- 離開函數 = 離開包廂，回到大廳

每個包廂都是獨立的空間，裡面的客人 (變數) 不會影響其他包廂。

### 堆疊幀的結構

```python
class Frame:
    names: OrderedDict    # 區域變數 (a=1, b=2)
    ret_pc: int           # 回去後要繼續執行的行號
    ret_var: str          # 回傳值要存入哪個變數
    incoming_args: list   # 傳進來的參數
```

### 函數呼叫的步驟

假設我們要呼叫 `add(1, 2)`：

#### 步驟 1：編譯時期產生的指令

```python
# 編譯器產生的中間碼：
PARAM 1, -, -
PARAM 2, -, -
CALL add, 2, t3    # 呼叫 add，傳入 2 個參數，回傳值存入 t3
```

#### 步驟 2：執行 CALL 指令

```python
elif q.op == 'CALL':
    # 1. 找到函數的進入點
    target_pc = func_table[q.arg1]  # 例如：找到 add 函數在第 10 行
    
    # 2. 建立新的堆疊幀 (Frame)
    sp += 1  # 進入新環境
    stack.append(Frame())
    
    # 3. 記住回來的位置
    stack[sp].ret_pc = pc + 1  # 執行完後回到 CALL 的下一行
    
    # 4. 記住回傳值要存哪裡
    stack[sp].ret_var = q.result  # 存到 t3
    
    # 5. 把參數傳遞過去
    param_count = int(q.arg2)  # 2 個參數
    stack[sp].incoming_args = [1, 2]
    
    # 6. 跳到函數去執行
    pc = target_pc
    continue
```

#### 步驟 3：執行函數內容

```python
# 執行 add 函數的內容：
# FUNC_BEG add
# FORMAL a, -, -    # 把 incoming_args[0] = 1 存入 a
# FORMAL b, -, -    # 把 incoming_args[1] = 2 存入 b
# IMM 1, -, t1      # t1 = 1
# IMM 2, -, t2      # t2 = 2
# ADD t1, t2, t3    # t3 = t1 + t2 = 3
# RET_VAL t3, -, -  # 回傳 t3 的值 (3)
```

#### 步驟 4：執行 RET_VAL 指令

```python
elif q.op == 'RET_VAL':
    # 1. 取出回傳值
    ret_val = get_var(q.arg1)  # 3
    
    # 2. 記住要回去的位置
    ret_pc = stack[sp].ret_pc  # CALL 的下一行
    
    # 3. 記住回傳值要存哪
    ret_var = stack[sp].ret_var  # t3
    
    # 4. 銷毀當前堆疊幀 (回到父環境)
    sp -= 1
    
    # 5. 把回傳值寫回父環境
    set_var(ret_var, ret_val)  # t3 = 3
    
    # 6. 跳回原來的位置
    pc = ret_pc
    continue
```

### 完整流程圖

```
 Caller (Frame 0)                    Callee (Frame 1)
 ──────────────────                 ──────────────────
 
 1. PARAM 1
 2. PARAM 2           ──────────>   (建立新 Frame)
 3. CALL add ───────────────────>   (設定 ret_pc=4, ret_var=t3)
                      (傳遞參數)     (設定 incoming_args=[1,2])
                                    
                                    (執行函數本體)
                                    (遇到 RET_VAL)
                      <─────────── 回傳值 3
 4. t3 = 3            (回到 Frame 0) (銷毀 Frame 1)
```

### 為什麼需要堆疊幀？

1. **隔離變數作用域**：每個函數的區域變數不會互相影響
2. **支援遞迴**：同樣的函數可以同時執行多次（如 fibonacci）
3. **記住回來的位置**：執行完後知道要回到哪裡繼續

---

## 5. while 迴圈的編譯

### while 語法

```
while (條件) {
    陳述句;
}
```

### 編譯原理

```python
# 假設 while (x < 10) { ... }

# 1. 記錄迴圈開始位置
loop_start = 5   # 假設這裡是 while 的開始

# 2. 產生條件判斷
# 假設 x < 10 編譯成 CMP_LT x, 10, t1
emit('CMP_LT', 'x', '10', 't1')

# 3. 條件為 false 時跳出迴圈
jmp_out = 目前的位置
emit('JMP_F', 't1', '-', '?')  # ? 以後會回填

# 4. 執行迴圈內容
... (其他陳述句)

# 5. 跳回迴圈開始
emit('JMP', '-', '-', str(loop_start))

# 6. 回填跳出位置
quads[jmp_out].result = str(目前位置)
```

### 範例

原始碼：
```
x = 0;
while (x < 3) {
    x = x + 1;
}
```

編譯結果：
```
00: IMM     0         -         x
02: CMP_LT  x         3         t1
04: JMP_F   t1        -         09      # 如果 x >= 3，跳到 09
06: IMM     1         -         t2
07: ADD     x         t2        t3
08: STORE   t3        -         x
09: JMP     -         -         02      # 跳回 02 判斷條件
```

執行流程：
```
x=0 → 判斷 0<3=真 → x=1 → 判斷 1<3=真 → x=2 → 判斷 2<3=真 → x=3 → 判斷 3<3=假 → 結束
```

---

## 6. 完整範例

### 測試程式

建立 `test.txt`：
```
func fib(n) {
    if (n < 2) {
        return n;
    }
    return fib(n-1) + fib(n-2);
}

result = fib(5);
```

### 執行方法

```bash
python 1.py test.txt
```

### 輸出結果

```
原始碼:
----------------------------------------
func fib(n) {
    if (n < 2) {
        return n;
    }
    return fib(n-1) + fib(n-2);
}

result = fib(5);

----------------------------------------

編譯器生成的中間碼 (PC: Quadruples):
----------------------------------------
000: FUNC_BEG fib         -          -
001: FORMAL   n           -          -
002: CMP_LT   n           2          t1
003: JMP_F    t1          -          006
004: RET_VAL  n           -          -
005: IMM      1           -          t2
006: SUB      n           t2         t3
007: PARAM    t3          -          -
008: IMM      2           -          t4
009: SUB      n           t4         t5
010: PARAM    t5          -          -
011: CALL     fib         2          t6
012: CALL     fib         2          t7
013: ADD      t6          t7         t8
014: RET_VAL  t8          -          -
015: FUNC_END fib         -          -
016: CALL     fib         1          t9
017: STORE    t9          -          result

=== VM 執行開始 ===
=== VM 執行完畢 ===

全域變數結果:
>> result = 5
```

---

## 7. 動手練習

### 練習 1：基本運算

```python
a = 10;
b = 20;
c = a + b;
```

### 練習 2：函數呼叫

```python
func double(x) {
    return x * 2;
}

y = double(5);
```

### 練習 3：while 迴圈

```python
i = 0;
sum = 0;
while (i < 10) {
    sum = sum + i;
    i = i + 1;
}
```

### 練習 4：遞迴（經典費波那契）

```python
func fib(n) {
    if (n < 2) {
        return n;
    }
    return fib(n-1) + fib(n-2);
}

result = fib(10);
```

---

## 總結

| 元件 | 功能 |
|------|------|
| **Lexer** | 將原始碼切分成 Token |
| **Parser** | 產生四元組中間碼 |
| **VM** | 執行四元組，實現函數呼叫 |
| **Stack Frame** | 隔離變數，支援遞迴 |

這個編譯器雖然簡單，但包含了所有編譯器的核心概念：
1. 詞法分析 → 語法分析 → 語意分析 → 程式生成 → 執行

學會這些概念後，你就能理解真正的編譯器是如何運作的了！