#!/usr/bin/env python3
"""
SimpleScript 語法分析器 (Parser)
將 Token 流解析為 AST (抽象語法樹)
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum

from lexer import Token, TokenType, Lexer


# ============== AST 節點定義 ==============

@dataclass
class ASTNode:
    """AST 節點基類"""
    line: int = 0
    column: int = 0


@dataclass
class Program(ASTNode):
    """程式根節點"""
    statements: List[ASTNode] = field(default_factory=list)


@dataclass
class VariableDecl(ASTNode):
    """變數宣告"""
    name: str
    var_type: str
    value: Optional[ASTNode] = None


@dataclass
class Assignment(ASTNode):
    """賦值語句"""
    target: ASTNode
    value: ASTNode


@dataclass
class Identifier(ASTNode):
    """識別符號"""
    name: str


@dataclass
class Literal(ASTNode):
    """常數"""
    value: Any
    literal_type: str = "unknown"


@dataclass
class ArrayLiteral(ASTNode):
    """陣列常值"""
    elements: List[ASTNode] = field(default_factory=list)


@dataclass
class BinaryOp(ASTNode):
    """二元運算"""
    operator: str
    left: ASTNode
    right: ASTNode


@dataclass
class UnaryOp(ASTNode):
    """一元運算"""
    operator: str
    operand: ASTNode


@dataclass
class IndexAccess(ASTNode):
    """陣列索引存取"""
    array: ASTNode
    index: ASTNode


@dataclass
class FunctionCall(ASTNode):
    """函數呼叫"""
    name: str
    arguments: List[ASTNode] = field(default_factory=list)


@dataclass
class FunctionDef(ASTNode):
    """函數定義"""
    name: str
    params: List[tuple] = field(default_factory=list)  # [(name, type), ...]
    return_type: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class ReturnStmt(ASTNode):
    """返回語句"""
    value: Optional[ASTNode] = None


@dataclass
class IfStmt(ASTNode):
    """條件語句"""
    condition: ASTNode
    then_branch: List[ASTNode] = field(default_factory=list)
    elif_branches: List[tuple] = field(default_factory=list)  # [(condition, body), ...]
    else_branch: List[ASTNode] = field(default_factory=list)


@dataclass
class WhileStmt(ASTNode):
    """while 迴圈"""
    condition: ASTNode
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class ForStmt(ASTNode):
    """for 迴圈"""
    variable: str
    start: ASTNode
    end: ASTNode
    step: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class ImportStmt(ASTNode):
    """匯入語句"""
    module_path: str


class ParseError(Exception):
    """語法分析錯誤"""
    def __init__(self, message: str, token: Token = None):
        if token:
            super().__init__(f"語法錯誤 at line {token.line}, column {token.column}: {message}")
        else:
            super().__init__(f"語法錯誤: {message}")


class Parser:
    """語法分析器"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self) -> Program:
        """解析程式"""
        statements = []
        
        while not self.is_at_end():
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        
        return Program(statements=statements, line=1, column=1)
    
    # ============== 語句解析 ==============
    
    def statement(self) -> ASTNode:
        """解析語句"""
        if self.match(TokenType.IMPORT):
            return self.import_statement()
        
        if self.match(TokenType.LET):
            return self.variable_declaration()
        
        if self.match(TokenType.FN):
            return self.function_definition()
        
        if self.match(TokenType.IF):
            return self.if_statement()
        
        if self.match(TokenType.WHILE):
            return self.while_statement()
        
        if self.match(TokenType.FOR):
            return self.for_statement()
        
        if self.match(TokenType.RETURN):
            return self.return_statement()
        
        # 表達式作為語句
        return self.expression_statement()
    
    def import_statement(self) -> ImportStmt:
        """匯入語句"""
        if not self.check(TokenType.STRING):
            raise ParseError("import 後需要字串", self.peek())
        
        token = self.advance()
        return ImportStmt(module_path=token.value, line=token.line, column=token.column)
    
    def variable_declaration(self) -> VariableDecl:
        """變數宣告"""
        # 識別符號
        if not self.check(TokenType.IDENTIFIER):
            raise ParseError("需要變數名稱", self.peek())
        
        name_token = self.advance()
        name = name_token.value
        
        # 冒號和類型
        if not self.match(TokenType.COLON):
            raise ParseError("需要冒號和類型", self.peek())
        
        if not self.check_type():
            raise ParseError("需要類型", self.peek())
        
        type_token = self.advance()
        var_type = type_token.value
        
        # 可选的初始化
        value = None
        if self.match(TokenType.ASSIGN):
            value = self.expression()
        
        return VariableDecl(
            name=name,
            var_type=var_type,
            value=value,
            line=name_token.line,
            column=name_token.column
        )
    
    def function_definition(self) -> FunctionDef:
        """函數定義"""
        # 函數名稱
        if not self.check(TokenType.IDENTIFIER):
            raise ParseError("需要函數名稱", self.peek())
        
        name_token = self.advance()
        name = name_token.value
        
        # 參數列表
        if not self.match(TokenType.LPAREN):
            raise ParseError("需要左括號", self.peek())
        
        params = []
        if not self.check(TokenType.RPAREN):
            while True:
                if not self.check(TokenType.IDENTIFIER):
                    raise ParseError("需要參數名稱", self.peek())
                
                param_name_token = self.advance()
                param_name = param_name_token.value
                
                if not self.match(TokenType.COLON):
                    raise ParseError("需要冒號和類型", self.peek())
                
                if not self.check_type():
                    raise ParseError("需要參數類型", self.peek())
                
                param_type_token = self.advance()
                params.append((param_name, param_type_token.value))
                
                if self.check(TokenType.COMMA):
                    self.advance()
                    continue
                break
        
        if not self.match(TokenType.RPAREN):
            raise ParseError("需要右括號", self.peek())
        
        # 返回類型
        return_type = None
        if self.match(TokenType.COLON):
            if not self.check_type():
                raise ParseError("需要返回類型", self.peek())
            return_type_token = self.advance()
            return_type = return_type_token.value
        
        # 函數體
        if not self.match(TokenType.LBRACE):
            raise ParseError("需要左花括號", self.peek())
        
        body = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            stmt = self.statement()
            if stmt:
                body.append(stmt)
        
        if not self.match(TokenType.RBRACE):
            raise ParseError("需要右花括號", self.peek())
        
        return FunctionDef(
            name=name,
            params=params,
            return_type=return_type,
            body=body,
            line=name_token.line,
            column=name_token.column
        )
    
    def if_statement(self) -> IfStmt:
        """if 語句"""
        condition = self.expression()
        
        if not self.match(TokenType.LBRACE):
            raise ParseError("需要左花括號", self.peek())
        
        then_branch = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            stmt = self.statement()
            if stmt:
                then_branch.append(stmt)
        
        if not self.match(TokenType.RBRACE):
            raise ParseError("需要右花括號", self.peek())
        
        # elif 分支
        elif_branches = []
        while self.match(TokenType.ELIF):
            elif_cond = self.expression()
            
            if not self.match(TokenType.LBRACE):
                raise ParseError("需要左花括號", self.peek())
            
            elif_body = []
            while not self.check(TokenType.RBRACE) and not self.is_at_end():
                if self.check(TokenType.NEWLINE):
                    self.advance()
                    continue
                stmt = self.statement()
                if stmt:
                    elif_body.append(stmt)
            
            if not self.match(TokenType.RBRACE):
                raise ParseError("需要右花括號", self.peek())
            
            elif_branches.append((elif_cond, elif_body))
        
        # else 分支
        else_branch = []
        if self.match(TokenType.ELSE):
            if not self.match(TokenType.LBRACE):
                raise ParseError("需要左花括號", self.peek())
            
            while not self.check(TokenType.RBRACE) and not self.is_at_end():
                if self.check(TokenType.NEWLINE):
                    self.advance()
                    continue
                stmt = self.statement()
                if stmt:
                    else_branch.append(stmt)
            
            if not self.match(TokenType.RBRACE):
                raise ParseError("需要右花括號", self.peek())
        
        return IfStmt(
            condition=condition,
            then_branch=then_branch,
            elif_branches=elif_branches,
            else_branch=else_branch,
            line=condition.line,
            column=condition.column
        )
    
    def while_statement(self) -> WhileStmt:
        """while 語句"""
        condition = self.expression()
        
        if not self.match(TokenType.LBRACE):
            raise ParseError("需要左花括號", self.peek())
        
        body = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            stmt = self.statement()
            if stmt:
                body.append(stmt)
        
        if not self.match(TokenType.RBRACE):
            raise ParseError("需要右花括號", self.peek())
        
        return WhileStmt(
            condition=condition,
            body=body,
            line=condition.line,
            column=condition.column
        )
    
    def for_statement(self) -> ForStmt:
        """for 語句"""
        # 變數名稱
        if not self.check(TokenType.IDENTIFIER):
            raise ParseError("需要變數名稱", self.peek())
        
        var_token = self.advance()
        variable = var_token.value
        
        if not self.match(TokenType.ASSIGN):
            raise ParseError("需要等號", self.peek())
        
        start = self.expression()
        
        if not self.check(TokenType.COMMA):
            raise ParseError("需要逗號", self.peek())
        self.advance()
        
        end = self.expression()
        
        step = None
        if self.check(TokenType.COMMA):
            self.advance()
            step = self.expression()
        
        if not self.match(TokenType.LBRACE):
            raise ParseError("需要左花括號", self.peek())
        
        body = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            stmt = self.statement()
            if stmt:
                body.append(stmt)
        
        if not self.match(TokenType.RBRACE):
            raise ParseError("需要右花括號", self.peek())
        
        return ForStmt(
            variable=variable,
            start=start,
            end=end,
            step=step,
            body=body,
            line=var_token.line,
            column=var_token.column
        )
    
    def return_statement(self) -> ReturnStmt:
        """return 語句"""
        if self.check_type_statement_end():
            return ReturnStmt(value=None, line=self.peek().line, column=self.peek().column)
        
        value = self.expression()
        return ReturnStmt(value=value, line=value.line, column=value.column)
    
    def expression_statement(self) -> ASTNode:
        """表達式語句"""
        expr = self.expression()
        
        # 檢查是否是賦值
        if self.match(TokenType.ASSIGN):
            value = self.expression()
            return Assignment(target=expr, value=value, line=expr.line, column=expr.column)
        
        # 處理賦值到陣列元素
        if isinstance(expr, IndexAccess) and self.match(TokenType.ASSIGN):
            value = self.expression()
            return Assignment(target=expr, value=value, line=expr.line, column=expr.column)
        
        return expr
    
    # ============== 表達式解析 ==============
    
    def expression(self) -> ASTNode:
        """表達式 - or"""
        return self.or_expression()
    
    def or_expression(self) -> ASTNode:
        """邏輯 OR"""
        left = self.and_expression()
        
        while self.match(TokenType.OR):
            right = self.and_expression()
            left = BinaryOp(operator='or', left=left, right=right, line=left.line, column=left.column)
        
        return left
    
    def and_expression(self) -> ASTNode:
        """邏輯 AND"""
        left = self.equality_expression()
        
        while self.match(TokenType.AND):
            right = self.equality_expression()
            left = BinaryOp(operator='and', left=left, right=right, line=left.line, column=left.column)
        
        return left
    
    def equality_expression(self) -> ASTNode:
        """相等比較"""
        left = self.comparison_expression()
        
        while self.match(TokenType.EQ, TokenType.NEQ):
            op = self.previous().value
            right = self.comparison_expression()
            left = BinaryOp(operator=op, left=left, right=right, line=left.line, column=left.column)
        
        return left
    
    def comparison_expression(self) -> ASTNode:
        """大小比較"""
        left = self.additive_expression()
        
        while self.match(TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE):
            op = self.previous().value
            right = self.additive_expression()
            left = BinaryOp(operator=op, left=left, right=right, line=left.line, column=left.column)
        
        return left
    
    def additive_expression(self) -> ASTNode:
        """加法運算"""
        left = self.multiplicative_expression()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous().value
            right = self.multiplicative_expression()
            left = BinaryOp(operator=op, left=left, right=right, line=left.line, column=left.column)
        
        return left
    
    def multiplicative_expression(self) -> ASTNode:
        """乘法運算"""
        left = self.unary_expression()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.previous().value
            right = self.unary_expression()
            left = BinaryOp(operator=op, left=left, right=right, line=left.line, column=left.column)
        
        return left
    
    def unary_expression(self) -> ASTNode:
        """一元運算"""
        if self.match(TokenType.MINUS):
            operand = self.unary_expression()
            return UnaryOp(operator='-', operand=operand, line=operand.line, column=operand.column)
        
        if self.match(TokenType.NOT):
            operand = self.unary_expression()
            return UnaryOp(operator='not', operand=operand, line=operand.line, column=operand.column)
        
        return self.postfix_expression()
    
    def postfix_expression(self) -> ASTNode:
        """後綴運算（函數呼叫、陣列存取）"""
        expr = self.primary_expression()
        
        while True:
            if self.match(TokenType.LBRACKET):
                index = self.expression()
                if not self.match(TokenType.RBRACKET):
                    raise ParseError("需要右中括號", self.peek())
                expr = IndexAccess(array=expr, index=index, line=expr.line, column=expr.column)
            
            elif self.match(TokenType.LPAREN):
                args = []
                if not self.check(TokenType.RPAREN):
                    while True:
                        args.append(self.expression())
                        if self.check(TokenType.COMMA):
                            self.advance()
                            continue
                        break
                
                if not self.match(TokenType.RPAREN):
                    raise ParseError("需要右括號", self.peek())
                
                expr = FunctionCall(name=expr.name if isinstance(expr, Identifier) else "", 
                                   arguments=args, line=expr.line, column=expr.column)
            else:
                break
        
        return expr
    
    def primary_expression(self) -> ASTNode:
        """基本表達式"""
        token = self.peek()
        
        # 識別符號（變數或函數呼叫）
        if self.check(TokenType.IDENTIFIER):
            self.advance()
            name = token.value
            
            # 檢查是否是函數呼叫
            if self.check(TokenType.LPAREN):
                if not self.match(TokenType.LPAREN):
                    raise ParseError("需要左括號", self.peek())
                
                args = []
                if not self.check(TokenType.RPAREN):
                    while True:
                        args.append(self.expression())
                        if self.check(TokenType.COMMA):
                            self.advance()
                            continue
                        break
                
                if not self.match(TokenType.RPAREN):
                    raise ParseError("需要右括號", self.peek())
                
                return FunctionCall(name=name, arguments=args, line=token.line, column=token.column)
            
            return Identifier(name=name, line=token.line, column=token.column)
        
        # 數字
        if self.check(TokenType.INT):
            self.advance()
            return Literal(value=token.value, literal_type='int', line=token.line, column=token.column)
        
        if self.check(TokenType.FLOAT):
            self.advance()
            return Literal(value=token.value, literal_type='float', line=token.line, column=token.column)
        
        # 字串
        if self.check(TokenType.STRING):
            self.advance()
            return Literal(value=token.value, literal_type='string', line=token.line, column=token.column)
        
        # 布林值
        if self.check(TokenType.TRUE):
            self.advance()
            return Literal(value=True, literal_type='bool', line=token.line, column=token.column)
        
        if self.check(TokenType.FALSE):
            self.advance()
            return Literal(value=False, literal_type='bool', line=token.line, column=token.column)
        
        # 陣列
        if self.match(TokenType.LBRACKET):
            elements = []
            if not self.check(TokenType.RBRACKET):
                while True:
                    elements.append(self.expression())
                    if self.check(TokenType.COMMA):
                        self.advance()
                        continue
                    break
            
            if not self.match(TokenType.RBRACKET):
                raise ParseError("需要右中括號", self.peek())
            
            return ArrayLiteral(elements=elements, line=token.line, column=token.column)
        
        # lambda 表達式
        if self.match(TokenType.FN):
            return self.lambda_expression()
        
        # 分組表達式
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            if not self.match(TokenType.RPAREN):
                raise ParseError("需要右括號", self.peek())
            return expr
        
        raise ParseError(f"無法解析表達式: {token.value if token else 'EOF'}", token)
    
    def lambda_expression(self):
        """lambda 表達式"""
        # 參數
        params = []
        if not self.check(TokenType.LBRACE):
            if not self.check(TokenType.RPAREN):
                while True:
                    if not self.check(TokenType.IDENTIFIER):
                        break
                    param_token = self.advance()
                    params.append((param_token.value, 'auto'))
                    
                    if self.check(TokenType.COMMA):
                        self.advance()
                        continue
                    break
        
        if not self.match(TokenType.LBRACE):
            raise ParseError("需要左花括號", self.peek())
        
        body = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            stmt = self.statement()
            if stmt:
                body.append(stmt)
        
        if not self.match(TokenType.RBRACE):
            raise ParseError("需要右花括號", self.peek())
        
        return FunctionDef(name='', params=params, body=body, line=1, column=1)
    
    # ============== 輔助方法 ==============
    
    def check_type(self) -> bool:
        """檢查是否是類型"""
        return self.check(TokenType.INT, TokenType.FLOAT, TokenType.STRING, 
                        TokenType.BOOL, TokenType.ARRAY)
    
    def check_type_statement_end(self) -> bool:
        """檢查是否結束語句"""
        return self.check(TokenType.NEWLINE, TokenType.EOF, TokenType.RBRACE)
    
    def check(self, *types) -> bool:
        """檢查當前 Token 類型"""
        if self.is_at_end():
            return False
        return self.peek().type in types
    
    def match(self, *types) -> bool:
        """匹配並前進"""
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False
    
    def previous(self) -> Token:
        """取得前一個 Token"""
        return self.tokens[self.pos - 1]
    
    def peek(self) -> Token:
        """查看當前 Token"""
        if self.is_at_end():
            return Token(TokenType.EOF, None, 0, 0)
        return self.tokens[self.pos]
    
    def advance(self) -> Token:
        """前進到下一個 Token"""
        if not self.is_at_end():
            self.pos += 1
        return self.previous()
    
    def is_at_end(self) -> bool:
        return self.pos >= len(self.tokens) or self.peek().type == TokenType.EOF


def parse(tokens: List[Token]) -> Program:
    """方便的解析函數"""
    parser = Parser(tokens)
    return parser.parse()


if __name__ == "__main__":
    from lexer import tokenize
    
    source = """
    let x: int = 10;
    let y: int = 20;
    let sum: int = x + y;
    print(sum);
    """
    
    tokens = tokenize(source)
    program = parse(tokens)
    print(f"Program has {len(program.statements)} statements")