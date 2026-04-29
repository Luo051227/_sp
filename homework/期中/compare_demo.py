#!/usr/bin/env python3
"""
安全 vs 不安全程式碼對比
說明：展示正確和錯誤的程式寫法
執行：python3 compare_demo.py
"""

print("=" * 60)
print("       安全 vs 不安全程式碼對比")
print("=" * 60)

# ═══════════════════════════════════════════
# 範例 1：陣列存取
# ═══════════════════════════════════════════
print("\n【範例 1】陣列存取")
print("-" * 40)

print("""
❌ 不安全（概念）- C 語言:
   int arr[5] = {1,2,3,4,5};
   arr[10] = 5;  // 可能超出範圍！危險！

✅ 安全 - Python:
   arr = [1, 2, 3, 4, 5]
   arr[10] = 5  # 會報錯！保護你！
""")

# Python 實際展示
arr = [1, 2, 3, 4, 5]
print(f"   列表: {arr}")

# 安全存取
print(f"   arr[0] = {arr[0]} ✓")

# 嘗試錯誤存取會被阻止
try:
    _ = arr[100]
except IndexError as e:
    print(f"   arr[100] 被阻止！Python 保護了你！✓")

# ═══════════════════════════════════════════
# 範例 2：指標檢查
# ═══════════════════════════════════════════
print("\n【範例 2】指標檢查")
print("-" * 40)

print("""
❌ 不安全（概念）- C 語言:
   int* ptr = NULL;
   *ptr = 10;  // 崩潰！空指標解引用

✅ 安全 - Python:
   data = None
   # Python 不允許解引用 None
""")

# Python 實際展示
data = None
try:
    _ = data + 1
except TypeError as e:
    print(f"   嘗試操作 None 被阻止！✓")
    print(f"   錯誤訊息: {e}")

# ═══════════════════════════════════════════
# 範例 3：記憶體管理
# ═══════════════════════════════════════════
print("\n【範例 3】記憶體管理")
print("-" * 40)

print("""
❌ 不安全（概念）- C 語言:
   char* ptr = malloc(100);
   // 用完了但沒釋放
   // 造成記憶體泄漏！
   // 程式越跑越慢...

✅ 安全 - Python:
   data = [1, 2, 3]  # 建立資料
   # 用完了不用處理
   # Python 會自動清理！
""")

# Python 實際展示
import gc

def memory_demo():
    large_data = [i for i in range(10000)]
    print(f"   建立大資料: {len(large_data)} 元素")

# 執行函數
memory_demo()
print("   函數結束後，記憶體自動被清理！✓")

# ═══════════════════════════════════════════
# 範例 4：邊界檢查
# ═══════════════════════════════════════════
print("\n【範例 4】邊界檢查")
print("-" * 40)

print("""
❌ 不安全（概念）- C 語言:
   for (int i = 0; i <= 10; i++) {
       arr[i] = 0;  // 可能超出！
   }

✅ 安全 - Python:
   arr = [1,2,3,4,5]
   for i in range(len(arr)):  # 只會在範圍內
       arr[i] = 0
""")

# Python 實際展示
arr = [1, 2, 3, 4, 5]
print(f"   原始列表: {arr}")

for i in range(len(arr)):
    arr[i] = 0

print(f"   修改後: {arr}")
print("   不會超出範圍！✓")

# ═══════════════════════════════════════════
# 範例 5：型別安全
# ═══════════════════════════════════════════
print("\n【範例 5】型別安全")
print("-" * 40)

print("""
❌ 不安全（概念）- C 語言:
   int num = 10;
   char* str = "hello";
   num = str;  // 可能編譯通過但執行出錯

✅ 安全 - Python:
   num = 10
   str = "hello"
   num = str  # 運行時會報錯！
""")

# Python 實際展示
num = 10
text = "hello"

try:
    result = num + text
except TypeError as e:
    print(f"   型別混用被阻止！✓")
    print(f"   錯誤訊息: {e}")

# ═══════════════════════════════════════════
# 範例 6：除零檢查
# ═══════════════════════════════════════════
print("\n【範例 6】除零檢查")
print("-" * 40)

print("""
❌ 不安全（概念）- C 語言:
   int a = 10;
   int b = 0;
   int c = a / b;  // 未定義行為！

✅ 安全 - Python:
   a = 10
   b = 0
   c = a / b  # 會報錯 ZeroDivisionError
""")

# Python 實際展示
a = 10
b = 0

try:
    c = a / b
except ZeroDivisionError as e:
    print(f"   除以零被阻止！✓")
    print(f"   錯誤訊息: {e}")

# ═══════════════════════════════════════════
# 範例 7：物件生命週期
# ═══════════════════════════════════════════
print("\n【範例 7】物件生命週期")
print("-" * 40)

print("""
❌ 不安全（概念）- C++ 語言:
   {
       MyClass* obj = new MyClass();
   } // 記憶體泄漏！忘記 delete

✅ 安全 - Python:
   {
       obj = MyClass()
   } # Python 自動管理！
""")

# Python 實際展示
class Demo:
    def __init__(self):
        print("   建立物件")
    def __del__(self):
        print("   物件被清理")

print("   建立物件1:")
obj1 = Demo()

print("   建立物件2:")
obj2 = Demo()

print("   刪除物件1:")
del obj1

print("   刪除物件2:")
del obj2

print("   Python 自動管理物件生命週期！✓")

print()
print("=" * 60)
print("💡 結論：使用 Python 這種安全語言，讓記憶體問題遠離你！")
print("   - 自動邊界檢查")
print("   - 自動記憶體管理")
print("   - 自動垃圾回收")
print("   - 強型別檢查")
print("=" * 60)