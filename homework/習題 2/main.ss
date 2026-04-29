// SimpleScript 範例：主程式
// 展示模組匯入功能

import "utils.ss";

print("SimpleScript 模組系統測試");
print("=========================");

// 使用模組中的函數
let result: int = utils.add(10, 20);
print("10 + 20 = " + str(result));

result = utils.multiply(6, 7);
print("6 * 7 = " + str(result));

result = utils.max(15, 8);
print("max(15, 8) = " + str(result));

result = utils.min(15, 8);
print("min(15, 8) = " + str(result));

let is_even: bool = utils.isEven(42);
print("isEven(42) = " + str(is_even));

result = utils.abs(-100);
print("abs(-100) = " + str(result));

print("");
print("常數:");
print("PI = " + str(utils.PI));
print("E = " + str(utils.E));