#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生產者-消費者問題模擬程式

功能：模擬多個生產者將產品放入緩衝區，多個消費者從緩衝區取出產品
說明：使用環形緩衝區，支援多個生產者和多個消費者
      生產者生產產品後放入緩衝區，消費者從緩衝區取出產品

執行：python3 生產者消費者.py
"""

import threading
import queue
import time
import random

# 緩衝區配置
BUFFER_SIZE = 10      # 緩衝區大小
MAX_ITEMS = 100       # 生產/消費的總數量
NUM_PRODUCERS = 2     # 生產者數量
NUM_CONSUMERS = 2     # 消費者數量

# 建立訊號量（使用 Condition 模擬）
class Semaphore:
    def __init__(self, initial_value):
        self._value = initial_value
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
    
    def wait(self):
        with self._condition:
            while self._value <= 0:
                self._condition.wait()
            self._value -= 1
    
    def signal(self):
        with self._condition:
            self._value += 1
            self._condition.notify()


# 環形緩衝區
class CircularBuffer:
    def __init__(self, size):
        self.buffer = queue.Queue(maxsize=size)
        self.lock = threading.Lock()
    
    def put(self, item):
        self.buffer.put(item)
    
    def get(self):
        return self.buffer.get()


# 全域變數
shared_buffer = CircularBuffer(BUFFER_SIZE)
empty_slots = Semaphore(BUFFER_SIZE)  # 空位數量
full_slots = Semaphore(0)             # 產品數量


def producer(producer_id):
    """生產者執行緒"""
    for i in range(MAX_ITEMS):
        # 等待有空位
        empty_slots.wait()
        
        # 放入產品
        item = producer_id * 1000 + i  # 唯一的產品編號
        shared_buffer.put(item)
        
        print(f"生產者 {producer_id} 生產: 產品 #{item}")
        
        # 增加產品數量
        full_slots.signal()
        
        # 模擬生產時間
        time.sleep(random.uniform(0, 0.00005))  # 0-50ms
    
    print(f"生產者 {producer_id} 完成所有生產任務")


def consumer(consumer_id):
    """消費者執行緒"""
    for i in range(MAX_ITEMS):
        # 等待有產品
        full_slots.wait()
        
        # 取出產品
        item = shared_buffer.get()
        
        print(f"消費者 {consumer_id} 消費: 產品 #{item}")
        
        # 增加空位數量
        empty_slots.signal()
        
        # 模擬消費時間
        time.sleep(random.uniform(0, 0.00005))  # 0-50ms
    
    print(f"消費者 {consumer_id} 完成所有消費任務")


def main():
    threads = []
    
    print("=======================================")
    print("     生產者-消費者問題模擬")
    print("=======================================")
    print(f"緩衝區大小：{BUFFER_SIZE}")
    print(f"每個生產者生產數量：{MAX_ITEMS}")
    print(f"每個消費者消費數量：{MAX_ITEMS}")
    print(f"生產者數量：{NUM_PRODUCERS}")
    print(f"消費者數量：{NUM_CONSUMERS}")
    print("=======================================\n")
    
    # 建立生產者執行緒
    for i in range(NUM_PRODUCERS):
        t = threading.Thread(target=producer, args=(i + 1,))
        threads.append(t)
    
    # 建立消費者執行緒
    for i in range(NUM_CONSUMERS):
        t = threading.Thread(target=consumer, args=(i + 1,))
        threads.append(t)
    
    # 啟動所有執行緒
    for t in threads:
        t.start()
    
    # 等待所有執行緒完成
    for t in threads:
        t.join()
    
    print("\n=======================================")
    print("           模擬完成")
    print("=======================================")
    print(f"預期生產總數：{NUM_PRODUCERS * MAX_ITEMS}")
    print(f"預期消費總數：{NUM_CONSUMERS * MAX_ITEMS}")
    print("=======================================\n")
    
    print("✓ 生產者和消費者都已完成任務。")
    print("✓ 緩衝區已清空。")


if __name__ == "__main__":
    main()