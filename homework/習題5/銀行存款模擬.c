/**
 * 銀行存款模擬程式
 * 
 * 功能：模擬同一帳戶的存提款操作
 * 說明：同一個人執行 100000 次存款和 100000 次提款
 *       每次存款和提款金額為 100 元
 *       由於次數相同，最終存款金額應該與初始金額相同
 * 
 * 編譯：gcc -pthread -o bank 銀行存款模擬.c
 * 執行：./bank
 */

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>

// 帳戶結構
typedef struct {
    int balance;              // 存款餘額
    pthread_mutex_t mutex;   // 互斥鎖保護餘額
} Account;

// 全域帳戶
Account account;

// 執行緒數量
#define NUM_THREADS 4
#define DEPOSIT_COUNT 100000  // 每個執行緒存款次數
#define WITHDRAW_COUNT 100000 // 每個執行緒提款次數
#define AMOUNT 100            // 每次存提金額

// 存款執行緒函數
void* deposit_thread(void* arg) {
    int thread_id = *(int*)arg;
    
    for (int i = 0; i < DEPOSIT_COUNT; i++) {
        pthread_mutex_lock(&account.mutex);
        
        // 臨界區：修改帳戶餘額
        account.balance += AMOUNT;
        
        pthread_mutex_unlock(&account.mutex);
    }
    
    printf("執行緒 %d 完成存款 %d 次\n", thread_id, DEPOSIT_COUNT);
    return NULL;
}

// 提款執行緒函數
void* withdraw_thread(void* arg) {
    int thread_id = *(int*)arg;
    
    for (int i = 0; i < WITHDRAW_COUNT; i++) {
        pthread_mutex_lock(&account.mutex);
        
        // 臨界區：修改帳戶餘額
        // 檢查餘額是否足夠
        if (account.balance >= AMOUNT) {
            account.balance -= AMOUNT;
        } else {
            printf("警告：執行緒 %d 提款失敗，餘額不足！\n", thread_id);
        }
        
        pthread_mutex_unlock(&account.mutex);
    }
    
    printf("執行緒 %d 完成提款 %d 次\n", thread_id, WITHDRAW_COUNT);
    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS * 2];  // 存款和提款執行緒
    int thread_ids[NUM_THREADS * 2];
    
    // 初始化帳戶
    account.balance = 0;
    pthread_mutex_init(&account.mutex, NULL);
    
    printf("=======================================\n");
    printf("       銀行存款模擬程式\n");
    printf("=======================================\n");
    printf("初始存款：%d 元\n", account.balance);
    printf("執行緒數量：%d\n", NUM_THREADS);
    printf("每執行緒存款次數：%d\n", DEPOSIT_COUNT);
    printf("每執行緒提款次數：%d\n", WITHDRAW_COUNT);
    printf("每次金額：%d 元\n", AMOUNT);
    printf("=======================================\n\n");
    
    // 記錄開始時間
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    
    // 建立存款執行緒
    for (int i = 0; i < NUM_THREADS; i++) {
        thread_ids[i] = i + 1;
        pthread_create(&threads[i], NULL, deposit_thread, &thread_ids[i]);
    }
    
    // 建立提款執行緒
    for (int i = 0; i < NUM_THREADS; i++) {
        thread_ids[NUM_THREADS + i] = i + 1;
        pthread_create(&threads[NUM_THREADS + i], NULL, 
                      withdraw_thread, &thread_ids[NUM_THREADS + i]);
    }
    
    // 等待所有執行緒完成
    for (int i = 0; i < NUM_THREADS * 2; i++) {
        pthread_join(threads[i], NULL);
    }
    
    // 記錄結束時間
    clock_gettime(CLOCK_MONOTONIC, &end);
    double elapsed = (end.tv_sec - start.tv_sec) + 
                     (end.tv_nsec - start.tv_nsec) / 1e9;
    
    // 計算預期結果
    int total_deposits = NUM_THREADS * DEPOSIT_COUNT * AMOUNT;
    int total_withdrawals = NUM_THREADS * WITHDRAW_COUNT * AMOUNT;
    int expected_balance = total_deposits - total_withdrawals;
    
    printf("\n=======================================\n");
    printf("           結果統計\n");
    printf("=======================================\n");
    printf("總存款次數：%d 次\n", NUM_THREADS * DEPOSIT_COUNT);
    printf("總提款次數：%d 次\n", NUM_THREADS * WITHDRAW_COUNT);
    printf("總存款金額：%d 元\n", total_deposits);
    printf("總提款金額：%d 元\n", total_withdrawals);
    printf("=======================================\n\n");
    
    printf("預期最終餘額：%d 元\n", expected_balance);
    printf("實際最終餘額：%d 元\n", account.balance);
    printf("執行耗時：%.3f 秒\n", elapsed);
    printf("=======================================\n\n");
    
    // 驗證結果
    if (account.balance == expected_balance) {
        printf("✓ 測試通過！存款與提款金額正確，餘額無誤。\n");
    } else {
        printf("✗ 測試失敗！餘額不正確，可能存在競爭條件事。\n");
    }
    
    // 銷毀互斥鎖
    pthread_mutex_destroy(&account.mutex);
    
    return 0;
}