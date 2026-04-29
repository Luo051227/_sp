#!/usr/bin/env python3
"""
記憶體安全示範 - Python 版本
說明：Python 有自動記憶體管理，非常安全！
執行：python3 safe_demo.py
"""

print("=" * 60)
print("       記憶體安全示範 - Python 版本")
print("=" * 60)

# ═══════════════════════════════════════════
# 範例 1：列表邊界檢查
# ═══════════════════════════════════════════
print("\n【範例 1】列表邊界檢查")
print("-" * 40)

numbers = [1, 2, 3, 4, 5]  # 建立一個列表
print(f"建立的列表: {numbers}")

# 正常的存取
print(f"正常存取 numbers[0] = {numbers[0]}")
print(f"正常存取 numbers[4] = {numbers[4]}")

# 嘗試存取超出範圍 - Python 會阻止！
print("\n嘗試存取超出範圍的索引...")
try:
    print(f"numbers[100] = {numbers[100]}")
except IndexError as e:
    print(f"💡 錯誤被阻止了！Python 自動檢查邊界")
    print(f"   錯誤訊息：list index out of range")
    print(f"   這保護了你避免記憶體問題！")

print()

# ═══════════════════════════════════════════
# 範例 2：自動記憶體管理
# ═══════════════════════════════════════════
print("【範例 2】自動記憶體管理")
print("-" * 40)

def create_list():
    """建立一個列表，自動管理記憶體"""
    data = [1, 2, 3, 4, 5]
    print(f"   在函數內建立列表: {data}")
    print(f"   函數即將結束，記憶體將被自動清理")
    return data

result = create_list()
print(f"   在函數外使用結果: {result}")
print("💡 函數結束後，列表會被自動清理！不用擔心記憶體泄漏！")

print()

# ═══════════════════════════════════════════
# 範例 3：垃圾回收
# ═══════════════════════════════════════════
print("【範例 3】垃圾回收機制")
print("-" * 40)

import gc  # 垃圾回收模組

print(f"   垃圾回收器狀態: {'啟用' if gc.isenabled() else '停用'}")

# 創建很多物件
objects_before = len(gc.get_objects())
print(f"   創建物件前數量: {objects_before}")

# 創建一些臨時物件
temp_list = [i for i in range(1000)]
temp_dict = {i: str(i) for i in range(100)}

objects_after = len(gc.get_objects())
print(f"   創建物件後數量: {objects_after}")

# 刪除引用
del temp_list
del temp_dict

# 強制垃圾回收
collected = gc.collect()
print(f"   垃圾回收了 {collected} 個物件")

objects_final = len(gc.get_objects())
print(f"   回收後物件數量: {objects_final}")
print("💡 Python 會自動清理不再使用的記憶體！")

print()

# ═══════════════════════════════════════════
# 範例 4：安全的記憶體操作
# ═══════════════════════════════════════════
print("【範例 4】安全的記憶體操作")
print("-" * 40)

# 安全的列表操作
data = [10, 20, 30, 40, 50]

# 安全的添加
data.append(60)
print(f"   添加元素: {data}")

# 安全的刪除
data.remove(60)
print(f"   刪除元素: {data}")

# 安全的切片
subset = data[1:4]
print(f"   安全切片: {subset}")

# 安全的遍歷
print("   安全遍歷:")
for i, value in enumerate(data):
    print(f"      data[{i}] = {value}")

print("💡 Python 確保所有操作都在安全範圍內！")

print()

# ═══════════════════════════════════════════
# 範例 5：None 檢查
# ═══════════════════════════════════════════
print("【範例 5】None 值的處理")
print("-" * 40)

data = None

# 嘗試對 None 操作會被阻止
print(f"   data = {data}")
print("   嘗試 data + 1...")

try:
    result = data + 1
except TypeError as e:
    print(f"   💡 錯誤被阻止！Python 保護了你！")
    print(f"   錯誤類型: TypeError")
    print(f"   這防止了空指標解引用的問題！")

print()

# ═══════════════════════════════════════════
# 範例 6：類型檢查
# ═══════════════════════════════════════════
print("【範例 6】類型安全")
print("-" * 40)

# Python 會阻止類型錯誤
num = 10
text = "hello"

print(f"   num = {num} (int)")
print(f"   text = {text} (string)")

print("   嘗試 num + text...")

try:
    result = num + text
except TypeError as e:
    print(f"   💡 類型錯誤被阻止！")
    print(f"   Python 確保型別相容！")

print("💡 強型別檢查防止了許多記憶體問題！")

print()
print("=" * 60)
print("💡 結論：Python 自動保護記憶體安全！")
print("   - 邊界檢查")
print("   - 自動記憶體管理")
print("   - 垃圾回收")
print("   - 型別檢查")
print("=" * 60)