#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNS 3910 批量测试工具 - 支持 CSV 输入/输出
使用方法：
  1. 准备 input.csv 文件（包含测试数据）
  2. 运行：python cns3910_batch_csv.py
  3. 查看 output.csv（包含计算结果）
"""

import csv
from typing import List, Dict
from HCD3_EnergyLevel_Cal_Core import HotWarmDispenserInput, evaluate

def read_csv(filename: str) -> List[Dict]:
    """
    读取 CSV 文件
    预期格式：
    型号,E24_kWh,T_hot24_C,T_amb_C,V_marked_L
    """
    data = []
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        print(f"❌ 找不到文件：{filename}")
        return []
    except Exception as e:
        print(f"❌ 读取文件时发生错误：{e}")
        return []

def write_csv(filename: str, data: List[Dict]):
    """
    写入 CSV 文件
    """
    if not data:
        print("❌ 没有数据可写入")
        return
    
    fieldnames = list(data[0].keys())
    
    try:
        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"✓ 结果已保存至：{filename}")
    except Exception as e:
        print(f"❌ 写入文件时发生错误：{e}")

def create_sample_input():
    """
    创建示例输入文件
    """
    sample_data = [
        {
            "型号": "型号A",
            "E24_kWh": "1.152",
            "T_hot24_C": "87.0",
            "T_amb_C": "25.0",
            "V_marked_L": "1.4"
        },
        {
            "型号": "型号B",
            "E24_kWh": "0.500",
            "T_hot24_C": "85.0",
            "T_amb_C": "25.0",
            "V_marked_L": "2.0"
        },
        {
            "型号": "型号C",
            "E24_kWh": "0.800",
            "T_hot24_C": "88.0",
            "T_amb_C": "24.0",
            "V_marked_L": "3.0"
        },
    ]
    
    filename = "sample_input.csv"
    write_csv(filename, sample_data)
    print(f"✓ 已创建示例输入文件：{filename}")
    return filename

def process_batch(input_file: str, output_file: str):
    """
    批量处理 CSV 文件
    """
    print("=" * 70)
    print("CNS 3910 批量测试工具")
    print("=" * 70)
    
    # 读取输入
    input_data = read_csv(input_file)
    if not input_data:
        return
    
    print(f"\n✓ 读取到 {len(input_data)} 组测试数据")
    
    # 处理每组数据
    results = []
    for idx, row in enumerate(input_data, 1):
        try:
            # 解析输入
            test_input = HotWarmDispenserInput(
                E24_kWh=float(row['E24_kWh']),
                T_hot24_C=float(row['T_hot24_C']),
                T_amb_C=float(row['T_amb_C']),
                V_marked_L=float(row['V_marked_L'])
            )
            
            # 执行计算
            result = evaluate(test_input)
            
            # 整合结果
            output_row = {
                "序号": idx,
                "型号": row.get('型号', f'测试{idx}'),
                "E24_kWh": row['E24_kWh'],
                "T_hot24_C": row['T_hot24_C'],
                "T_amb_C": row['T_amb_C'],
                "V_marked_L": row['V_marked_L'],
                "温度校正系数_K": f"{result['K']:.6f}",
                "E_st24_kWh": f"{result['E_st24_kWh']:.3f}",
                "MEPS_kWh": f"{result['MEPS_kWh']:.3f}",
                "1级门槛": f"{result['limits_kWh'][1]:.3f}",
                "2级门槛": f"{result['limits_kWh'][2]:.3f}",
                "3级门槛": f"{result['limits_kWh'][3]:.3f}",
                "4级门槛": f"{result['limits_kWh'][4]:.3f}",
                "5级门槛": f"{result['limits_kWh'][5]:.3f}",
                "能效等级": result['grade'] if result['grade'] else "不合格",
                "是否通过MEPS": "是" if result['is_meps_pass'] else "否",
            }
            
            results.append(output_row)
            
            # 显示进度
            grade_str = f"{result['grade']}级" if result['grade'] else "❌不合格"
            print(f"  [{idx}/{len(input_data)}] {output_row['型号']}: "
                  f"E_st,24={result['E_st24_kWh']:.3f} kWh → {grade_str}")
            
        except KeyError as e:
            print(f"  ❌ 第 {idx} 行数据格式错误：缺少字段 {e}")
        except ValueError as e:
            print(f"  ❌ 第 {idx} 行数据格式错误：{e}")
        except Exception as e:
            print(f"  ❌ 第 {idx} 行处理失败：{e}")
    
    # 输出结果
    if results:
        write_csv(output_file, results)
        
        # 统计摘要
        print("\n" + "=" * 70)
        print("统计摘要")
        print("=" * 70)
        
        total = len(results)
        passed = sum(1 for r in results if r['是否通过MEPS'] == "是")
        
        print(f"  总测试数：{total}")
        print(f"  通过 MEPS：{passed} ({passed/total*100:.1f}%)")
        print(f"  未通过：{total - passed} ({(total-passed)/total*100:.1f}%)")
        
        # 按等级统计
        print("\n  等级分布：")
        for grade in [1, 2, 3, 4, 5]:
            count = sum(1 for r in results if r['能效等级'] == grade)
            if count > 0:
                print(f"    {grade}级: {count} ({count/total*100:.1f}%)")
        
        failed = sum(1 for r in results if r['能效等级'] == "不合格")
        if failed > 0:
            print(f"    不合格: {failed} ({failed/total*100:.1f}%)")
        
        print("=" * 70)

def main():
    import sys
    import os
    
    if len(sys.argv) > 1 and sys.argv[1] == "--sample":
        # 创建示例文件
        create_sample_input()
        return
    
    # 检查输入文件
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.csv"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.csv"
    
    if not os.path.exists(input_file):
        print(f"❌ 找不到输入文件：{input_file}")
        print("\n使用方法：")
        print("  1. 创建示例文件：python cns3910_batch_csv.py --sample")
        print("  2. 编辑 sample_input.csv 或准备自己的 input.csv")
        print("  3. 运行批量测试：python cns3910_batch_csv.py [input.csv] [output.csv]")
        return
    
    # 执行批量处理
    process_batch(input_file, output_file)

if __name__ == "__main__":
    main()

