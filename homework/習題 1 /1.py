#!/usr/bin/env python3
"""
p0 編譯器 - 加入 while 語法
支援：函數定義、if 判斷、while 迴圈、算術運算、函數呼叫
"""

import sys
import re
from collections import OrderedDict

# =========================================================
# 1. 中間碼 (Quadruples) 資料結構
# 四元組格式：(Op, Arg1, Arg2, Result)
# =========================================================

class Quad:
    def __init__(self, op="", arg1="", arg2="", result=""):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __str__(self):
        return f"{self.op:10} {self.arg1:10} {self.arg2:10} {self.result:10}"

quads = []
t_idx = 0

def new_t():
    global t_idx
    t_idx += 1
    return f"t{t_idx}"

def emit(op, arg1="", arg2="", result=""):
    """生成中間碼並印出"""
    q = Quad(op, arg1, arg2, result)
    quads.append(q)
    print(f"{len(quads)-1:03d}: {q}")
    return len(quads) - 1

# =========================================================
# 2. 詞法分析 (Lexer)
# 將原始碼字串切分成 Token
# =========================================================

TOKEN_TYPES = [
    'FUNC', 'RETURN', 'IF', 'WHILE', 'ELSE',
    'ID', 'NUM',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'SEMICOLON',
    'ASSIGN', 'PLUS', 'MINUS', 'MUL', 'DIV',
    'EQ', 'LT', 'GT', 'NE',
    'EOF'
]

class Token:
    def __init__(self, type_, text=""):
        self.type = type_
        self.text = text

    def __repr__(self):
        return f"Token({self.type}, '{self.text}')"

class Lexer:
    def __init__(self, src):
        self.src = src
        self.pos = 0
        self.current_char = self.src[0] if self.src else None
    
    def advance(self):
        self.pos += 1
        self.current_char = self.src[self.pos] if self.pos < len(self.src) else None
    
    def peek(self, n=1):
        idx = self.pos + n
        return self.src[idx] if idx < len(self.src) else None
    
    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        if self.current_char == '/':
            if self.peek() == '/':
                while self.current_char and self.current_char != '\n':
                    self.advance()
            elif self.peek() == '*':
                self.advance()
                self.advance()
                while self.current_char:
                    if self.current_char == '*' and self.peek() == '/':
                        self.advance()
                        self.advance()
                        break
                    self.advance()
    
    def read_number(self):
        num = ""
        while self.current_char and self.current_char.isdigit():
            num += self.current_char
            self.advance()
        return Token('NUM', num)
    
    def read_identifier(self):
        ident = ""
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            ident += self.current_char
            self.advance()
        
        keywords = {'func': 'FUNC', 'return': 'RETURN', 'if': 'IF', 
                   'while': 'WHILE', 'else': 'ELSE'}
        return Token(keywords.get(ident, 'ID'), ident)
    
    def get_next_token(self):
        while self.current_char:
            # 跳過空白
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # 跳過註解
            if self.current_char == '/':
                self.skip_comment()
                continue
            
            # 數字
            if self.current_char.isdigit():
                return self.read_number()
            
            # 識別碼或關鍵字
            if self.current_char.isalpha() or self.current_char == '_':
                return self.read_identifier()
            
            # 運算符與符號
            char = self.current_char
            
            # 雙字元運算符
            if char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('EQ', '==')
            if char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('NE', '!=')
            if char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('LE', '<=')
            if char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('GE', '>=')
            
            # 單字元
            single_tokens = {
                '(': 'LPAREN', ')': 'RPAREN', '{': 'LBRACE', '}': 'RBRACE',
                ',': 'COMMA', ';': 'SEMICOLON', '+': 'PLUS', '-': 'MINUS',
                '*': 'MUL', '/': 'DIV', '=': 'ASSIGN', '<': 'LT', '>': 'GT'
            }
            
            if char in single_tokens:
                self.advance()
                return Token(single_tokens[char], char)
            
            # 未知的字元
            self.advance()
        
        return Token('EOF', '')

# =========================================================
# 3. 語法解析 (Parser) - 遞迴下降法
# =========================================================

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self, expected):
        print(f"錯誤：預期 {expected}，但得到 {self.current_token}")
        sys.exit(1)
    
    def advance(self):
        self.current_token = self.lexer.get_next_token()
    
    def expect(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
        else:
            self.error(token_type)
    
    # --- 表達式解析 ---
    
    def factor(self):
        """factor = number | identifier [ "(" [ args ] ")" ] | "(" expression ")" """
        if self.current_token.type == 'NUM':
            res = new_t()
            emit('IMM', self.current_token.text, '-', res)
            self.advance()
            return res
        elif self.current_token.type == 'ID':
            name = self.current_token.text
            self.advance()
            if self.current_token.type == 'LPAREN':
                # 函數呼叫
                self.advance()
                args = []
                while self.current_token.type != 'RPAREN':
                    arg = self.expression()
                    args.append(arg)
                    if self.current_token.type == 'COMMA':
                        self.advance()
                self.expect('RPAREN')
                # 產生 PARAM 指令
                for arg in args:
                    emit('PARAM', arg, '-', '-')
                res = new_t()
                emit('CALL', name, str(len(args)), res)
                return res
            return name
        elif self.current_token.type == 'LPAREN':
            self.advance()
            res = self.expression()
            self.expect('RPAREN')
            return res
        else:
            self.error("factor")
            return ""
    
    def term(self):
        """term = factor { ("*" | "/") factor }"""
        res = self.factor()
        while self.current_token.type in ('MUL', 'DIV'):
            op = 'MUL' if self.current_token.type == 'MUL' else 'DIV'
            self.advance()
            right = self.factor()
            temp = new_t()
            emit(op, res, right, temp)
            res = temp
        return res
    
    def arith_expr(self):
        """arith_expr = term { ("+" | "-") term }"""
        res = self.term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = 'ADD' if self.current_token.type == 'PLUS' else 'SUB'
            self.advance()
            right = self.term()
            temp = new_t()
            emit(op, res, right, temp)
            res = temp
        return res
    
    def comparison(self):
        """comparison = arith_expr [ ("==" | "<" | ">" | "!=" | "<=" | ">=") arith_expr ]"""
        res = self.arith_expr()
        if self.current_token.type in ('EQ', 'LT', 'GT', 'NE', 'LE', 'GE'):
            op_map = {'EQ': 'CMP_EQ', 'LT': 'CMP_LT', 'GT': 'CMP_GT', 
                     'NE': 'CMP_NE', 'LE': 'CMP_LE', 'GE': 'CMP_GE'}
            op = op_map[self.current_token.type]
            self.advance()
            right = self.arith_expr()
            temp = new_t()
            emit(op, res, right, temp)
            return temp
        return res
    
    def expression(self):
        """表達式 = 比較運算"""
        return self.comparison()
    
    # --- 陳述句解析 ---
    
    def statement(self):
        """statement = if_statement | while_statement | assignment | return_statement"""
        if self.current_token.type == 'IF':
            self.if_statement()
        elif self.current_token.type == 'WHILE':
            self.while_statement()
        elif self.current_token.type == 'RETURN':
            self.return_statement()
        elif self.current_token.type == 'ID':
            self.assignment_statement()
        else:
            # 空陳述句或區塊結束
            pass
    
    def if_statement(self):
        """if_statement = "if" "(" expression ")" "{" { statement } "}" [ "else" "{" { statement } "}" ]"""
        self.advance()  # skip 'if'
        self.expect('LPAREN')
        cond = self.expression()
        self.expect('RPAREN')
        self.expect('LBRACE')
        
        # 記錄 if 開始位置
        if_start = len(quads)
        emit('JMP_F', cond, '-', '?')  # 條件為 false 跳過if區塊
        
        while self.current_token.type != 'RBRACE':
            self.statement()
        self.expect('RBRACE')
        
        # 回填 if 結束後的跳轉點
        quads[if_start].result = str(len(quads))
        
        # else 處理
        if self.current_token.type == 'ELSE':
            self.advance()
            self.expect('LBRACE')
            
            # 跳過 else 區塊
            else_jump = len(quads)
            emit('JMP', '-', '-', '?')
            
            # 回填 if 結束位置
            quads[if_start].result = str(len(quads))
            
            while self.current_token.type != 'RBRACE':
                self.statement()
            self.expect('RBRACE')
            
            # 回填 else 結束位置
            quads[else_jump].result = str(len(quads))
    
    def while_statement(self):
        """while_statement = "while" "(" expression ")" "{" { statement } "}" """
        self.advance()  # skip 'while'
        self.expect('LPAREN')
        
        loop_start = len(quads)  # 記錄迴圈開始位置
        cond = self.expression()
        self.expect('RPAREN')
        self.expect('LBRACE')
        
        # 條件為 false 時跳出迴圈
        jmp_out = len(quads)
        emit('JMP_F', cond, '-', '?')
        
        while self.current_token.type != 'RBRACE':
            self.statement()
        self.expect('RBRACE')
        
        # 跳回迴圈開始
        emit('JMP', '-', '-', str(loop_start))
        
        # 回填跳出位置
        quads[jmp_out].result = str(len(quads))
    
    def assignment_statement(self):
        """assignment = identifier "=" expression ";" """
        name = self.current_token.text
        self.advance()
        if self.current_token.type == 'ASSIGN':
            self.advance()
            res = self.expression()
            emit('STORE', res, '-', name)
            if self.current_token.type == 'SEMICOLON':
                self.advance()
        elif self.current_token.type == 'LPAREN':
            # 函數呼叫作為陳述句
            args = []
            while self.current_token.type != 'RPAREN':
                arg = self.expression()
                args.append(arg)
                if self.current_token.type == 'COMMA':
                    self.advance()
            self.expect('RPAREN')
            for arg in args:
                emit('PARAM', arg, '-', '-')
            emit('CALL', name, str(len(args)), '_')
            if self.current_token.type == 'SEMICOLON':
                self.advance()
    
    def return_statement(self):
        """return_statement = "return" expression ";" """
        self.advance()  # skip 'return'
        res = self.expression()
        emit('RET_VAL', res, '-', '-')
        if self.current_token.type == 'SEMICOLON':
            self.advance()
    
    # --- 程式主體 ---
    
    def program(self):
        """program = { function_def | statement }"""
        while self.current_token.type != 'EOF':
            if self.current_token.type == 'FUNC':
                self.function_def()
            else:
                self.statement()
    
    def function_def(self):
        """function_def = "func" identifier "(" [ params ] ")" "{" { statement } "}" """
        self.advance()  # skip 'func'
        func_name = self.current_token.text
        self.advance()
        
        emit('FUNC_BEG', func_name, '-', '-')
        
        self.expect('LPAREN')
        # 處理參數
        while self.current_token.type == 'ID':
            emit('FORMAL', self.current_token.text, '-', '-')
            self.advance()
            if self.current_token.type == 'COMMA':
                self.advance()
        self.expect('RPAREN')
        
        self.expect('LBRACE')
        while self.current_token.type != 'RBRACE':
            self.statement()
        self.expect('RBRACE')
        
        emit('FUNC_END', func_name, '-', '-')

# =========================================================
# 4. 虛擬機 (Virtual Machine)
# 模擬 CPU 行為，實現函數呼叫機制
# =========================================================

class Frame:
    """堆疊幀 (Stack Frame) - 用於實現函數呼叫"""
    def __init__(self):
        self.names = OrderedDict()    # 區域變數名稱 -> 值
        self.ret_pc = 0               # 回傳後應繼續執行的 PC 位置
        self.ret_var = ""             # 結果應回填給 Caller 的哪個變數
        self.incoming_args = []       # 傳進來的參數值
        self.formal_idx = 0           # 處理參數的計數器

class VirtualMachine:
    def __init__(self, quads):
        self.quads = quads
        self.stack = [Frame()]  # 呼叫堆疊，0 號為全域環境
        self.sp = 0             # Stack Pointer
        self.pc = 0             # Program Counter
        
        # 建立函數查詢表
        self.func_table = {}  # 函數名 -> 進入點 PC
        for i, q in enumerate(quads):
            if q.op == 'FUNC_BEG':
                self.func_table[q.arg1] = i
    
    def get_var(self, name):
        """取得目前 Frame 的變數值"""
        if name.isdigit() or (name[0] == '-' and name[1:].isdigit()):
            return int(name)
        if name in self.stack[self.sp].names:
            return self.stack[self.sp].names[name]
        return 0
    
    def set_var(self, name, value):
        """設定或新建目前 Frame 的變數"""
        self.stack[self.sp].names[name] = value
    
    def run(self):
        print("\n=== VM 執行開始 ===")
        
        while self.pc < len(self.quads):
            q = self.quads[self.pc]
            
            # 遇到函數定義段落，直接跳到結束
            if q.op == 'FUNC_BEG':
                while self.pc < len(self.quads) and self.quads[self.pc].op != 'FUNC_END':
                    self.pc += 1
                self.pc += 1
                continue
            
            # 基本運算
            if q.op == 'IMM':
                self.set_var(q.result, int(q.arg1))
            
            elif q.op == 'ADD':
                self.set_var(q.result, self.get_var(q.arg1) + self.get_var(q.arg2))
            elif q.op == 'SUB':
                self.set_var(q.result, self.get_var(q.arg1) - self.get_var(q.arg2))
            elif q.op == 'MUL':
                self.set_var(q.result, self.get_var(q.arg1) * self.get_var(q.arg2))
            elif q.op == 'DIV':
                self.set_var(q.result, self.get_var(q.arg1) // self.get_var(q.arg2))
            
            # 比較運算
            elif q.op == 'CMP_EQ':
                self.set_var(q.result, 1 if self.get_var(q.arg1) == self.get_var(q.arg2) else 0)
            elif q.op == 'CMP_LT':
                self.set_var(q.result, 1 if self.get_var(q.arg1) < self.get_var(q.arg2) else 0)
            elif q.op == 'CMP_GT':
                self.set_var(q.result, 1 if self.get_var(q.arg1) > self.get_var(q.arg2) else 0)
            elif q.op == 'CMP_NE':
                self.set_var(q.result, 1 if self.get_var(q.arg1) != self.get_var(q.arg2) else 0)
            elif q.op == 'CMP_LE':
                self.set_var(q.result, 1 if self.get_var(q.arg1) <= self.get_var(q.arg2) else 0)
            elif q.op == 'CMP_GE':
                self.set_var(q.result, 1 if self.get_var(q.arg1) >= self.get_var(q.arg2) else 0)
            
            # 賦值
            elif q.op == 'STORE':
                self.set_var(q.result, self.get_var(q.arg1))
            
            # 跳轉指令
            elif q.op == 'JMP':
                self.pc = int(q.result)
                continue
            elif q.op == 'JMP_F':
                if self.get_var(q.arg1) == 0:
                    self.pc = int(q.result)
                    continue
            
            # 函數呼叫相關
            elif q.op == 'PARAM':
                # 參數傳遞 - 簡化版本，用全域列表
                if not hasattr(self, 'param_stack'):
                    self.param_stack = []
                self.param_stack.append(self.get_var(q.arg1))
            
            elif q.op == 'CALL':
                # 取得目標函數的 PC
                target_pc = self.func_table.get(q.arg1, -1)
                if target_pc == -1:
                    print(f"錯誤：函數 {q.arg1} 未定義")
                    return
                
                # 建立新的堆疊幀
                self.sp += 1
                self.stack.append(Frame())
                self.stack[self.sp].ret_pc = self.pc + 1
                self.stack[self.sp].ret_var = q.result
                
                # 傳遞參數
                param_count = int(q.arg2)
                self.stack[self.sp].incoming_args = self.param_stack[-param_count:]
                self.param_stack = self.param_stack[:-param_count]
                
                self.pc = target_pc
                continue
            
            elif q.op == 'FORMAL':
                # 將傳入的參數存入區域變數
                idx = self.stack[self.sp].formal_idx
                self.set_var(q.arg1, self.stack[self.sp].incoming_args[idx])
                self.stack[self.sp].formal_idx += 1
            
            elif q.op == 'RET_VAL':
                # 回傳值
                ret_val = self.get_var(q.arg1)
                ret_pc = self.stack[self.sp].ret_pc
                ret_var = self.stack[self.sp].ret_var
                
                # 銷毀當前堆疊幀
                self.sp -= 1
                
                # 將回傳值寫入 Caller 的變數空間
                if ret_var != '_':
                    self.set_var(ret_var, ret_val)
                
                self.pc = ret_pc
                continue
            
            self.pc += 1
        
        print("=== VM 執行完畢 ===")
        print("\n全域變數結果:")
        for name, value in self.stack[0].names.items():
            if not name.startswith('t'):
                print(f">> {name} = {value}")

# =========================================================
# 主程式
# =========================================================

def main():
    if len(sys.argv) < 2:
        print("用法: python 1.py <source_file>")
        print("範例: python 1.py test.txt")
        sys.exit(1)
    
    # 讀取原始碼
    with open(sys.argv[1], 'r') as f:
        src = f.read()
    
    print("原始碼:")
    print("-" * 40)
    print(src)
    print("-" * 40)
    print("\n編譯器生成的中間碼 (PC: Quadruples):")
    print("-" * 40)
    
    # 詞法分析
    lexer = Lexer(src)
    
    # 語法解析
    parser = Parser(lexer)
    parser.program()
    
    # 虛擬機執行
    vm = VirtualMachine(quads)
    vm.run()

if __name__ == '__main__':
    main()