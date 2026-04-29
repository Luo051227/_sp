#!/usr/bin/env python3
"""
SimpleScript 直譯器 (Interpreter)
執行 AST 並產生結果
"""

import sys
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

from parser import (
    Program, ASTNode, VariableDecl, Assignment, Identifier, Literal,
    BinaryOp, UnaryOp, IndexAccess, FunctionCall, FunctionDef,
    ReturnStmt, IfStmt, WhileStmt, ForStmt, ImportStmt, ArrayLiteral
)


class RuntimeError(Exception):
    """執行階段錯誤"""
    def __init__(self, message: str, line: int = 0, column: int = 0):
        self.line = line
        self.column = column
        super().__init__(f"執行錯誤 at line {line}: {message}")


class Function:
    """函數物件"""
    def __init__(self, name: str, params: List[tuple], return_type: Optional[str], body: List[ASTNode], closure: Dict):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body
        self.closure = closure  # 閉包環境


class SSArray:
    """SimpleScript 陣列"""
    def __init__(self, elements: List[Any]):
        self.elements = elements
        self._refcount = 0
    
    def __len__(self):
        return len(self.elements)
    
    def __getitem__(self, index):
        return self.elements[index]
    
    def __setitem__(self, index, value):
        self.elements[index] = value
    
    def __str__(self):
        return "[" + ", ".join(str(e) for e in self.elements) + "]"
    
    def __repr__(self):
        return self.__str__()


class Interpreter:
    """直譯器"""
    
    def __init__(self):
        # 全域變數環境
        self.global_env: Dict[str, Any] = {}
        
        # 函數定義
        self.functions: Dict[str, Function] = {}
        
        # 當前環境
        self.env: Dict[str, Any] = {}
        
        # 回傳值
        self.return_value: Any = None
        self.return_set: bool = False
        
        # 內建函數
        self.setup_builtins()
    
    def setup_builtins(self):
        """設定內建函數"""
        self.functions['print'] = Function('print', [], None, [], {})
        self.functions['len'] = Function('len', [], None, [], {})
        self.functions['str'] = Function('str', [], None, [], {})
        self.functions['int'] = Function('int', [], None, [], {})
        self.functions['float'] = Function('float', [], None, [], {})
        self.functions['input'] = Function('input', [], None, [], {})
        self.functions['range'] = Function('range', [], None, [], {})
    
    def interpret(self, program: Program):
        """執行程式"""
        # 執行所有語句
        for stmt in program.statements:
            if isinstance(stmt, ImportStmt):
                self.execute_import(stmt)
            elif not self.return_set:
                self.execute(stmt)
        
        return self.global_env
    
    def execute_import(self, stmt: ImportStmt):
        """執行匯入"""
        module_path = stmt.module_path
        
        # 移除 .ss 副檔名
        if module_path.endswith('.ss'):
            module_path = module_path[:-3]
        
        # 嘗試讀取檔案
        full_path = module_path + '.ss'
        
        if not os.path.exists(full_path):
            raise RuntimeError(f"找不到模組: {full_path}", stmt.line, stmt.column)
        
        # 讀取並執行模組
        with open(full_path, 'r') as f:
            source = f.read()
        
        # 為模組創建新的直譯器
        module_interpreter = Interpreter()
        
        # 執行模組
        from lexer import tokenize
        from parser import parse
        
        tokens = tokenize(source)
        module_program = parse(tokens)
        module_interpreter.interpret(module_program)
        
        # 將模組的全局變數添加到當前環境
        for key, value in module_interpreter.global_env.items():
            self.global_env[key] = value
    
    def execute(self, node: ASTNode) -> Any:
        """執行 AST 節點"""
        if isinstance(node, Program):
            for stmt in node.statements:
                if self.return_set:
                    break
                self.execute(stmt)
        
        elif isinstance(node, VariableDecl):
            value = None
            if node.value:
                value = self.evaluate(node.value)
            
            # 類型檢查（簡單版）
            if node.var_type == 'int' and value is not None:
                value = int(value)
            elif node.var_type == 'float' and value is not None:
                value = float(value)
            elif node.var_type == 'string' and value is not None:
                value = str(value)
            elif node.var_type == 'bool' and value is not None:
                value = bool(value)
            elif node.var_type == 'array' and value is None:
                value = SSArray([])
            elif node.var_type == 'array' and isinstance(value, list):
                value = SSArray(value)
            
            self.env[node.name] = value
        
        elif isinstance(node, Assignment):
            target = node.target
            value = self.evaluate(node.value)
            
            if isinstance(target, Identifier):
                # 檢查是否是函數內部
                if target.name in self.env:
                    self.env[target.name] = value
                else:
                    self.global_env[target.name] = value
            
            elif isinstance(target, IndexAccess):
                arr = self.evaluate(target.array)
                if isinstance(arr, SSArray):
                    idx = self.evaluate(target.index)
                    arr[int(idx)] = value
                elif isinstance(arr, list):
                    arr[int(idx)] = value
        
        elif isinstance(node, Identifier):
            if node.name in self.env:
                return self.env[node.name]
            elif node.name in self.global_env:
                return self.global_env[node.name]
            elif node.name in self.functions:
                return self.functions[node.name]
            else:
                raise RuntimeError(f"未定義的變數: {node.name}", node.line, node.column)
        
        elif isinstance(node, Literal):
            return node.value
        
        elif isinstance(node, ArrayLiteral):
            elements = [self.evaluate(e) for e in node.elements]
            return SSArray(elements)
        
        elif isinstance(node, BinaryOp):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            
            if node.operator == '+':
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            elif node.operator == '-':
                return left - right
            elif node.operator == '*':
                return left * right
            elif node.operator == '/':
                return left // right  # 整數除法
            elif node.operator == '%':
                return left % right
            elif node.operator == '==':
                return left == right
            elif node.operator == '!=':
                return left != right
            elif node.operator == '<':
                return left < right
            elif node.operator == '>':
                return left > right
            elif node.operator == '<=':
                return left <= right
            elif node.operator == '>=':
                return left >= right
            elif node.operator == 'and':
                return left and right
            elif node.operator == 'or':
                return left or right
        
        elif isinstance(node, UnaryOp):
            operand = self.evaluate(node.operand)
            
            if node.operator == '-':
                return -operand
            elif node.operator == 'not':
                return not operand
        
        elif isinstance(node, IndexAccess):
            arr = self.evaluate(node.array)
            idx = self.evaluate(node.index)
            
            if isinstance(arr, SSArray):
                return arr[int(idx)]
            elif isinstance(arr, list):
                return arr[int(idx)]
            elif isinstance(arr, str):
                return arr[int(idx)]
        
        elif isinstance(node, FunctionCall):
            return self.call_function(node.name, node.arguments, node.line, node.column)
        
        elif isinstance(node, FunctionDef):
            self.functions[node.name] = Function(
                node.name, node.params, node.return_type, node.body, {}
            )
        
        elif isinstance(node, ReturnStmt):
            self.return_set = True
            if node.value:
                self.return_value = self.evaluate(node.value)
        
        elif isinstance(node, IfStmt):
            if self.evaluate(node.condition):
                for stmt in node.then_branch:
                    if self.return_set:
                        break
                    self.execute(stmt)
            else:
                executed = False
                for cond, body in node.elif_branches:
                    if self.evaluate(cond):
                        for stmt in body:
                            if self.return_set:
                                break
                            self.execute(stmt)
                        executed = True
                        break
                
                if not executed and node.else_branch:
                    for stmt in node.else_branch:
                        if self.return_set:
                            break
                        self.execute(stmt)
        
        elif isinstance(node, WhileStmt):
            while self.evaluate(node.condition):
                for stmt in node.body:
                    if self.return_set:
                        break
                    self.execute(stmt)
        
        elif isinstance(node, ForStmt):
            start_val = self.evaluate(node.start)
            end_val = self.evaluate(node.end)
            step_val = self.evaluate(node.step) if node.step else 1
            
            for i in range(int(start_val), int(end_val), int(step_val)):
                self.env[node.variable] = i
                for stmt in node.body:
                    if self.return_set:
                        break
                    self.execute(stmt)
    
    def call_function(self, name: str, args: List[ASTNode], line: int, column: int) -> Any:
        """呼叫函數"""
        # 內建函數
        if name == 'print':
            values = [self.evaluate(arg) for arg in args]
            print(*values, sep='')
            return None
        
        elif name == 'len':
            arg = self.evaluate(args[0]) if args else None
            if isinstance(arg, SSArray):
                return len(arg.elements)
            elif isinstance(arg, list):
                return len(arg)
            elif isinstance(arg, str):
                return len(arg)
            return 0
        
        elif name == 'str':
            arg = self.evaluate(args[0]) if args else None
            return str(arg)
        
        elif name == 'int':
            arg = self.evaluate(args[0]) if args else None
            return int(arg)
        
        elif name == 'float':
            arg = self.evaluate(args[0]) if args else None
            return float(arg)
        
        elif name == 'input':
            prompt = self.evaluate(args[0]) if args else ""
            return input(str(prompt))
        
        elif name == 'range':
            if len(args) == 1:
                return range(self.evaluate(args[0]))
            elif len(args) == 2:
                return range(self.evaluate(args[0]), self.evaluate(args[1]))
            elif len(args) == 3:
                return range(self.evaluate(args[0]), self.evaluate(args[1]), self.evaluate(args[2]))
            return range(0)
        
        # 用戶自定義函數
        if name not in self.functions:
            raise RuntimeError(f"未定義的函數: {name}", line, column)
        
        func = self.functions[name]
        
        # 保存當前環境
        saved_env = self.env
        saved_return = self.return_set
        saved_value = self.return_value
        
        # 創建新環境
        self.env = func.closure.copy()
        
        # 綁定參數
        for i, (param_name, _) in enumerate(func.params):
            if i < len(args):
                self.env[param_name] = self.evaluate(args[i])
        
        # 執行函數體
        self.return_set = False
        self.return_value = None
        
        for stmt in func.body:
            self.execute(stmt)
            if self.return_set:
                break
        
        result = self.return_value
        
        # 恢復環境
        self.env = saved_env
        self.return_set = saved_return
        self.return_value = saved_value
        
        return result
    
    def evaluate(self, node: ASTNode) -> Any:
        """計算表達式"""
        return self.execute(node)


def run(source: str) -> Dict[str, Any]:
    """執行 SimpleScript 程式碼"""
    from lexer import tokenize
    from parser import parse
    
    tokens = tokenize(source)
    program = parse(tokens)
    
    interpreter = Interpreter()
    return interpreter.interpret(program)


if __name__ == "__main__":
    # 測試
    source = """
    let x: int = 10;
    let y: int = 20;
    let sum: int = x + y;
    print("x + y = ");
    print(sum);
    """
    
    run(source)