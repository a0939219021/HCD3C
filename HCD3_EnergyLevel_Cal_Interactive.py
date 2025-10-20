#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNS 3910 温热型饮水机能源效率计算器 - 交互式版本
"""

from HCD3_EnergyLevel_Cal_Core import HotWarmDispenserInput, evaluate, print_report

def get_float_input(prompt: str, min_val: float = None, max_val: float = None) -> float:
    """
    获取浮点数输入，带验证
    """
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f"  ⚠ 输入值不能小于 {min_val}，请重新输入")
                continue
            if max_val is not None and value > max_val:
                print(f"  ⚠ 输入值不能大于 {max_val}，请重新输入")
                continue
            return value
        except ValueError:
            print("  ⚠ 输入格式错误，请输入有效的数字")
        except KeyboardInterrupt:
            print("\n\n程序已取消")
            exit(0)

def main():
    print("=" * 70)
    print("CNS 3910 溫熱型飲水機能源效率計算器")
    print("=" * 70)
    print("\n請輸入測試數據：\n")
    
    # 输入数据
    E24 = get_float_input("1. 24小時備用損失 E24 (kWh): ", min_val=0)
    T_hot = get_float_input("2. 熱水系統24h平均水溫 (°C): ", min_val=0, max_val=100)
    T_amb = get_float_input("3. 周圍溫度 (°C): ", min_val=0, max_val=50)
    V = get_float_input("4. 熱貯水桶標示容量 (L): ", min_val=0)
    
    # 验证温度关系
    if T_hot <= T_amb:
        print("\n⚠ 警告：热水温度应高于周围温度")
        response = input("是否继续计算？(y/n): ")
        if response.lower() != 'y':
            print("程序已取消")
            return
    
    # 创建输入对象
    input_data = HotWarmDispenserInput(
        E24_kWh=E24,
        T_hot24_C=T_hot,
        T_amb_C=T_amb,
        V_marked_L=V
    )
    
    # 执行计算
    result = evaluate(input_data)
    
    # 显示结果
    print("\n")
    print_report(input_data, result)
    
    # 询问是否继续
    print("\n")
    response = input("是否繼續測試其他數據？(y/n): ")
    if response.lower() == 'y':
        print("\n" * 2)
        main()
    else:
        print("\n感謝使用！")

def batch_test():
    """
    批量测试模式 - 测试多个不同容量的标准值
    """
    print("=" * 70)
    print("批量測試模式 - 不同容量的能效分級門檻")
    print("=" * 70)
    
    test_volumes = [1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 10.0]
    
    print("\n容量 (L) | 1級     | 2級     | 3級     | 4級     | 5級/MEPS")
    print("-" * 70)
    
    from HCD3_EnergyLevel_Cal_Core import grade_thresholds_kWh
    
    for V in test_volumes:
        limits = grade_thresholds_kWh(V)
        print(f"{V:8.1f} | {limits[1]:.3f}  | {limits[2]:.3f}  | "
              f"{limits[3]:.3f}  | {limits[4]:.3f}  | {limits[5]:.3f}")
    
    print("=" * 70)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        batch_test()
    else:
        try:
            main()
        except KeyboardInterrupt:
            print("\n\n程序已取消")

