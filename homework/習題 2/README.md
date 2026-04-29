# SimpleScript 程式語言 - 從零開始的完整指南

> 這是一個專為初學者設計的程式語言專案，讓你了解程式語言是如何運作的！

---

## 目錄

1. [什麼是 SimpleScript？](#一什麼是-simplescript)
2. [為什麼要學這個？](#二為什麼要學這個)
3. [語言語法 - 怎麼寫程式](#三語言語法---怎麼寫程式)
4. [程式碼範例 - 從範例學習](#四程式碼範例---從範例學習)
5. [直譯器是什麼？它是怎麼運作的？](#五直譯器是什麼它是怎麼運作的)
6. [如何執行 SimpleScript 程式](#六如何執行-simplescript-程式)
7. [常見問題](#七常見問題)

---

## 一、什麼是 SimpleScript？

### 1.1 簡單介紹

SimpleScript 是我們自己設計的一種**程式語言**！就像英語有語法規則一樣，程式語言也有自己的規則。

**想一想**：當你跟電腦說「幫我計算 1+1」的時候，電腦聽得懂嗎？當然聽不懂！所以我們需要一種電腦能懂的語言，這就是程式語言。

SimpleScript 的目標是：
- ✅ **很簡單**：語法很容易學，就像學英文一樣
- ✅ **很安全**：寫錯了會告訴你哪裡錯
- ✅ **很有趣**：可以拿來寫各種小程式

### 1.2 這個語言能做什麼？

```
┌─────────────────────────────────────────────────────────┐
│                   SimpleScript 能做的事                  │
├─────────────────────────────────────────────────────────┤
│  ✓ 計算數學 (1 + 2 * 3)                                 │
│  ✓ 儲存資料 (let x: int = 10)                          │
│  ✓ 判斷條件 (if x > 5 { ... })                          │
│  ✓ 迴圈執行 (for i = 1, 10, 1 { ... })                  │
│  ✓ 函數封裝 (fn add(a: int, b: int) -> int { ... })     │
│  ✓ 陣列操作 (let nums: array<int> = [1, 2, 3])          │
│  ✓ 模組匯入 (import "utils.ss")                         │
└─────────────────────────────────────────────────────────┘
```

### 1.3 技術規格（讓你了解一下）

| 項目 | 說明 | 簡單解釋 |
|------|------|----------|
| **型別系統** | 強型態 (Strong Typing) | 變數有固定的類型，不能混用 |
| **執行模式** | 直譯器 (Interpreter) | 讀一行執行一行，不用先編譯 |
| **記憶體管理** | 參考計數 GC | 自動回收不需要的記憶體 |
| **實作語言** | Python 3 | 用 Python 寫的直譯器 |

---

## 二、為什麼要學這個？

### 2.1 學會這個，你會得到什麼？

```
     ┌──────────────────────────────────────┐
     │       學會程式語言設計的好處          │
     └──────────────────────────────────────┘
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
  了解電腦        學習程式設計        更好除錯
  如何運作        的核心概念        程式問題
      │               │               │
      ▼               ▼               ▼
  變得更厲害！     寫出更好的程式！    解決問題更快！
```

### 2.2 什麼是「直譯器」？什麼是「編譯器」？

**簡單比喻**：

```
📝 編譯器 (Compiler)：
   就像翻譯一本書 entire book
   - 把整本書翻譯完才能看
   - 翻譯時間長，但執行快速
   - 例子：C、C++、Go

📝 直譯器 (Interpreter)：
   就像同聲傳譯
   - 邊聽邊翻譯，馬上就能用
   - 啟動快，但執行較慢
   - 例子：Python、JavaScript、SimpleScript
```

### 2.3 我們的語言是直譯器！

```
使用者寫的程式 (.ss 檔案)
        │
        ▼
    ┌─────────────┐
    │  詞彙分析   │  ← 辨認每個字是什麼
    │  (Lexer)   │
    └─────────────┘
        │
        ▼
    ┌─────────────┐
    │  語法分析   │  ← 檢查語法對不對
    │  (Parser)   │
    └─────────────┘
        │
        ▼
        AST (抽象語法樹)
        │
        ▼
    ┌─────────────┐
    │  直譯器    │  ← 執行指令
    │(Interpreter)│
    └─────────────┘
        │
        ▼
     輸出結果！
```

---

## 三、語言語法 - 怎麼寫程式

### 3.1 基本語法規則

#### 🔸 變數宣告

```simplescript
// 語法：let 變數名稱 : 類型 = 值;

// 整數
let age: int = 20;

// 浮點數
let height: float = 175.5;

// 字串
let name: string = "王小明";

// 布林值
let isStudent: bool = true;

// 陣列
let numbers: array<int> = [1, 2, 3, 4, 5];
```

**💡 小提醒**：
- `//` 後面是註解，不會被執行
- 每行結尾要加 `;`（分號）
- 變數名稱不能是 `if`、`while`、`fn` 這些關鍵字

#### 🔸 資料類型

| 類型 | 說明 | 範例 |
|------|------|------|
| `int` | 整數 | `10`, `0`, `-5` |
| `float` | 浮點數 | `3.14`, `1.5` |
| `string` | 字串 | `"Hello"` |
| `bool` | 布林值 | `true`, `false` |
| `array<類型>` | 陣列 | `[1, 2, 3]` |

#### 🔸 運算子

```simplescript
// 算術運算
let a: int = 10 + 5;    // 加法 = 15
let b: int = 10 - 5;    // 減法 = 5
let c: int = 10 * 5;    // 乘法 = 50
let d: int = 10 / 5;    // 除法 = 2
let e: int = 10 % 3;    // 取餘數 = 1

// 比較運算
let x: bool = 10 > 5;   // 大於 = true
let y: bool = 10 == 10; // 等於 = true
let z: bool = 10 != 5;  // 不等於 = true

// 邏輯運算
let result: bool = true and false;  // 且 = false
let result2: bool = true or false;   // 或 = true
let result3: bool = not true;         // 非 = false
```

#### 🔸 條件判斷 (if / elif / else)

```simplescript
let score: int = 85;

if score >= 90 {
    print("成績：A");
} elif score >= 80 {
    print("成績：B");
} elif score >= 70 {
    print("成績：C");
} else {
    print("成績：不及格");
}
```

#### 🔸 迴圈 (while / for)

```simplescript
// while 迴圈
let i: int = 0;
while i < 5 {
    print(i);
    i = i + 1;
}

// for 迴圈
// 語法：for 變數 = 開始, 結束, 間隔 { }
for i = 0, 10, 1 {
    print(i);  // 會印出 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
}
```

#### 🔸 函數

```simplescript
// 定義函數
fn sayHello(name: string) -> void {
    print("你好，" + name + "！");
}

// 呼叫函數
sayHello("王小明");

// 有返回值的函數
fn add(a: int, b: int) -> int {
    return a + b;
}

let result: int = add(10, 20);
print(result);  // 印出 30
```

### 3.2 EBNF 語法 - 這是什麼？

**EBNF** 是一種用來描述程式語言語法的「文法」。就像英文的文法規則告訴你怎麼組成句子，EBNF 告訴你怎麼組成程式。

```
📝 簡單解釋：

letter      = "A".."Z" | "a".."z" ;    → 字母可以是 A-Z 或 a-z
digit       = "0".."9" ;               → 數字可以是 0-9
identifier  = letter { letter | digit | "_" } ;  → 識別符號由字母、數字、底線組成
```

**常見符號**：
- `::=` = 定義為
- `|` = 或者
- `{ ... }` = 重複零次或多次
- `[ ... ]` = 可選（零次或一次）
- `"..."` = 字面量

---

## 四、程式碼範例 - 從範例學習

### 4.1 第一個程式：Hello World

建立一個檔案叫做 `hello.ss`，內容如下：

```simplescript
// 我的第一個 SimpleScript 程式
print("Hello, World!");
print("歡迎來到 SimpleScript 的世界！");
```

**執行方式**：
```bash
python3 simplescript.py hello.ss
```

**執行結果**：
```
執行 hello.ss...
----------------------------------------
Hello, World!
歡迎來到 SimpleScript 的世界！
----------------------------------------
執行完成
```

### 4.2 變數練習

```simplescript
// 變數宣告與運算
let x: int = 10;
let y: int = 20;

// 計算
let sum: int = x + y;
let product: int = x * y;

// 輸出結果
print("x = " + str(x));
print("y = " + str(y));
print("x + y = " + str(sum));
print("x * y = " + str(product));
```

### 4.3 迴圈練習：算總和

```simplescript
// 計算 1 + 2 + 3 + ... + 10 的總和
let total: int = 0;

for i = 1, 11, 1 {
    total = total + i;
}

print("1+2+...+10 = " + str(total));
```

### 4.4 函數練習：費波那契數列

```simplescript
// 費波那契數列遞迴版本
fn fib(n: int) -> int {
    if n <= 1 {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

// 顯示前 10 項
for i = 0, 10, 1 {
    print("fib(" + str(i) + ") = " + str(fib(i)));
}
```

### 4.5 完整範例：計算階乘

```simplescript
// 計算階層 (n! = 1*2*3*...*n)

fn factorial(n: int) -> int {
    if n <= 1 {
        return 1;
    }
    return n * factorial(n - 1);
}

let num: int = 5;
let result: int = factorial(num);
print(str(num) + "! = " + str(result));

// 測試多個數字
for i = 1, 6, 1 {
    print(str(i) + "! = " + str(factorial(i)));
}
```

### 4.6 模組練習

首先建立 `math_utils.ss`：

```simplescript
// 數學工具模組

let PI: float = 3.14159;

fn add(a: int, b: int) -> int {
    return a + b;
}

fn multiply(a: int, b: int) -> int {
    return a * b;
}

fn power(base: int, exp: int) -> int {
    let result: int = 1;
    for i = 0, exp, 1 {
        result = result * base;
    }
    return result;
}
```

然後建立 `main.ss` 來使用它：

```simplescript
// 使用模組
import "math_utils.ss";

print("模組測試：");
print("PI = " + str(math_utils.PI));
print("add(10, 20) = " + str(math_utils.add(10, 20)));
print("multiply(6, 7) = " + str(math_utils.multiply(6, 7)));
print("power(2, 8) = " + str(math_utils.power(2, 8)));
```

---

## 五、直譯器是什麼？它是怎麼運作的？

### 5.1 整個系統的架構

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           SimpleScript 系統                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   使用者寫的程式碼                                                      │
│   ┌──────────────────────────────────────────────────────────────┐     │
│   │ let x: int = 10;                                            │     │
│   │ let y: int = 20;                                            │     │
│   │ print(x + y);                                               │     │
│   └──────────────────────────────────────────────────────────────┘     │
│                                                                         │
│   ↓ 輸入                                                                │
│                                                                         │
│   ┌─────────────────┐                                              │
│   │   詞彙分析器     │  (lexer.py)                                    │
│   │   將程式碼變成   │  把 "let" 變成 LET，                         │
│   │   一連串的 Token │  "x" 變成 IDENTIFIER                         │
│   └─────────────────┘                                              │
│                                                                         │
│   ↓ Token 流                                                            │
│                                                                         │
│   ┌─────────────────┐                                              │
│   │   語法分析器     │  (parser.py)                                    │
│   │   建立抽象語法樹 │  檢查語法是否正確，                            │
│   │   (AST)         │  建立語法樹結構                                │
│   └─────────────────┘                                              │
│                                                                         │
│   ↓ AST                                                                  │
│                                                                         │
│   ┌─────────────────┐                                              │
│   │   直譯器        │  (interpreter.py)                              │
│   │   執行 AST      │  根據語法樹執行指令，                          │
│   │   產生結果      │  輸出結果                                      │
│   └─────────────────┘                                              │
│                                                                         │
│   ↓ 輸出                                                                 │
│                                                                         │
│   30                                                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.2 讓我們用圖片解釋

```
Step 1: 原始程式碼
══════════════════════════════════════════
  let x: int = 10;
  let y: int = 20;
  print(x + y);

Step 2: 詞彙分析 - 變成 Token
══════════════════════════════════════════
  [LET, "let"] [IDENTIFIER, "x"] [COLON, ":"]
  [INT, "int"] [ASSIGN, "="] [INT, "10"]
  [NEWLINE, "\n"]
  ...

Step 3: 語法分析 - 變成 AST
══════════════════════════════════════════
  Program
   └── VariableDecl (name="x", type="int", value=10)
   └── VariableDecl (name="y", type="int", value=20)
   └── FunctionCall (name="print", args=[BinaryOp(+)])

Step 4: 直譯器執行
══════════════════════════════════════════
  建立變數 x = 10
  建立變數 y = 20
  計算 x + y = 30
  輸出 30
```

### 5.3 程式碼結構

```python
# lexer.py - 詞彙分析器
══════════════════════════════════════════
功能：將字元轉換成 Token（最小的語法單位）

輸入："let x: int = 10;"
輸出：
  Token(LET, "let")
  Token(IDENTIFIER, "x")
  Token(COLON, ":")
  Token(INT, "int")
  Token(ASSIGN, "=")
  Token(INT, 10)
```

```python
# parser.py - 語法分析器
══════════════════════════════════════════
功能：將 Token 轉換成 AST（抽象語法樹）

輸入：Token 流
輸出：
  VariableDecl(
    name="x",
    var_type="int",
    value=Literal(10)
  )
```

```python
# interpreter.py - 直譯器
══════════════════════════════════════════
功能：執行 AST，產生結果

輸入：AST
輸出：執行的結果
```

---

## 六、如何執行 SimpleScript 程式

### 6.1 前置要求

```bash
# 檢查 Python 版本
python3 --version

# 應該顯示 Python 3.8 或更高版本
```

### 6.2 執行方式

```bash
# 方式 1：執行範例程式
python3 simplescript.py hello.ss

# 方式 2：進入互動模式
python3 simplescript.py

# 然後輸入：
>>> let x: int = 10;
>>> print(x);
10
>>> exit()
```

### 6.3 已有範例檔案

| 檔案 | 說明 |
|------|------|
| `hello.ss` | Hello World 範例 |
| `fibonacci.ss` | 費波那契數列 |
| `utils.ss` | 工具模組 |
| `main.ss` | 模組匯入範例 |

---

## 七、常見問題

### Q1: 為什麼叫「直譯器」不叫「編譯器」？

**解答**：
- **編譯器**就像翻譯一本書，要先把整本書翻完才能看（執行）
- **直譯器**就像同聲傳譯，邊讀邊翻譯，馬上就能用

SimpleScript 是直譯器，所以輸入指令後馬上就能看到結果！

### Q2: 為什麼要做自己的語言？

**解答**：
1. 學習電腦底層如何運作
2. 了解程式語言的設計原理
3. 培養解決問題的能力
4. 很好玩！（自己設計語言很有成就感）

### Q3: 學這個對未來有什麼幫助？

**解答**：
- 了解 Python、JavaScript 等語言的運作原理
- 學習如何設計大型系統
- 未來可以設計自己的領域特定語言 (DSL)

### Q4: 程式出錯了怎麼辦？

**解答**：常見錯誤：

```simplescript
// 錯誤 1：忘記分號
let x: int = 10  // ← 少了 ;
print(x);

// 錯誤 2：類型錯誤
let x: int = "hello";  // ← 字串不能給 int

// 錯誤 3：使用未定義的變數
print(y);  // ← y 沒有被宣告過

// 錯誤 4：語法錯誤
if x > 5   // ← 少了 {
    print(x);
}
```

---

## 八、動手練習！

試著修改以下程式碼，體驗 SimpleScript：

### 練習 1：Hello World
```simplescript
print("你好，世界！");
```

### 練習 2：變數運算
```simplescript
let a: int = 100;
let b: int = 50;
print("a + b = " + str(a + b));
print("a - b = " + str(a - b));
print("a * b = " + str(a * b));
```

### 練習 3：寫一個函數
```simplescript
fn double(n: int) -> int {
    return n * 2;
}

print("double(5) = " + str(double(5)));
print("double(10) = " + str(double(10)));
```

---

## 九、總結

恭喜你完成了 SimpleScript 的學習！🎉

在這個專案中，我們學會了：

```
┌─────────────────────────────────────────────────────┐
│                 SimpleScript 學習成果              │
├─────────────────────────────────────────────────────┤
│  ✅ 設計自己的程式語言                               │
│  ✅ 了解直譯器的運作原理                             │
│  ✅ 學會 EBNF 語法定義                               │
│  ✅ 實作詞彙分析器                                   │
│  ✅ 實作語法分析器                                   │
│  ✅ 實作直譯器                                      │
│  ✅ 編寫和執行自己的程式                            │
└─────────────────────────────────────────────────────┘
```

**下一步可以做什麼？**
- 修改 lexer.py 加入新的關鍵字
- 修改 parser.py 支援更多語法
- 加入更多內建函數
- 嘗試寫一個編譯器（把 SimpleScript 編譯成其他語言）

---

* SimpleScript - 讓程式語言變簡單！ *
* 感謝你學習這個專案！ *