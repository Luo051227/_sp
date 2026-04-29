// SimpleScript 範例：費波那契數列
// 展示函數定義和遞迴

fn fib(n: int) -> int {
    if n <= 1 {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

print("費波那契數列前10項:");
for i = 0, 10, 1 {
    print("fib(" + str(i) + ") = " + str(fib(i)));
}

// 迴圈版本
fn fibLoop(n: int) -> int {
    if n <= 1 {
        return n;
    }
    let a: int = 0;
    let b: int = 1;
    let temp: int = 0;
    
    for i = 2, n, 1 {
        temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

print("");
print("迴圈版本:");
for i = 0, 10, 1 {
    print("fib(" + str(i) + ") = " + str(fibLoop(i)));
}