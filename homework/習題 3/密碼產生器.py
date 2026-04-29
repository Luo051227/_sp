#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
密碼產生器 - 圖形介面版本
功能：產生安全密碼，包含大小寫字母、數字、特殊符號
執行：python3 密碼產生器.py
"""

import random
import string
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


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
            exclude_ambiguous: 排除容易混淆的字元 (0, O, l, 1, I)
        
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
        """
        產生易記的密碼片語
        
        參數:
            word_count: 單字數量
            separator: 分隔符
        
        回傳:
            密碼片語
        """
        words = [
            'apple', 'banana', 'cherry', 'dragon', 'eagle', 'forest',
            'garden', 'harbor', 'island', 'jungle', 'knight', 'lemon',
            'mountain', 'nebula', 'ocean', 'phoenix', 'quantum', 'river',
            'sunset', 'thunder', 'umbrella', 'valley', 'winter', 'xenon',
            'yellow', 'zebra', 'brave', 'cloud', 'dance', 'earth'
        ]
        
        # 隨機選擇單字，首字母大寫
        selected = [random.choice(words).capitalize() for _ in range(word_count)]
        
        return separator.join(selected)
    
    def calculate_strength(self, password):
        """
        計算密碼強度
        
        參數:
            password: 要評估的密碼
        
        回傳:
            (強度等级, 描述)
        """
        length = len(password)
        has_lower = any(c in self.lowercase for c in password)
        has_upper = any(c in self.uppercase for c in password)
        has_digit = any(c in self.digits for c in password)
        has_punct = any(c in self.punctuation for c in password)
        
        score = 0
        
        # 長度分數
        if length >= 16:
            score += 3
        elif length >= 12:
            score += 2
        elif length >= 8:
            score += 1
        
        # 字元類型分數
        if has_lower:
            score += 1
        if has_upper:
            score += 1
        if has_digit:
            score += 1
        if has_punct:
            score += 1
        
        # 評估結果
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


class PasswordGeneratorApp:
    """密碼產生器 GUI 應用程式"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 密碼產生器")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        self.generator = PasswordGenerator()
        
        self.setup_ui()
    
    def setup_ui(self):
        """設定使用者介面"""
        
        # 標題
        title_label = tk.Label(
            self.root, 
            text="密碼產生器", 
            font=("Microsoft JhengHei", 20, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=15)
        
        # 設定框架
        settings_frame = ttk.LabelFrame(self.root, text="密碼設定", padding=10)
        settings_frame.pack(fill="x", padx=20, pady=5)
        
        # 密碼長度
        length_frame = tk.Frame(settings_frame)
        length_frame.pack(fill="x", pady=5)
        
        tk.Label(length_frame, text="密碼長度:", font=("Microsoft JhengHei", 10)).pack(side="left")
        
        self.length_var = tk.IntVar(value=16)
        length_spin = ttk.Spinbox(
            length_frame, 
            from_=4, 
            to=64, 
            textvariable=self.length_var,
            width=10,
            font=("Microsoft JhengHei", 10)
        )
        length_spin.pack(side="left", padx=10)
        
        # 選項框架
        options_frame = tk.Frame(settings_frame)
        options_frame.pack(fill="x", pady=5)
        
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_punctuation = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(
            options_frame, 
            text="包含大寫字母 (A-Z)",
            variable=self.use_uppercase
        ).pack(anchor="w", pady=2)
        
        ttk.Checkbutton(
            options_frame, 
            text="包含數字 (0-9)",
            variable=self.use_digits
        ).pack(anchor="w", pady=2)
        
        ttk.Checkbutton(
            options_frame, 
            text="包含特殊符號 (!@#$%^&*)",
            variable=self.use_punctuation
        ).pack(anchor="w", pady=2)
        
        ttk.Checkbutton(
            options_frame, 
            text="排除容易混淆的字元 (0,O,l,1,I)",
            variable=self.exclude_ambiguous
        ).pack(anchor="w", pady=2)
        
        # 產生按鈕框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)
        
        generate_btn = tk.Button(
            button_frame,
            text="🔑 產生密碼",
            font=("Microsoft JhengHei", 12, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=8,
            command=self.generate_password
        )
        generate_btn.pack(side="left", padx=5)
        
        memorable_btn = tk.Button(
            button_frame,
            text="📝 產生片語",
            font=("Microsoft JhengHei", 12),
            bg="#9b59b6",
            fg="white",
            padx=20,
            pady=8,
            command=self.generate_memorable
        )
        memorable_btn.pack(side="left", padx=5)
        
        # 密碼顯示框架
        result_frame = ttk.LabelFrame(self.root, text="產生的密碼", padding=10)
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.password_text = tk.Text(
            result_frame,
            font=("Consolas", 14),
            height=3,
            wrap="word",
            bg="#ecf0f1"
        )
        self.password_text.pack(fill="x")
        
        # 複製按鈕
        copy_btn = tk.Button(
            self.root,
            text="📋 複製到剪貼簿",
            font=("Microsoft JhengHei", 10),
            bg="#27ae60",
            fg="white",
            padx=15,
            pady=5,
            command=self.copy_password
        )
        copy_btn.pack(pady=5)
        
        # 強度顯示
        strength_frame = tk.Frame(self.root)
        strength_frame.pack(pady=5)
        
        tk.Label(strength_frame, text="密碼強度:", font=("Microsoft JhengHei", 10)).pack(side="left")
        
        self.strength_label = tk.Label(
            strength_frame,
            text="",
            font=("Microsoft JhengHei", 10, "bold"),
            fg="#e74c3c"
        )
        self.strength_label.pack(side="left", padx=5)
        
        # 密碼歷史框架
        history_frame = ttk.LabelFrame(self.root, text="密碼歷史", padding=5)
        history_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.history_text = scrolledtext.ScrolledText(
            history_frame,
            font=("Consolas", 9),
            height=5,
            bg="#f8f9fa"
        )
        self.history_text.pack(fill="both", expand=True)
        
        self.history_count = 0
    
    def generate_password(self):
        """產生一般密碼"""
        password = self.generator.generate(
            length=self.length_var.get(),
            use_uppercase=self.use_uppercase.get(),
            use_digits=self.use_digits.get(),
            use_punctuation=self.use_punctuation.get(),
            exclude_ambiguous=self.exclude_ambiguous.get()
        )
        
        self.display_password(password, "一般密碼")
    
    def generate_memorable(self):
        """產生易記片語密碼"""
        password = self.generator.generate_memorable(word_count=4)
        
        self.display_password(password, "片語密碼")
    
    def display_password(self, password, ptype):
        """顯示密碼"""
        # 清除舊內容
        self.password_text.delete("1.0", "end")
        
        # 顯示新密碼
        self.password_text.insert("1.0", password)
        
        # 計算並顯示強度
        strength, desc = self.generator.calculate_strength(password)
        self.strength_label.config(text=f"{strength} {desc}")
        
        # 根據強度設置顏色
        if '強' in desc:
            self.strength_label.config(fg="#27ae60")
        elif '中等' in desc:
            self.strength_label.config(fg="#f39c12")
        else:
            self.strength_label.config(fg="#e74c3c")
        
        # 添加到歷史
        self.history_count += 1
        self.history_text.insert("end", f"{self.history_count}. [{ptype}] {password}\n")
        
        # 限制歷史數量
        if self.history_count > 10:
            self.history_text.delete("2.0", "3.0")
    
    def copy_password(self):
        """複製密碼到剪貼簿"""
        password = self.password_text.get("1.0", "end").strip()
        
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("成功", "密碼已複製到剪貼簿！")
        else:
            messagebox.showwarning("警告", "請先產生密碼！")


def main():
    """主函數"""
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()