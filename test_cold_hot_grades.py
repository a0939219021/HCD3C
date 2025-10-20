#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试冰温热型分级功能
"""

from HCD3_EnergyLevel_Cal_Core import ColdHotDispenserInput, evaluate_cold_hot

def test_cold_hot_grades():
    print("=" * 60)
    print("冰温热型饮水供应机分级测试")
    print("=" * 60)
    
    # 测试案例1：应该得到3级
    test1 = ColdHotDispenserInput(
        E24_kWh=0.400,   # 较低的能耗
        T_hot_C=88.0,
        T_cold_C=8.0,
        T_amb_C=25.0,
        V_hot_L=2.5,
        V_cold_L=3.0
    )
    
    result1 = evaluate_cold_hot(test1)
    print("\n测试案例1（预期3级）：")
    print(f"Veq = {result1['Veq_L']:.3f} L")
    print(f"E24 = {result1['E24_kWh']:.3f} kWh")
    print(f"容许基准 = {result1['E_standard_kWh']:.3f} kWh")
    print(f"等级 = {result1['grade']}")
    print("各等级门槛:")
    for grade in [1,2,3,4,5]:
        threshold = result1['limits_kWh'][grade]
        status = '✓' if result1['E24_kWh'] <= threshold else '✗'
        print(f"  {grade}级: E24 ≤ {threshold:.3f} kWh {status}")
    
    # 测试案例2：应该得到1级
    test2 = ColdHotDispenserInput(
        E24_kWh=0.200,   # 很低的能耗
        T_hot_C=88.0,
        T_cold_C=8.0,
        T_amb_C=25.0,
        V_hot_L=2.5,
        V_cold_L=3.0
    )
    
    result2 = evaluate_cold_hot(test2)
    print("\n测试案例2（预期1级）：")
    print(f"Veq = {result2['Veq_L']:.3f} L")
    print(f"E24 = {result2['E24_kWh']:.3f} kWh")
    print(f"容许基准 = {result2['E_standard_kWh']:.3f} kWh")
    print(f"等级 = {result2['grade']}")
    print("各等级门槛:")
    for grade in [1,2,3,4,5]:
        threshold = result2['limits_kWh'][grade]
        status = '✓' if result2['E24_kWh'] <= threshold else '✗'
        print(f"  {grade}级: E24 ≤ {threshold:.3f} kWh {status}")
    
    # 测试案例3：应该不合格
    test3 = ColdHotDispenserInput(
        E24_kWh=1.000,   # 很高的能耗
        T_hot_C=88.0,
        T_cold_C=8.0,
        T_amb_C=25.0,
        V_hot_L=2.5,
        V_cold_L=3.0
    )
    
    result3 = evaluate_cold_hot(test3)
    print("\n测试案例3（预期不合格）：")
    print(f"Veq = {result3['Veq_L']:.3f} L")
    print(f"E24 = {result3['E24_kWh']:.3f} kWh")
    print(f"容许基准 = {result3['E_standard_kWh']:.3f} kWh")
    print(f"等级 = {result3['grade']}")
    print("各等级门槛:")
    for grade in [1,2,3,4,5]:
        threshold = result3['limits_kWh'][grade]
        status = '✓' if result3['E24_kWh'] <= threshold else '✗'
        print(f"  {grade}级: E24 ≤ {threshold:.3f} kWh {status}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_cold_hot_grades()
