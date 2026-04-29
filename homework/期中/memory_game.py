#!/usr/bin/env python3
"""
記憶體管理模擬遊戲
說明：互動式體驗記憶體管理概念
執行：python3 memory_game.py
"""

print("=" * 60)
print("       🎮 記憶體管理模擬遊戲 🎮")
print("=" * 60)

print("""
╔══════════════════════════════════════════════════════════╗
║  遊戲說明：                                              ║
║  你是一個記憶體管理員，需要正確管理記憶體！              ║
║  用 Python 來體驗！                                      ║
╚══════════════════════════════════════════════════════════╝
""")

print("\n【關卡 1】分配記憶體")
print("-" * 40)
print("   想象記憶體是一個大倉庫...")
print("   我們需要申請空間來存放資料")

# 模擬分配記憶體
memory_blocks = []
memory_used = 0
memory_limit = 1000

def allocate(size):
    """分配記憶體"""
    global memory_used
    
    if memory_used + size > memory_limit:
        print(f"   ❌ 記憶體不足！無法分配 {size} 位元組")
        return None
    
    block = f"block_{len(memory_blocks)}_{size}B"
    memory_blocks.append({
        'name': block,
        'size': size,
        'data': 'allocated'
    })
    memory_used += size
    print(f"   ✓ 分配 {size} 位元組: {block}")
    print(f"   📊 記憶體使用: {memory_used}/{memory_limit} ({memory_used*100//memory_limit}%)")
    return block

# 分配記憶體
b1 = allocate(100)
b2 = allocate(200)
b3 = allocate(50)

print(f"\n   總共分配了 {len(memory_blocks)} 塊記憶體")
print(f"   記憶體使用中：{memory_used} 位元組")

print("\n【關卡 2】使用記憶體")
print("-" * 40)

def use_memory(block_name):
    """使用記憶體"""
    for block in memory_blocks:
        if block['name'] == block_name:
            print(f"   ✓ 使用 {block_name} - 資料讀取中...")
            print(f"      資料內容: {block['data']}")
            return True
    
    print(f"   ❌ {block_name} 不存在或已經釋放！")
    return False

use_memory(b1)
use_memory(b2)

print("\n【關卡 3】釋放記憶體")
print("-" * 40)

def deallocate(block_name):
    """釋放記憶體"""
    global memory_used
    
    for i, block in enumerate(memory_blocks):
        if block['name'] == block_name:
            memory_blocks.pop(i)
            memory_used -= block['size']
            print(f"   ✓ 釋放 {block_name} - 記憶體歸還系統")
            print(f"   📊 記憶體使用: {memory_used}/{memory_limit} ({memory_used*100//memory_limit}%)")
            return True
    
    print(f"   ⚠️  {block_name} 已經被釋放過了！")
    return False

deallocate(b1)
deallocate(b2)
deallocate(b3)

print(f"\n   剩餘記憶體：{memory_used} 位元組")

print("\n【關卡 4】錯誤處理挑戰")
print("-" * 40)

# 重新分配
b4 = allocate(150)
b5 = allocate(150)

# 嘗試使用已釋放的記憶體
print("\n   嘗試使用已經釋放的記憶體...")
result = use_memory(b1)  # 會失敗！

if not result:
    print("   💡 這個錯誤被正確處理了！")
    print("   在 Python 中，這種錯誤會被自動阻止！")

# 嘗試使用不存在的記憶體
print("\n   嘗試使用不存在的記憶體...")
result = use_memory("block_999")

if not result:
    print("   💡 這種錯誤也會被阻止！")

print("\n【關卡 5】模擬記憶體泄漏")
print("-" * 40)

print("""
   想象你忘記釋放記憶體：

   ┌─────────────────────────────┐
   │  申請記憶體 (malloc)        │
   └─────────────────────────────┘
            ↓
   ┌─────────────────────────────┐
   │  使用記憶體                  │
   └─────────────────────────────┘
            ↓
   ┌─────────────────────────────┐
   │  忘記釋放！ 💧              │
   └─────────────────────────────┘
            ↓
   記憶體越來越少... 💀
""")

print("   Python 避免這個問題：")
print("   ✓ 自動垃圾回收")
print("   ✓ 當物件不再被引用時自動釋放")

# 展示 Python 自動化
print("\n   Python 物件生命周期演示：")

class MemoryDemo:
    def __init__(self, name):
        self.name = name
        print(f"   → 建立物件: {name}")
    
    def use(self):
        print(f"   → 使用中: {self.name}")
    
    def __del__(self):
        print(f"   → 刪除物件: {self.name} (記憶體自動釋放)")

obj1 = MemoryDemo("測試1")
obj1.use()
del obj1  # 手動刪除

obj2 = MemoryDemo("測試2")
obj2.use()

print("   函數結束，物件自動被清理！")

def auto_cleanup():
    obj = MemoryDemo("自動清理")
    obj.use()
    # 函數結束，obj 自動被清理

auto_cleanup()

print("\n💡 這個遊戲展示了記憶體管理的基本概念！")
print("   Python 會自動幫你做這些事！")

print("\n" + "=" * 60)
print("【彩蛋】Python 的強大之處")
print("=" * 60)

print("""
   Python 記憶體安全檢查：

   1. 邊界檢查
      arr = [1,2,3]
      arr[100]  → IndexError

   2. 型別檢查
      10 + "hello" → TypeError

   3. None 檢查
      None + 1 → TypeError

   4. 除零檢查
      1 / 0 → ZeroDivisionError

   5. 自動記憶體管理
      不用擔心泄漏！
""")

print("\n" + "=" * 60)
print("🎉 恭喜完成記憶體管理模擬遊戲！")
print("💡 記住：Python 會自動處理這些問題！")
print("=" * 60)