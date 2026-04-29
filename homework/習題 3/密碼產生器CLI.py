#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
密碼產生器 - 命令列版本
功能：從命令列產生安全密碼
執行：python3 密碼產生器CLI.py [-l 長度] [-u] [-d] [-p] [-e]
"""

import random
import string
import argparse
import sys


class PasswordGenerator:
    """密碼產生器類別"""
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.punctuation = string.punctuation
    
    def generate(self, length=16, use_uppercase=True, use_digits=True, 
                 use_punctuation=True, exclude_ambiguous=False):
        """
        產生隨機密碼
        
        參數:
            length: 密碼長度
            use_uppercase: 包含大寫字母
            use_digits: 包含數字
            use_punctuation: 包含特殊符號
            exclude_ambiguous: 排除容易混淆的字元
        
        回傳:
            產生的密碼字串
        """
        # 構建字元集
        chars = self.lowercase
        
        if use_uppercase:
            chars += self.uppercase
        
        if use_digits:
            chars += self.digits
        
        if use_punctuation:
            chars += self.punctuation
        
        # 排除容易混淆的字元
        if exclude_ambiguous:
            ambiguous = '0O1lI'
            chars = ''.join(c for c in chars if c not in ambiguous)
        
        # 確保至少有一個字元
        if not chars:
            chars = self.lowercase
        
        # 產生密碼
        password = ''.join(random.choice(chars) for _ in range(length))
        
        return password
    
    def generate_memorable(self, word_count=4, separator='-'):
        """產生易記的密碼片語"""
        words = [
            'apple', 'banana', 'cherry', 'dragon', 'eagle', 'forest',
            'garden', 'harbor', 'island', 'jungle', 'knight', 'lemon',
            'mountain', 'nebula', 'ocean', 'phoenix', 'quantum', 'river',
            'sunset', 'thunder', 'umbrella', 'valley', 'winter', 'xenon',
            'yellow', 'zebra', 'brave', 'cloud', 'dance', 'earth'
        ]
        
        selected = [random.choice(words).capitalize() for _ in range(word_count)]
        
        return separator.join(selected)
    
    def calculate_strength(self, password):
        """計算密碼強度"""
        length = len(password)
        has_lower = any(c in self.lowercase for c in password)
        has_upper = any(c in self.uppercase for c in password)
        has_digit = any(c in self.digits for c in password)
        has_punct = any(c in self.punctuation for c in password)
        
        score = 0
        
        if length >= 16:
            score += 3
        elif length >= 12:
            score += 2
        elif length >= 8:
            score += 1
        
        if has_lower:
            score += 1
        if has_upper:
            score += 1
        if has_digit:
            score += 1
        if has_punct:
            score += 1
        
        if score >= 7:
            return ('★★★★★', '非常強')
        elif score >= 5:
            return ('★★★★☆', '強')
        elif score >= 3:
            return ('★★★☆☆', '中等')
        elif score >= 2:
            return ('★★☆☆☆', '弱')
        else:
            return ('★☆☆☆☆', '非常弱')


def parse_args():
    """解析命令列參數"""
    parser = argparse.ArgumentParser(
        description='密碼產生器 - 產生安全的隨機密碼',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  %(prog)s                                    產生預設密碼（16字元）
  %(prog)s -l 20                              產生20字元密碼
  %(prog)s -l 12 -u -d -p                     產生包含大小寫、數字、特殊符號的密碼
  %(prog)s --memorable                        產生易記片語密碼
  %(prog)s -n 5                               一次產生5個密碼

注意事項:
  建議密碼長度至少12個字元，並包含多種字元類型以獲得更強的安全性。
        '''
    )
    
    parser.add_argument(
        '-l', '--length',
        type=int,
        default=16,
        help='密碼長度 (預設: 16)'
    )
    
    parser.add_argument(
        '-u', '--uppercase',
        action='store_true',
        default=True,
        help='包含大寫字母 (預設: 啟用)'
    )
    
    parser.add_argument(
        '-d', '--digits',
        action='store_true',
        default=True,
        help='包含數字 (預設: 啟用)'
    )
    
    parser.add_argument(
        '-p', '--punctuation',
        action='store_true',
        default=True,
        help='包含特殊符號 (預設: 啟用)'
    )
    
    parser.add_argument(
        '-e', '--exclude-ambiguous',
        action='store_true',
        help='排除容易混淆的字元 (0, O, l, 1, I)'
    )
    
    parser.add_argument(
        '-n', '--count',
        type=int,
        default=1,
        help='一次產生的密碼數量 (預設: 1)'
    )
    
    parser.add_argument(
        '-m', '--memorable',
        action='store_true',
        help='產生易記的片語密碼'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='安靜模式，只輸出密碼'
    )
    
    return parser.parse_args()


def print_banner():
    """輸出橫幅"""
    print("=" * 50)
    print("       🔐 密碼產生器 (命令列版本)")
    print("=" * 50)


def main():
    """主函數"""
    args = parse_args()
    
    generator = PasswordGenerator()
    
    # 驗證參數
    if args.length < 4:
        print("錯誤：密碼長度至少需要4個字元", file=sys.stderr)
        sys.exit(1)
    
    if args.count < 1 or args.count > 100:
        print("錯誤：密碼數量必須在1-100之間", file=sys.stderr)
        sys.exit(1)
    
    # 檢查是否沒有選擇任何字元類型
    if not (args.uppercase or args.digits or args.punctuation):
        print("警告：未選擇任何字元類型，將使用小寫字母", file=sys.stderr)
    
    # 產生密碼
    if args.memorable:
        # 易記片語模式
        passwords = [generator.generate_memorable() for _ in range(args.count)]
        ptype = "片語密碼"
    else:
        # 一般模式
        passwords = [
            generator.generate(
                length=args.length,
                use_uppercase=args.uppercase,
                use_digits=args.digits,
                use_punctuation=args.punctuation,
                exclude_ambiguous=args.exclude_ambiguous
            )
            for _ in range(args.count)
        ]
        ptype = "一般密碼"
    
    # 輸出結果
    if args.quiet:
        # 安靜模式
        for p in passwords:
            print(p)
    else:
        # 一般模式
        if args.count == 1:
            print_banner()
            print(f"\n密碼類型: {ptype}")
            print(f"密碼長度: {args.length}")
            print(f"\n{'─' * 50}")
            print(f"  {passwords[0]}")
            print(f"{'─' * 50}")
            
            strength, desc = generator.calculate_strength(passwords[0])
            print(f"密碼強度: {strength} {desc}")
        else:
            print_banner()
            print(f"\n密碼類型: {ptype}")
            print(f"密碼數量: {args.count}\n")
            
            for i, p in enumerate(passwords, 1):
                strength, _ = generator.calculate_strength(p)
                print(f"{i:2d}. {p}  {strength}")


if __name__ == "__main__":
    main()