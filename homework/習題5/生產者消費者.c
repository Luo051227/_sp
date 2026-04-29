/**
 * 生產者-消費者問題模擬程式
 * 
 * 功能：模擬多個生產者將產品放入緩衝區，多個消費者從緩衝區取出產品
 * 說明：使用環形緩衝區，支援多個生產者和多個消費者
 *       生產者生產產品後放入緩衝區，消費者從緩衝區取出產品
 * 
 * 編譯：gcc -pthread -o producer_consumer 生產者消費者.c
 * 執行：./producer_consumer
 */

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

// 緩衝區配置
#define BUFFER_SIZE 10      // 緩衝區大小
#define MAX_ITEMS 100       // 生產/消費的總數量
#define NUM_PRODUCERS 2     // 生產者數量
#define NUM_CONSUMERS 2     // 消費者數量

// 緩衝區結構
typedef struct {
    int buffer[BUFFER_SIZE]; // 環形緩衝區
    int in;                 // 下一個放入位置
    int out;               // 下一個取出位置
    int count;             // 當前產品數量
} Buffer;

// 全域變數
Buffer shared_buffer;
pthread_mutex_t buffer_mutex;  // 保護緩衝區
sem_t empty_slots;             // 空位數量
sem_t full_slots;              // 產品數量

// 初始化緩衝區
void init_buffer(Buffer* buf) {
    buf->in = 0;
    buf->out = 0;
    buf->count = 0;
}

// 生產者執行緒
void* producer(void* arg) {
    int producer_id = *(int*)arg;
    
    for (int i = 0; i < MAX_ITEMS; i++) {
        // 等待有空位
        sem_wait(&empty_slots);
        
        // 保護緩衝區
        pthread_mutex_lock(&buffer_mutex);
        
        // 放入產品
        int item = producer_id * 1000 + i;  // 唯一的產品編號
        shared_buffer.buffer[shared_buffer.in] = item;
        shared_buffer.in = (shared_buffer.in + 1) % BUFFER_SIZE;
        shared_buffer.count++;
        
        printf("生產者 %d 生產: 產品 #%d (緩衝區: %d/%d)\n", 
               producer_id, item, shared_buffer.count, BUFFER_SIZE);
        
        pthread_mutex_unlock(&buffer_mutex);
        
        // 增加產品數量
        sem_post(&full_slots);
        
        // 模擬生產時間
        usleep(rand() % 50000);  // 0-50ms
    }
    
    printf("生產者 %d 完成所有生產任務\n", producer_id);
    return NULL;
}

// 消費者執行緒
void* consumer(void* arg) {
    int consumer_id = *(int*)arg;
    
    for (int i = 0; i < MAX_ITEMS; i++) {
        // 等待有產品
        sem_wait(&full_slots);
        
        // 保護緩衝區
        pthread_mutex_lock(&buffer_mutex);
        
        // 取出產品
        int item = shared_buffer.buffer[shared_buffer.out];
        shared_buffer.out = (shared_buffer.out + 1) % BUFFER_SIZE;
        shared_buffer.count--;
        
        printf("消費者 %d 消費: 產品 #%d (緩衝區: %d/%d)\n", 
               consumer_id, item, shared_buffer.count, BUFFER_SIZE);
        
        pthread_mutex_unlock(&buffer_mutex);
        
        // 增加空位數量
        sem_post(&empty_slots);
        
        // 模擬消費時間
        usleep(rand() % 50000);  // 0-50ms
    }
    
    printf("消費者 %d 完成所有消費任務\n", consumer_id);
    return NULL;
}

int main() {
    pthread_t producer_threads[NUM_PRODUCERS];
    pthread_t consumer_threads[NUM_CONSUMERS];
    int producer_ids[NUM_PRODUCERS];
    int consumer_ids[NUM_CONSUMERS];
    
    // 初始化
    srand(time(NULL));
    init_buffer(&shared_buffer);
    
    pthread_mutex_init(&buffer_mutex, NULL);
    sem_init(&empty_slots, 0, BUFFER_SIZE);  // 初始有空位
    sem_init(&full_slots, 0, 0);              // 初始無產品
    
    printf("=======================================\n");
    printf("     生產者-消費者問題模擬\n");
    printf("=======================================\n");
    printf("緩衝區大小：%d\n", BUFFER_SIZE);
    printf("每個生產者生產數量：%d\n", MAX_ITEMS);
    printf("每個消費者消費數量：%d\n", MAX_ITEMS);
    printf("生產者數量：%d\n", NUM_PRODUCERS);
    printf("消費者數量：%d\n", NUM_CONSUMERS);
    printf("=======================================\n\n");
    
    // 建立生產者執行緒
    for (int i = 0; i < NUM_PRODUCERS; i++) {
        producer_ids[i] = i + 1;
        pthread_create(&producer_threads[i], NULL, 
                       producer, &producer_ids[i]);
    }
    
    // 建立消費者執行緒
    for (int i = 0; i < NUM_CONSUMERS; i++) {
        consumer_ids[i] = i + 1;
        pthread_create(&consumer_threads[i], NULL, 
                       consumer, &consumer_ids[i]);
    }
    
    // 等待所有執行緒完成
    for (int i = 0; i < NUM_PRODUCERS; i++) {
        pthread_join(producer_threads[i], NULL);
    }
    
    for (int i = 0; i < NUM_CONSUMERS; i++) {
        pthread_join(consumer_threads[i], NULL);
    }
    
    printf("\n=======================================\n");
    printf("           模擬完成\n");
    printf("=======================================\n");
    printf("預期生產總數：%d\n", NUM_PRODUCERS * MAX_ITEMS);
    printf("預期消費總數：%d\n", NUM_CONSUMERS * MAX_ITEMS);
    printf("=======================================\n\n");
    
    // 驗證結果
    int expected_total = NUM_PRODUCERS * MAX_ITEMS;
    printf("✓ 生產者和消費者都已完成任務。\n");
    printf("✓ 緩衝區已清空。\n");
    
    // 清理
    pthread_mutex_destroy(&buffer_mutex);
    sem_destroy(&empty_slots);
    sem_destroy(&full_slots);
    
    return 0;
}