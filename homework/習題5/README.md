# 執行緒、競爭條件事、互斥鎖、死結 - 完全指南

## 目錄

1. [執行緒（Thread）](#1-執行緒thread)
2. [競爭條件事（Race Condition）](#2-競爭條件事race-condition)
3. [互斥鎖（Mutex）](#3-互斥鎖mutex)
4. [死結（Deadlock）](#4-死結deadlock)
5. [範例程式說明](#5-範例程式說明)

---

## 1. 執行緒（Thread）

### 1.1 什麼是執行緒

執行緒是程式中的最小執行單位，是程序內的一個執行流程。在同一個程序內，多個執行緒共享程序的資源，但每個執行緒有自己的執行狀態。

### 1.2 執行緒與程序的比較

| 特性 | 程序（Process） | 執行緒（Thread） |
|------|-----------------|------------------|
| 資源共享 | 獨立位址空間 | 共享程序資源 |
| 創建成本 | 高（需要複製資源） | 低（共享資源） |
| 通訊方式 | IPC複雜 | 直接共享記憶體 |
| 獨立性 | 高 | 低（共享資源） |
| 創建速度 | 慢 | 快 |

### 1.3 多執行緒的優點

1. **提高資源利用率**：可以在等待I/O時執行其他任務
2. **提升執行效率**：利用多核處理器並行執行
3. **簡化程式結構**：某些問題天然適合多執行緒模型
4. **響應性**：保持UI執行緒響應用戶操作

### 1.4 多執行緒的挑戰

1. **同步問題**：需要協調執行緒間的存取
2. **競爭條件事**：共享資源可能產生衝突
3. **死結風險**：不當的鎖順序可能導致死結
4. **除錯困難**：非確定性的執行順序

### 1.5 POSIX執行緒（pthread）

Linux系統使用pthread庫進行多執行緒程式設計：

```c
#include <pthread.h>

// 執行緒函數
void* thread_function(void* arg) {
    int* num = (int*)arg;
    printf("執行緒執行，參數: %d\n", *num);
    return NULL;
}

int main() {
    pthread_t thread;
    int arg = 42;
    
    // 創建執行緒
    pthread_create(&thread, NULL, thread_function, &arg);
    
    // 等待執行緒結束
    pthread_join(thread, NULL);
    
    return 0;
}
```

### 1.6 執行緒的生命週期

```
        ┌─────────┐
        │  建立   │
        └────┬────┘
             │
             ↓
     ┌────────────────┐
     │                │
     ↓                ↓
┌─────────┐     ┌─────────┐
│  就緒   │────→│ 執行中 │
│(Ready)  │     │(Running)│
└────┬────┘     └────┬────┘
     │                │
     │                ↓
     │         ┌─────────────┐
     │         │  阻塞等待   │
     │         │(Blocked)   │
     │         └──────┬──────┘
     │                │
     └────────────────┘
             ↓
        ┌─────────┐
        │  結束   │
        └─────────┘
```

---

## 2. 競爭條件事（Race Condition）

### 2.1 什麼是競爭條件事

競爭條件事發生在多個執行緒同時存取共享資源，且最終結果依賴於執行順序的情況。當多個執行緒對同一個變數進行讀寫操作時，如果沒有適當的同步機制，可能會產生錯誤的結果。

### 2.2 競爭條件事的成因

競爭條件事的根本原因是**操作的非原子性**。一個看似簡單的運算，如「讀取-修改-寫入」，在執行過程中可能被打斷：

```c
// 原始餘額 = 1000
// 執行緒1: 讀取餘額(1000) → 加100 → 寫回(1100)
// 執行緒2: 讀取餘額(1000) → 減200 → 寫回(800)

// 錯誤結果取決於執行順序：
// 如果交錯執行，最終可能變成 800 或 1100
// 但正確結果應該是 900
```

### 2.3 競爭條件事的類型

#### 2.3.1 讀-修改-寫競爭

```c
// 不安全的程式碼
int counter = 0;

void* increment(void* arg) {
    for (int i = 0; i < 10000; i++) {
        counter++;  // 讀取、修改、寫回三個步驟
    }
    return NULL;
}

// 執行兩個執行緒後，counter可能小於20000
```

#### 2.3.2 檢查-然後-操作競爭

```c
// 不安全的雙重檢查鎖
if (instance == NULL) {
    instance = new Singleton();
}

// 兩個執行緒可能同時通過檢查，都創建實例
```

### 2.4 競爭條件事的範例

#### 銀行帳戶問題

```c
typedef struct {
    int balance;
} Account;

void withdraw(Account* acc, int amount) {
    if (acc->balance >= amount) {
        // 可能的問題：在檢查和扣款之間
        // 其他執行緒可能修改餘額
        acc->balance -= amount;
    }
}
```

### 2.5 檢測競爭條件事

1. **程式碼審查**：檢查所有共享資源的存取
2. **工具分析**：使用ThreadSanitizer、Valgrind等工具
3. **壓力測試**：多次執行測試非確定性行為
4. **模型檢查**：形式化驗證

### 2.6 解決競爭條件事的方法

1. **互斥鎖**：保護臨界區
2. **原子操作**：使用atomic變數
3. **執行緒局部儲存**：避免共享
4. **不可變設計**：設計不變的資料結構

---

## 3. 互斥鎖（Mutex）

### 3.1 什麼是互斥鎖

互斥鎖（Mutual Exclusion Lock）是一種同步機制，用於保護共享資源，防止多個執行緒同時訪問臨界區。當一個執行緒獲得互斥鎖時，其他執行緒必須等待直到鎖被釋放。

### 3.2 互斥鎖的基本操作

```c
#include <pthread.h>

pthread_mutex_t mutex;

// 初始化互斥鎖
pthread_mutex_init(&mutex, NULL);

// 加鎖
pthread_mutex_lock(&mutex);
// 臨界區：只能有一個執行緒進入
pthread_mutex_unlock(&mutex);

// 銷毀互斥鎖
pthread_mutex_destroy(&mutex);
```

### 3.3 互斥鎖的類型

#### 3.3.1 普通互斥鎖

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

// 基本使用
pthread_mutex_lock(&mutex);
// 臨界區域
pthread_mutex_unlock(&mutex);
```

#### 3.3.2 遞迴互斥鎖

允許同一執行緒多次鎖定，需要相同次數解鎖：

```c
pthread_mutex_t mutex;
pthread_mutexattr_t attr;

pthread_mutexattr_init(&attr);
pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_RECURSIVE);
pthread_mutex_init(&mutex, &attr);
```

#### 3.3.3 錯誤檢查互斥鎖

幫助檢測死結和錯誤使用：

```c
pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_ERRORCHECK);
```

### 3.4 互斥鎖的實現原理

```
執行緒A                    執行緒B
   │                          │
   ├─ lock() → 獲得鎖         │
   │                          ├─ lock() → 阻塞等待
   │                          │
   │                          │
   ├─ 解鎖 → 釋放鎖           │
   │                          ├─ 獲得鎖 → 進入臨界區
   │                          │
   ├──────────────────────────┤
```

### 3.5 臨界區設計原則

1. **最小化臨界區**：只保護必要的共享資源
2. **避免長時間持有鎖**：減少其他執行緒等待
3. **不要在持鎖時呼叫阻塞函數**：避免死結
4. **一致的鎖順序**：防止死結

### 3.6 其他同步機制

#### 3.6.1 讀寫鎖

```c
pthread_rwlock_t rwlock;

// 讀鎖（多個執行緒可以同時讀）
pthread_rwlock_rdlock(&rwlock);
// 讀操作
pthread_rwlock_unlock(&rwlock);

// 寫鎖（獨占）
pthread_rwlock_wrlock(&rwlock);
// 寫操作
pthread_rwlock_unlock(&rwlock);
```

#### 3.6.2 條件變數

```c
pthread_cond_t cond;
pthread_mutex_t mutex;
int ready = 0;

// 等待條件
pthread_mutex_lock(&mutex);
while (!ready) {
    pthread_cond_wait(&cond, &mutex);
}
pthread_mutex_unlock(&mutex);

// 發送信號
pthread_mutex_lock(&mutex);
ready = 1;
pthread_cond_signal(&cond);
pthread_mutex_unlock(&mutex);
```

#### 3.6.3 訊號量

```c
sem_t sem;
sem_init(&sem, 0, 1);  // 初始值1

// P操作（遞減）
sem_wait(&sem);
// 臨界區
sem_post(&sem);  // V操作（遞增）
```

---

## 4. 死結（Deadlock）

### 4.1 什麼是死結

死結是指兩個或多個執行緒互相等待對方釋放資源，導致所有執行緒都无法繼續執行的狀態。這是多執行緒程式設計中最嚴重的問題之一。

### 4.2 死結的必要條件

Coffman條件是產生死結的四個必要條件：

1. **互斥條件（Mutual Exclusion）**：資源只能被一個執行緒佔用
2. **占有並等待（Hold and Wait）**：執行緒持有資源的同時等待其他資源
3. **不可搶占（No Preemption）**：資源不能被強制搶占，只能自願釋放
4. **循環等待（Circular Wait）**：形成資源等待循環

```
執行緒A: 持有資源1 → 等待資源2
執行緒B: 持有資源2 → 等待資源1

形成循環等待：
執行緒A → 資源2 ← 執行緒B
  ↑              │
  └──────────────┘
```

### 4.3 死結的範例

#### 4.3.1 兩個互斥鎖

```c
// 執行緒1
pthread_mutex_lock(&mutex1);
pthread_mutex_lock(&mutex2);
// 臨界區
pthread_mutex_unlock(&mutex2);
pthread_mutex_unlock(&mutex1);

// 執行緒2（不同的鎖順序）
pthread_mutex_lock(&mutex2);
pthread_mutex_lock(&mutex1);
// 臨界區
pthread_mutex_unlock(&mutex1);
pthread_mutex_unlock(&mutex2);

// 可能發生：執行緒1獲得mutex1，執行緒2獲得mutex2，然後互相等待
```

#### 4.3.2 生產者-消費者問題中的死結

```c
// 如果緩衝區滿且沒有正確的同步
// 生產者等待消費者取出資料
// 消費者等待生產者放入資料
```

### 4.4 預防死結的方法

#### 4.4.1 破壞占有並等待

```c
// 方法1：一次請求所有資源
pthread_mutex_lock(&both_mutex);
// 使用兩個資源
pthread_mutex_unlock(&both_mutex);

// 方法2：釋放已持有的資源再請求新資源
void safe_function() {
    pthread_mutex_lock(&mutex1);
    pthread_mutex_unlock(&mutex1);  // 釋放
    
    // 重新請求
    pthread_mutex_lock(&mutex1);
    pthread_mutex_lock(&mutex2);
}
```

#### 4.4.2 破壞循環等待

```c
// 方法：固定順序請求資源
// 總是先請求mutex1，再請求mutex2

// 執行緒1
pthread_mutex_lock(&mutex1);
pthread_mutex_lock(&mutex2);

// 執行緒2（相同的順序）
pthread_mutex_lock(&mutex1);
pthread_mutex_lock(&mutex2);
```

### 4.5 避免死結的策略

#### 4.5.1 銀行家演算法

在資源分配前檢查是否安全，雖然保守但能避免死結。

#### 4.5.2 鎖超時

```c
// 使用pthread_mutex_timedlock
struct timespec ts;
clock_gettime(CLOCK_REALTIME, &ts);
ts.tv_sec += 1;  // 1秒超時

int result = pthread_mutex_timedlock(&mutex, &ts);
if (result == ETIMEDOUT) {
    // 處理超時，可能需要回退
}
```

### 4.6 檢測和恢復

#### 4.6.1 死結檢測

```c
// 定期檢查執行緒等待圖
// 如果發現環則表示死結
```

#### 4.6.2 恢復策略

1. **強制終止**：殺死一個執行緒
2. **回滾**：讓執行緒釋放所有資源
3. **搶占**：從某個執行緒搶占資源

### 4.7 死結 vs 活結

| 特性 | 死結（Deadlock） | 活結（Livelock） |
|------|------------------|------------------|
| 執行緒狀態 | 阻塞 | 運行但無法前進 |
| CPU使用 | 不消耗 | 消耗但無進展 |
| 原因 | 互相等待 | 不斷重試 |
| 檢測 | 等待圖 | 觀察執行 |

---

## 5. 範例程式說明

### 5.1 銀行存款模擬

**目標**：模擬同一帳戶的存提款操作，驗證執行緒安全性

**關鍵概念**：
- 使用互斥鎖保護共享的帳戶餘額
- 執行100000次存款和100000次提款
- 最終餘額應為初始值（因為存款提款次數相同）

**同步機制**：
- 使用pthread_mutex保護臨界區
- 每次存款/提款前加鎖，完成後解鎖

### 5.2 生產者-消費者問題

**目標**：模擬多個生產者將產品放入緩衝區，多個消費者從緩衝區取出產品

**關鍵概念**：
- 緩衝區大小有限
- 生產者需要等待緩衝區有空位
- 消費者需要等待緩衝區有產品

**同步機制**：
- 訊號量控制緩衝區空位和產品數量
- 互斥鎖保護緩衝區的實際存取
- 防止生產者和消費者同時訪問緩衝區

### 5.3 哲學家用餐問題

**目標**：模擬五位哲學家在圓桌上用餐的經典同步問題

**問題描述**：
- 五位哲學家圍坐在圓桌旁
- 每位哲學家左右各有一支叉子
- 只有拿到兩支叉子才能吃麵
- 吃完後放下叉子讓其他哲學家使用

**挑戰**：
- 可能發生死結（所有哲學家同時拿起左叉）
- 需要避免死結同時保證公平性

**解決方案**：
- 規定奇數號哲學家先拿左邊叉子，偶數號先拿右邊
- 或使用侍者（最多四位哲學家同時就座）
- 使用互斥鎖保護叉子狀態

---

## 結論

多執行緒程式設計帶來了效能提升，但也帶來了同步挑戰。理解競爭條件事、互斥鎖和死結的概念對於編寫正確的多執行緒程式至關重要。通過適當的同步機制和良好的設計模式，我們可以充分利用多核系統的效能，同時避免常見的同步問題。

---

*本文件說明了執行緒程式設計的核心概念，包含競爭條件事、互斥鎖和死結的基本理論與實作。*