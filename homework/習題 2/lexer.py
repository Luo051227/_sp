#!/usr/bin/env python3
"""
SimpleScript 詞彙分析器 (Lexer)
將原始程式碼轉換為 Token 流
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    # 關鍵字
    LET = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    FN = auto()
    RETURN = auto()
    IMPORT = auto()
    TRUE = auto()
    FALSE = auto()
    
    # 類型
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOL = auto()
    ARRAY = auto()
    
    # 識別符號
    IDENTIFIER = auto()
    
    # 運算子
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    
    # 比較運算子
    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()
    
    # 邏輯運算子
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # 賦值
    ASSIGN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    COLON = auto()
    ARROW = auto()  # ->
    
    # 特殊
    EOF = auto()
    NEWLINE = auto()


@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int


class LexerError(Exception):
    """詞彙分析錯誤"""
    def __init__(self, message: str, line: int = 0, column: int = 0):
        self.line = line
        self.column = column
        super().__init__(f"詞彙錯誤 at line {line}, column {column}: {message}")


class Lexer:
    """詞彙分析器"""
    
    KEYWORDS = {
        'let': TokenType.LET,
        'if': TokenType.IF,
        'elif': TokenType.ELIF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        'fn': TokenType.FN,
        'return': TokenType.RETURN,
        'import': TokenType.IMPORT,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'int': TokenType.INT,
        'float': TokenType.FLOAT,
        'string': TokenType.STRING,
        'bool': TokenType.BOOL,
        'array': TokenType.ARRAY,
    }
    
    OPERATORS = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '%': TokenType.MODULO,
        '=': TokenType.ASSIGN,
        '==': TokenType.EQ,
        '!=': TokenType.NEQ,
        '<': TokenType.LT,
        '>': TokenType.GT,
        '<=': TokenType.LTE,
        '>=': TokenType.GTE,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """執行詞彙分析"""
        while not self.is_at_end():
            self.skip_whitespace_and_comments()
            if self.is_at_end():
                break
            
            token = self.next_token()
            if token and token.type != TokenType.NEWLINE:
                self.tokens.append(token)
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
    
    def next_token(self) -> Optional[Token]:
        """取得下一個 Token"""
        char = self.peek()
        
        # 識別符號或關鍵字
        if char.isalpha() or char == '_':
            return self.identifier()
        
        # 數字
        if char.isdigit():
            return self.number()
        
        # 字串
        if char == '"' or char == "'":
            return self.string()
        
        # 運算子
        if char in '+-*/%<>=!':
            return self.operator()
        
        # 標點符號
        return self.punctuation()
    
    def identifier(self) -> Token:
        """識別符號或關鍵字"""
        start = self.column
        result = ''
        
        while not self.is_at_end() and (self.peek().isalnum() or self.peek() == '_'):
            result += self.peek()
            self.advance()
        
        token_type = self.KEYWORDS.get(result, TokenType.IDENTIFIER)
        
        # 檢查 -> 語法
        if result == '->':
            return Token(TokenType.ARROW, '->', self.line, start)
        
        return Token(token_type, result, self.line, start)
    
    def number(self) -> Token:
        """數字常數"""
        start = self.column
        result = ''
        has_dot = False
        
        while not self.is_at_end() and (self.peek().isdigit() or self.peek() == '.'):
            if self.peek() == '.':
                if has_dot:
                    break
                has_dot = True
            result += self.peek()
            self.advance()
        
        if has_dot:
            return Token(TokenType.FLOAT, float(result), self.line, start)
        else:
            return Token(TokenType.INT, int(result), self.line, start)
    
    def string(self) -> Token:
        """字串常數"""
        start = self.column
        quote = self.peek()
        self.advance()  # 跳過開頭引號
        
        result = ''
        while not self.is_at_end() and self.peek() != quote:
            if self.peek() == '\\':  # 處理逸出序列
                self.advance()
                if not self.is_at_end():
                    escaped = self.peek()
                    escape_map = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"'}
                    result += escape_map.get(escaped, escaped)
                    self.advance()
            else:
                result += self.peek()
                self.advance()
        
        if self.is_at_end():
            raise LexerError("未關閉的字串", self.line, start)
        
        self.advance()  # 跳過結尾引號
        return Token(TokenType.STRING, result, self.line, start)
    
    def operator(self) -> Token:
        """運算子"""
        start = self.column
        char = self.peek()
        self.advance()
        
        # 雙字元運算子
        if not self.is_at_end() and self.peek() in '=<>!':
            two_char = char + self.peek()
            self.advance()
            
            if two_char == '->':
                return Token(TokenType.ARROW, '->', self.line, start)
            
            token_type = self.OPERATORS.get(two_char)
            if token_type:
                return Token(token_type, two_char, self.line, start)
        
        token_type = self.OPERATORS.get(char)
        if token_type:
            return Token(token_type, char, self.line, start)
        
        raise LexerError(f"未知的運算子: {char}", self.line, start)
    
    def punctuation(self) -> Token:
        """標點符號"""
        char = self.peek()
        start = self.column
        
        token_map = {
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            ',': TokenType.COMMA,
            ':': TokenType.COLON,
            '\n': TokenType.NEWLINE,
        }
        
        self.advance()
        
        if char == '\n':
            self.line += 1
            self.column = 1
            return Token(TokenType.NEWLINE, '\n', self.line - 1, start)
        
        return Token(token_map.get(char, TokenType.EOF), char, self.line, start)
    
    def skip_whitespace_and_comments(self):
        """跳過空白和註解"""
        while not self.is_at_end():
            char = self.peek()
            
            # 跳過空白
            if char in ' \t\r':
                self.advance()
                continue
            
            # 跳過行註解
            if char == '/' and self.peek_next() == '/':
                while not self.is_at_end() and self.peek() != '\n':
                    self.advance()
                continue
            
            break
    
    def peek(self) -> str:
        """查看當前字元"""
        if self.is_at_end():
            return '\0'
        return self.source[self.pos]
    
    def peek_next(self) -> str:
        """查看下一個字元"""
        if self.pos + 1 >= len(self.source):
            return '\0'
        return self.source[self.pos + 1]
    
    def advance(self) -> str:
        """前進到下一個字元"""
        if self.source[self.pos] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        self.pos += 1
        return self.source[self.pos - 1]
    
    def is_at_end(self) -> bool:
        return self.pos >= len(self.source)


def tokenize(source: str) -> List[Token]:
    """方便的詞彙分析函數"""
    lexer = Lexer(source)
    return lexer.tokenize()


if __name__ == "__main__":
    # 測試
    source = """
    let x: int = 10;
    let name: string = "Hello";
    if x > 5 {
        print(x);
    }
    """
    
    tokens = tokenize(source)
    for token in tokens:
        print(f"{token.type.name:15} {repr(token.value):15} (line {token.line}, col {token.column})")