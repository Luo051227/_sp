// SimpleScript 範例：工具模組
// 定義一些常用的函數

let PI: float = 3.14159;
let E: float = 2.71828;

fn add(a: int, b: int) -> int {
    return a + b;
}

fn multiply(a: int, b: int) -> int {
    return a * b;
}

fn max(a: int, b: int) -> int {
    if a > b {
        return a;
    }
    return b;
}

fn min(a: int, b: int) -> int {
    if a < b {
        return a;
    }
    return b;
}

fn isEven(n: int) -> bool {
    return n % 2 == 0;
}

fn abs(n: int) -> int {
    if n < 0 {
        return -n;
    }
    return n;
}