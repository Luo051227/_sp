#!/usr/bin/env python3
"""
SimpleScript 直譯器 - 主程式
執行 .ss 檔案或進入互動模式
"""

import sys
import os

def main():
    """主函數"""
    if len(sys.argv) < 2:
        # 互動模式
        run_interactive()
    else:
        # 執行檔案
        filename = sys.argv[1]
        if not filename.endswith('.ss'):
            filename += '.ss'
        
        if not os.path.exists(filename):
            print(f"錯誤: 找不到檔案 {filename}")
            sys.exit(1)
        
        run_file(filename)


def run_file(filename: str):
    """執行 SimpleScript 檔案"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        print(f"執行 {filename}...")
        print("-" * 40)
        
        from lexer import tokenize
        from parser import parse
        from interpreter import Interpreter
        
        tokens = tokenize(source)
        program = parse(tokens)
        
        interpreter = Interpreter()
        interpreter.interpret(program)
        
        print("-" * 40)
        print("執行完成")
        
    except Exception as e:
        print(f"錯誤: {e}")
        sys.exit(1)


def run_interactive():
    """互動模式"""
    print("=" * 50)
    print("  SimpleScript 直譯器 - 互動模式")
    print("  輸入 exit() 離開")
    print("=" * 50)
    print()
    
    from lexer import tokenize
    from parser import parse
    from interpreter import Interpreter
    
    while True:
        try:
            source = input(">>> ")
            
            if source.strip() == 'exit()':
                break
            
            if not source.strip():
                continue
            
            # 單行模式
            if '\n' not in source and ';' not in source:
                # 檢查是否是表達式
                tokens = tokenize(source)
                
                if tokens and tokens[0].type.value in ['IDENTIFIER', 'INT', 'FLOAT', 'STRING', 'TRUE', 'FALSE']:
                    # 當作表達式執行
                    try:
                        program = parse(tokens)
                        interpreter = Interpreter()
                        result = interpreter.interpret(program)
                        
                        # 嘗試找出結果
                        if interpreter.return_set:
                            print(interpreter.return_value)
                    except:
                        pass
                else:
                    # 當作語句執行
                    try:
                        source_with_semicolon = source + ";"
                        tokens = tokenize(source_with_semicolon)
                        program = parse(tokens)
                        interpreter = Interpreter()
                        interpreter.interpret(program)
                    except Exception as e:
                        print(f"錯誤: {e}")
            else:
                # 多行模式
                try:
                    program = parse(tokenize(source))
                    interpreter = Interpreter()
                    result = interpreter.interpret(program)
                except Exception as e:
                    print(f"錯誤: {e}")
                    
        except KeyboardInterrupt:
            print("\nBye!")
            break
        except EOFError:
            break
        except Exception as e:
            print(f"錯誤: {e}")


if __name__ == "__main__":
    main()