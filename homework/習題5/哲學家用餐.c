/**
 * 哲學家用餐問題模擬程式
 * 
 * 功能：模擬五位哲學家在圓桌上用餐的經典同步問題
 * 說明：每位哲學家需要左右兩支叉子才能吃麵
 *       使用不同策略避免死結
 * 
 * 編譯：gcc -pthread -o philosophers 哲學家用餐.c
 * 執行：./philosophers
 */

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

#define NUM_PHILOSOPHERS 5    // 哲學家數量
#define MEALS_TO_EAT 3        // 每位哲學家需要吃的餐數
#define THINKING_TIME 100000  // 思考時間 (微秒)
#define EATING_TIME 100000    // 吃飯時間 (微秒)

// 叉子狀態：0=可用，1=已被佔用
int forks[NUM_PHILOSOPHERS];

// 互斥鎖保護叉子
pthread_mutex_t fork_mutex;

// 策略選擇：0=固定順序，1=奇偶策略
#define STRATEGY 1

// 顯示叉子狀態
void print_forks() {
    printf("叉子狀態: [");
    for (int i = 0; i < NUM_PHILOSOPHERS; i++) {
        printf("%d", forks[i]);
        if (i < NUM_PHILOSOPHERS - 1) printf(", ");
    }
    printf("]\n");
}

// 哲學家執行緒
void* philosopher(void* arg) {
    int id = *(int*)arg;
    int left_fork = id;                      // 左邊叉子
    int right_fork = (id + 1) % NUM_PHILOSOPHERS;  // 右邊叉子
    
    for (int meal = 1; meal <= MEALS_TO_EAT; meal++) {
        printf("哲學家 %d 正在思考... (餐 %d/%d)\n", id, meal, MEALS_TO_EAT);
        usleep(THINKING_TIME + rand() % THINKING_TIME);
        
        // 嘗試拿起叉子
        printf("哲學家 %d 嘗試拿叉子\n", id);
        
        // 使用不同策略拿起叉子
#if STRATEGY == 0
        // 策略0：固定順序（可能死結）
        // 先拿編號較小的叉子
        int first = (left_fork < right_fork) ? left_fork : right_fork;
        int second = (left_fork < right_fork) ? right_fork : left_fork;
        
        pthread_mutex_lock(&fork_mutex);
        while (forks[first]) {
            pthread_mutex_unlock(&fork_mutex);
            usleep(10000);
            pthread_mutex_lock(&fork_mutex);
        }
        forks[first] = 1;
        printf("  哲學家 %d 拿起叉子 %d\n", id, first);
        
        while (forks[second]) {
            pthread_mutex_unlock(&fork_mutex);
            usleep(10000);
            pthread_mutex_lock(&fork_mutex);
        }
        forks[second] = 1;
        printf("  哲學家 %d 拿起叉子 %d\n", id, second);
        pthread_mutex_unlock(&fork_mutex);
        
#else
        // 策略1：奇偶策略（避免死結）
        // 奇數號哲學家先拿左邊，偶數號先拿右邊
        int first, second;
        
        if (id % 2 == 1) {  // 奇數：先左後右
            first = left_fork;
            second = right_fork;
        } else {            // 偶數：先右後左
            first = right_fork;
            second = left_fork;
        }
        
        // 拿起第一支叉子
        pthread_mutex_lock(&fork_mutex);
        while (forks[first]) {
            pthread_mutex_unlock(&fork_mutex);
            usleep(10000);
            pthread_mutex_lock(&fork_mutex);
        }
        forks[first] = 1;
        printf("  哲學家 %d 拿起叉子 %d\n", id, first);
        pthread_mutex_unlock(&fork_mutex);
        
        // 拿起第二支叉子
        pthread_mutex_lock(&fork_mutex);
        while (forks[second]) {
            pthread_mutex_unlock(&fork_mutex);
            usleep(10000);
            pthread_mutex_lock(&fork_mutex);
        }
        forks[second] = 1;
        printf("  哲學家 %d 拿起叉子 %d\n", id, second);
        pthread_mutex_unlock(&fork_mutex);
#endif
        
        // 吃飯
        printf(">>> 哲學家 %d 開始吃飯 (餐 %d/%d) <<<\n", id, meal, MEALS_TO_EAT);
        print_forks();
        usleep(EATING_TIME + rand() % EATING_TIME);
        
        // 放下叉子
        pthread_mutex_lock(&fork_mutex);
        forks[left_fork] = 0;
        forks[right_fork] = 0;
        printf("  哲學家 %d 放下叉子 %d 和 %d\n", id, left_fork, right_fork);
        print_forks();
        pthread_mutex_unlock(&fork_mutex);
    }
    
    printf("★★★ 哲學家 %d 完成所有餐點 ★★★\n", id);
    return NULL;
}

int main() {
    pthread_t philosophers[NUM_PHILOSOPHERS];
    int philosopher_ids[NUM_PHILOSOPHERS];
    
    // 初始化
    srand(time(NULL));
    pthread_mutex_init(&fork_mutex, NULL);
    
    for (int i = 0; i < NUM_PHILOSOPHERS; i++) {
        forks[i] = 0;
    }
    
    printf("=======================================\n");
    printf("     哲學家用餐問題模擬\n");
    printf("=======================================\n");
    printf("哲學家數量：%d\n", NUM_PHILOSOPHERS);
    printf("每位哲學家需吃：%d 餐\n", MEALS_TO_EAT);
#if STRATEGY == 0
    printf("使用策略：固定順序（可能死結）\n");
#else
    printf("使用策略：奇偶策略（避免死結）\n");
#endif
    printf("=======================================\n\n");
    
    print_forks();
    printf("\n");
    
    // 建立哲學家執行緒
    for (int i = 0; i < NUM_PHILOSOPHERS; i++) {
        philosopher_ids[i] = i;
        pthread_create(&philosophers[i], NULL, philosopher, &philosopher_ids[i]);
    }
    
    // 等待所有執行緒完成
    for (int i = 0; i < NUM_PHILOSOPHERS; i++) {
        pthread_join(philosophers[i], NULL);
    }
    
    printf("\n=======================================\n");
    printf("     所有哲學家都已吃完！\n");
    printf("=======================================\n");
    
    // 清理
    pthread_mutex_destroy(&fork_mutex);
    
    return 0;
}