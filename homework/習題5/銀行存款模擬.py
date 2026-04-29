#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
銀行存款模擬程式

功能：模擬同一帳戶的存提款操作
說明：同一個人執行 100000 次存款和 100000 次提款
      每次存款和提款金額為 100 元
      由於次數相同，最終存款金額應該與初始金額相同

執行：python3 銀行存款模擬.py
"""

import threading
import time

# 帳戶餘額
balance = 0

# 建立互斥鎖
lock = threading.Lock()

# 執行緒數量
NUM_THREADS = 4
DEPOSIT_COUNT = 100000  # 每個執行緒存款次數
WITHDRAW_COUNT = 100000 # 每個執行緒提款次數
AMOUNT = 100            # 每次存提金額


def deposit(thread_id):
    """存款執行緒"""
    global balance
    
    for i in range(DEPOSIT_COUNT):
        with lock:  # 使用上下文管理器自動加鎖/解鎖
            balance += AMOUNT
    
    print(f"執行緒 {thread_id} 完成存款 {DEPOSIT_COUNT} 次")


def withdraw(thread_id):
    """提款執行緒"""
    global balance
    
    for i in range(WITHDRAW_COUNT):
        with lock:
            if balance >= AMOUNT:
                balance -= AMOUNT
            else:
                print(f"警告：執行緒 {thread_id} 提款失敗，餘額不足！")
    
    print(f"執行緒 {thread_id} 完成提款 {WITHDRAW_COUNT} 次")


def main():
    global balance
    
    threads = []
    
    print("=======================================")
    print("       銀行存款模擬程式")
    print("=======================================")
    print(f"初始存款：{balance} 元")
    print(f"執行緒數量：{NUM_THREADS}")
    print(f"每執行緒存款次數：{DEPOSIT_COUNT}")
    print(f"每執行緒提款次數：{WITHDRAW_COUNT}")
    print(f"每次金額：{AMOUNT} 元")
    print("=======================================\n")
    
    # 記錄開始時間
    start_time = time.time()
    
    # 建立存款執行緒
    for i in range(NUM_THREADS):
        t = threading.Thread(target=deposit, args=(i + 1,))
        threads.append(t)
    
    # 建立提款執行緒
    for i in range(NUM_THREADS):
        t = threading.Thread(target=withdraw, args=(i + 1,))
        threads.append(t)
    
    # 啟動所有執行緒
    for t in threads:
        t.start()
    
    # 等待所有執行緒完成
    for t in threads:
        t.join()
    
    # 記錄結束時間
    end_time = time.time()
    elapsed = end_time - start_time
    
    # 計算預期結果
    total_deposits = NUM_THREADS * DEPOSIT_COUNT * AMOUNT
    total_withdrawals = NUM_THREADS * WITHDRAW_COUNT * AMOUNT
    expected_balance = total_deposits - total_withdrawals
    
    print("\n=======================================")
    print("           結果統計")
    print("=======================================")
    print(f"總存款次數：{NUM_THREADS * DEPOSIT_COUNT} 次")
    print(f"總提款次數：{NUM_THREADS * WITHDRAW_COUNT} 次")
    print(f"總存款金額：{total_deposits} 元")
    print(f"總提款金額：{total_withdrawals} 元")
    print("=======================================\n")
    
    print(f"預期最終餘額：{expected_balance} 元")
    print(f"實際最終餘額：{balance} 元")
    print(f"執行耗時：{elapsed:.3f} 秒")
    print("=======================================\n")
    
    # 驗證結果
    if balance == expected_balance:
        print("✓ 測試通過！存款與提款金額正確，餘額無誤。")
    else:
        print("✗ 測試失敗！餘額不正確，可能存在競爭條件事。")


if __name__ == "__main__":
    main()