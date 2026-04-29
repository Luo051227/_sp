# SimpleScript 程式語言設計與實作

## 一、語言設計目標與功能

### 1.1 設計目標

SimpleScript 是一個簡潔、直覺的腳本語言，專為教學和快速原型開發設計。語言強調：

- **簡潔易學**：語法簡單直觀，降低學習門檻
- **強型別安全**：編譯期檢查類型錯誤，提高程式可靠性
- **自動記憶體管理**：內建垃圾回收機制，無需手動記憶體管理
- **多範式支援**：支援程序式和函數式編程

### 1.2 功能特色

| 功能 | 說明 |
|------|------|
| 變數宣告 | 支援整數、浮點數、字串、布林值 |
| 運算子 | 算術、比較、邏輯、字串運算 |
| 控制流 | if/elif/else 條件判斷、while/for 迴圈 |
| 函數 | 支援函數定義、參數傳遞、返回值 |
| 陣列 | 支援一維陣列、切片操作 |
| 內建函式 | print、len、input、str、int、float 等 |
| 模組系統 | 支援 import 載入外部模組 |

### 1.3 技術規格

- **型別系統**：強型態（Strong Typing）
- **執行模式**：直譯器（Interpreter）
- **虛擬機器**：堆疊機（Stack Machine）
- **記憶體管理**：參考計數垃圾回收（Reference Counting GC）
- **實作語言**：Python 3

---

## 二、語言語法 EBNF / BNF 定義

### 2.1 詞彙規則

```
letter      = "A".."Z" | "a".."z" ;
digit       = "0".."9" ;
identifier  = letter { letter | digit | "_" } ;
integer     = [ "-" ] digit { digit } ;
float       = [ "-" ] digit { digit } "." digit { digit } ;
string      = '"' { any-except-'"' } '"' | "'" { any-except-"'" } "'" ;
boolean     = "true" | "false" ;
```

### 2.2 語法規則

```ebnf
program             = { statement } ;

statement          = variable-declaration
                    | function-declaration
                    | assignment
                    | if-statement
                    | while-statement
                    | for-statement
                    | return-statement
                    | function-call
                    | import-statement
                    ;

variable-declaration = "let" identifier ":" type [ "=" expression ] ;

type                = "int" | "float" | "string" | "bool" | "array" "<" type ">" ;

assignment          = identifier "=" expression
                    | identifier "[" expression "]" "=" expression
                    ;

if-statement        = "if" expression "{" { statement } "}"
                      { "elif" expression "{" { statement } "}" }
                      [ "else" "{" { statement } "}" ] ;

while-statement     = "while" expression "{" { statement } "}" ;

for-statement       = "for" identifier "=" expression "," expression
                      [ "," expression ] "{" { statement } "}" ;

function-declaration = "fn" identifier "(" [ parameters ] ")" [ ":" type ]
                      "{" { statement } "}" ;

parameters          = parameter { "," parameter } ;
parameter           = identifier ":" type ;

return-statement     = "return" [ expression ] ;

function-call       = identifier "(" [ arguments ] ")" ;
arguments           = expression { "," expression } ;

import-statement     = "import" string ;

expression          = logical-or ;
logical-or          = logical-and { "or" logical-and } ;
logical-and         = equality { "and" equality } ;
equality            = relational { ( "==" | "!=" ) relational } ;
relational          = additive { ( "<" | ">" | "<=" | ">=" ) additive } ;
additive            = multiplicative { ( "+" | "-" ) multiplicative } ;
multiplicative      = unary { ( "*" | "/" | "%" ) unary } ;
unary               = ( "-" | "not" ) unary | postfix ;
postfix             = primary { "[" expression "]" | "(" arguments ")" } ;
primary             = identifier | integer | float | string | boolean
                    | "(" expression ")" | array-literal | lambda ;
array-literal       = "[" [ expression { "," expression } ] "]" ;
lambda              = "fn" "(" [ parameters ] ")" "{" { statement } "}" ;
```

### 2.3 完整 BNF 語法

```bnf
<program>          ::= <statement-list>

<statement-list> ::= <statement> <statement-list> | ε

<statement>      ::= <variable-decl>
                   | <function-def>
                   | <assignment>
                   | <if-stmt>
                   | <while-stmt>
                   | <for-stmt>
                   | <return-stmt>
                   | <func-call>
                   | <import-stmt>

<variable-decl>   ::= "let" <identifier> ":" <type> ["=" <expr>]

<type>            ::= "int" | "float" | "string" | "bool" | "array" "<" <type> ">"

<function-def>    ::= "fn" <identifier> "(" [<param-list>] ")" [":" <type>] "{" <statement-list> "}"

<param-list>      ::= <param> {"," <param>}

<param>           ::= <identifier> ":" <type>

<assignment>      ::= <identifier> "=" <expr>
                   | <identifier> "[" <expr> "]" "=" <expr>

<if-stmt>         ::= "if" <expr> "{" <statement-list> "}"
                      {"elif" <expr> "{" <statement-list> "}"}
                      ["else" "{" <statement-list> "}"]

<while-stmt>      ::= "while" <expr> "{" <statement-list> "}"

<for-stmt>        ::= "for" <identifier> "=" <expr> "," <expr> ["," <expr>] "{" <statement-list> "}"

<return-stmt>      ::= "return" [<expr>]

<func-call>       ::= <identifier> "(" [<arg-list>] ")"

<arg-list>        ::= <expr> {"," <expr>}

<import-stmt>     ::= "import" <string-literal>

<expr>            ::= <logical-or-expr>

<logical-or-expr> ::= <logical-and-expr> {"or" <logical-and-expr>}

<logical-and-expr> ::= <equality-expr> {"and" <equality-expr>}

<equality-expr>   ::= <relational-expr> {("==" | "!=") <relational-expr>}

<relational-expr> ::= <additive-expr> {("<" | ">" | "<=" | ">=") <additive-expr>}

<additive-expr>   ::= <multiplicative-expr> {("+" | "-") <multiplicative-expr>}

<multiplicative-expr> ::= <unary-expr> {("*" | "/" | "%") <unary-expr>}

<unary-expr>      ::= ("-" | "not") <unary-expr> | <postfix-expr>

<postfix-expr>    ::= <primary-expr> {("[" <expr> "]") | ("(" <arg-list> ")")}

<primary-expr>    ::= <identifier> | <integer-literal> | <float-literal>
                   | <string-literal> | <boolean-literal> | "(" <expr> ")"
                   | <array-literal> | <lambda-expr>

<array-literal>   ::= "[" [<expr> {"," <expr>}] "]"

<lambda-expr>     ::= "fn" "(" [<param-list>] ")" "{" <statement-list> "}"
```

---

## 三、程式範例

### 3.1 Hello World

```simplescript
// Hello World 範例
print("Hello, World!");
```

### 3.2 變數與運算

```simplescript
// 變數宣告與運算
let x: int = 10;
let y: int = 20;
let sum: int = x + y;
let isGreater: bool = sum > 25;

print("x = " + str(x));
print("y = " + str(y));
print("x + y = " + str(sum));
print("sum > 25: " + str(isGreater));
```

### 3.3 迴圈與條件

```simplescript
// 計算階層
fn factorial(n: int) -> int {
    if n <= 1 {
        return 1;
    }
    return n * factorial(n - 1);
}

let result: int = factorial(5);
print("5! = " + str(result));

// 迴圈範例
let sum: int = 0;
for i = 1, 10, 1 {
    sum = sum + i;
}
print("1+2+...+10 = " + str(sum));
```

### 3.4 陣列操作

```simplescript
// 陣列範例
let numbers: array<int> = [1, 2, 3, 4, 5];

print("陣列長度: " + str(len(numbers)));
print("第一個元素: " + str(numbers[0]));
print("最後元素: " + str(numbers[4]));

// 陣列遍歷
let total: int = 0;
for i = 0, len(numbers), 1 {
    total = total + numbers[i];
}
print("總和: " + str(total));
```

### 3.5 完整範例：費波那契數列

```simplescript
// 費波那契數列
fn fib(n: int) -> int {
    if n <= 1 {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

print("費波那契數列前10項:");
for i = 0, 10, 1 {
    print("fib(" + str(i) + ") = " + str(fib(i)));
}

// 使用迴圈版本
fn fibLoop(n: int) -> int {
    if n <= 1 {
        return n;
    }
    let a: int = 0;
    let b: int = 1;
    let temp: int = 0;
    
    for i = 2, n, 1 {
        temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

print("\n迴圈版本:");
for i = 0, 10, 1 {
    print("fib(" + str(i) + ") = " + str(fibLoop(i)));
}
```

### 3.6 模組匯入範例

```simplescript
// main.simplescript
import "utils.ss";

// 使用模組中的函數
let result: int = utils.add(10, 20);
print("10 + 20 = " + str(result));

// 使用模組中的變數
print("PI = " + str(utils.PI));
```

---

## 四、實作架構

### 4.1 系統架構

```
┌─────────────────────────────────────────────────────────────┐
│                    SimpleScript 語言                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   詞彙分析   │ →  │   語意分析   │ →  │   語法分析   │    │
│  │   (Lexer)   │    │   (Parser)   │    │   (Parser)  │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
├─────────────────────────────────────────────────────────────┤
│                      AST 抽象語法樹                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │ 語意分析器   │ →  │  解譯器     │ →  │  記憶體管理  │    │
│  │ (Analyzer)  │    │ (Interpreter)│   │   (GC)      │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
├─────────────────────────────────────────────────────────────┤
│                    堆疊機虛擬機器 (Stack VM)                 │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 核心元件

| 元件 | 檔案 | 說明 |
|------|------|------|
| 詞彙分析器 | lexer.py | 將原始碼轉換為 Token 流 |
| 語法分析器 | parser.py | 解析 Token 並建立 AST |
| 語意分析器 | analyzer.py | 進行類型檢查和作用域分析 |
| 解譯器 | interpreter.py | 執行 AST 並產生結果 |
| 垃圾回收器 | gc.py | 記憶體回收機制 |
| 虛擬機器 | vm.py | 堆疊機指令執行 |

---

## 五、執行方式

### 5.1 執行環境需求

- Python 3.8+
- 無需安裝額外套件

### 5.2 執行命令

```bash
# 執行 SimpleScript 程式
python3 simplescript.py <檔案名稱>

# 或使用 shearbang
chmod +x simplescript.py
./simplescript.py <檔案名稱>
```

### 5.3 互動模式

```bash
# 進入互動模式
python3 simplescript.py
```

---

## 六、內建函式

| 函式 | 說明 | 範例 |
|------|------|------|
| print(...) | 輸出到控制台 | print("Hello") |
| str(val) | 轉換為字串 | str(123) |
| int(val) | 轉換為整數 | int("42") |
| float(val) | 轉換為浮點數 | float("3.14") |
| len(arr) | 取得陣列長度 | len(arr) |
| input(prompt) | 取得使用者輸入 | input("Name: ") |

---

## 七、錯誤訊息

| 錯誤類型 | 說明 |
|----------|------|
| LexerError | 詞彙分析錯誤 |
| ParseError | 語法分析錯誤 |
| TypeError | 型別錯誤 |
| NameError | 未定義的名稱 |
| RuntimeError | 執行階段錯誤 |
| ImportError | 模組匯入錯誤 |

---

## 八、總結

SimpleScript 是一個完整的直譯器語言，展示了程式語言設計的核心概念：

- ✅ **強型態**：編譯期類型檢查
- ✅ **直譯器**：直接執行原始碼
- ✅ **堆疊機**：基於堆疊的虛擬機器
- ✅ **垃圾回收**：參考計數記憶體管理
- ✅ **完整的語法**：支援多種程式設計範式

本專案可作為學習程式語言理論和實作的基礎教材。

---

*SimpleScript - 簡單而強大的程式語言*