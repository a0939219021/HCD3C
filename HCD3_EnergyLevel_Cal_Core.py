from dataclasses import dataclass
from typing import Literal, Optional, Dict

Grade = Literal[1, 2, 3, 4, 5]

@dataclass
class HotWarmDispenserInput:
    # 量測輸入
    E24_kWh: float          # 24 小時備用損失 E24 (kWh)
    T_hot24_C: float        # 熱水系統 24h 平均水溫 (°C)
    T_amb_C: float          # 周圍溫度 (°C)
    V_marked_L: float       # 熱貯水桶「標示容量」(L) → 依規定計算至小數 1 位

@dataclass
class ColdHotDispenserInput:
    # 冰溫熱型飲水機量測輸入
    E24_kWh: float          # 24 小時備用損失 E24 (kWh)
    T_hot_C: float          # 熱水平均溫度 Th (°C)
    T_cold_C: float         # 冰水平均溫度 Tc (°C)
    T_amb_C: float          # 周圍溫度 (°C)
    V_hot_L: float          # 熱水貯水桶容量標示值 V1 (L)
    V_cold_L: float         # 冰水貯水桶容量標示值 V2 (L)

# --- 公式（依 CNS3910 與附表）---

def temp_correction_factor(T_hot24_C: float, T_amb_C: float) -> float:
    """
    溫度校正係數 K = (T - 周圍溫度) / (100 - 周圍溫度)
    """
    return (T_hot24_C - T_amb_C) / (100.0 - T_amb_C)

def est24(E24_kWh: float, T_hot24_C: float, T_amb_C: float, rounding: int = 3) -> float:
    """
    標準化每 24 小時備用損失 E_st,24 = E24 / K
    依規定：E_st,24 實測值計算至小數第 3 位（第 4 位四捨五入）。
    """
    K = temp_correction_factor(T_hot24_C, T_amb_C)
    return round(E24_kWh / K, rounding)

def meps_limit_kWh(V_marked_L: float) -> float:
    """
    容許耗用能源基準（附表一）：
    MEPS = 0.053 × V + 0.750  (kWh)
    V 為熱水系統貯水桶「標示容量」，計算至小數第 1 位（第 2 位四捨五入）
    """
    V = round(V_marked_L, 1)
    return 0.053 * V + 0.750

def grade_thresholds_kWh(V_marked_L: float) -> Dict[Grade, float]:
    """
    能源效率分級（附表五）之上限線（含）：
      1級: E_st,24 ≤ 0.032×V + 0.450
      2級: E_st,24 ≤ 0.037×V + 0.525
      3級: E_st,24 ≤ 0.042×V + 0.600
      4級: E_st,24 ≤ 0.048×V + 0.675
      5級: E_st,24 ≤ 0.053×V + 0.750  (同 MEPS)
    """
    V = round(V_marked_L, 1)
    return {
        1: 0.032 * V + 0.450,
        2: 0.037 * V + 0.525,
        3: 0.042 * V + 0.600,
        4: 0.048 * V + 0.675,
        5: 0.053 * V + 0.750,  # 亦為 MEPS
    }

def classify_grade(est24_kWh: float, V_marked_L: float) -> Optional[Grade]:
    """
    根據 E_st,24 與分級門檻回傳 1–5 級；
    若 E_st,24 大於 5 級上限（亦即超過 MEPS），回傳 None 表示「不合格」。
    """
    limits = grade_thresholds_kWh(V_marked_L)
    for g in (1, 2, 3, 4, 5):
        if est24_kWh <= limits[g]:
            return g
    return None  # 超過 5 級上限 → 不符合容許基準

# --- 綜合計算 ---

def evaluate(input: HotWarmDispenserInput) -> dict:
    """
    輸入量測值，輸出：
      - K 溫度校正係數
      - E_st,24 (kWh)
      - 各級上限值與 MEPS
      - 等級/是否合格
    """
    K = temp_correction_factor(input.T_hot24_C, input.T_amb_C)
    Est24 = est24(input.E24_kWh, input.T_hot24_C, input.T_amb_C)
    limits = grade_thresholds_kWh(input.V_marked_L)
    meps = meps_limit_kWh(input.V_marked_L)
    g = classify_grade(Est24, input.V_marked_L)
    return {
        "K": round(K, 6),
        "E_st24_kWh": Est24,
        "limits_kWh": limits,
        "MEPS_kWh": meps,
        "grade": g,                # None 代表不合格
        "is_meps_pass": Est24 <= meps
    }

# --- 冰溫熱型飲水機計算函數（節能標章基準） ---

def calc_K1(T_hot_C: float, T_amb_C: float) -> float:
    """
    熱水溫度校正係數 K1 = (Th - 周圍溫度) / (100 - 周圍溫度)
    計算至小數第 3 位
    """
    return round((T_hot_C - T_amb_C) / (100.0 - T_amb_C), 3)

def calc_K2(T_cold_C: float, T_amb_C: float) -> float:
    """
    冰水溫度校正係數 K2 = (周圍溫度 - Tc) / 周圍溫度
    計算至小數第 3 位
    """
    return round((T_amb_C - T_cold_C) / T_amb_C, 3)

def calc_Veq(V_hot_L: float, V_cold_L: float, K1: float, K2: float) -> float:
    """
    等效內容量 Veq = V1 × K1 + (V2 × K2) / 3
    V1, V2 計算至小數第 1 位
    """
    V1 = round(V_hot_L, 1)
    V2 = round(V_cold_L, 1)
    return V1 * K1 + (V2 * K2) / 3

def energy_standard_limit(Veq: float) -> float:
    """
    冰溫熱型飲水供應機容許耗用能源基準
    E24 ≤ 0.081×Veq+0.405
    計算至小數第 3 位
    """
    E = 0.081 * Veq + 0.405
    return round(E, 3)

def cold_hot_grade_thresholds(Veq: float) -> Dict[Grade, float]:
    """
    冰溫熱型飲水供應機能效分級（Veq ≤ 8L）：
      1級: E24 ≤ 0.049×Veq+0.243
      2級: 0.049×Veq+0.243 < E24 ≤ 0.057×Veq+0.284
      3級: 0.057×Veq+0.284 < E24 ≤ 0.065×Veq+0.324
      4級: 0.065×Veq+0.324 < E24 ≤ 0.073×Veq+0.365
      5級: 0.073×Veq+0.365 < E24 ≤ 0.081×Veq+0.405
    """
    return {
        1: 0.049 * Veq + 0.243,
        2: 0.057 * Veq + 0.284,
        3: 0.065 * Veq + 0.324,
        4: 0.073 * Veq + 0.365,
        5: 0.081 * Veq + 0.405,  # 亦為容許基準
    }

def classify_cold_hot_grade(E24_kWh: float, Veq: float) -> Optional[Grade]:
    """
    根據 E24 與冰溫熱型分級門檻回傳 1–5 級；
    若 E24 大於 5 級上限（亦即超過容許基準），回傳 None 表示「不合格」。
    """
    limits = cold_hot_grade_thresholds(Veq)
    for g in (1, 2, 3, 4, 5):
        if E24_kWh <= limits[g]:
            return g
    return None  # 超過 5 級上限 → 不符合容許基準

def evaluate_cold_hot(input: ColdHotDispenserInput) -> dict:
    """
    冰溫熱型飲水供應機評估
    輸入量測值，輸出：
      - K1, K2 溫度校正係數
      - Veq 等效內容量
      - E 容許耗用能源基準
      - 1-5級能效等級
    """
    K1 = calc_K1(input.T_hot_C, input.T_amb_C)
    K2 = calc_K2(input.T_cold_C, input.T_amb_C)
    Veq = calc_Veq(input.V_hot_L, input.V_cold_L, K1, K2)
    E_standard = energy_standard_limit(Veq)
    limits = cold_hot_grade_thresholds(Veq)
    grade = classify_cold_hot_grade(input.E24_kWh, Veq)
    
    # 判定：E24 實測值不得高於容許耗用能源基準
    is_qualified = input.E24_kWh <= E_standard
    
    # 計算餘裕量（越大越好）
    margin_kWh = E_standard - input.E24_kWh
    margin_percent = (margin_kWh / E_standard * 100) if E_standard > 0 else 0
    
    return {
        "K1": K1,
        "K2": K2,
        "V_hot_L": round(input.V_hot_L, 1),
        "V_cold_L": round(input.V_cold_L, 1),
        "Veq_L": round(Veq, 3),
        "E24_kWh": round(input.E24_kWh, 3),
        "E_standard_kWh": E_standard,
        "limits_kWh": limits,
        "grade": grade,
        "is_qualified": is_qualified,
        "margin_kWh": round(margin_kWh, 3),
        "margin_percent": round(margin_percent, 1)
    }

def print_report_cold_hot(input: ColdHotDispenserInput, result: dict):
    """
    輸出冰溫熱型飲水供應機測試報告
    """
    print("=" * 70)
    print("冰溫熱型飲水供應機能效測試報告")
    print("=" * 70)
    print("\n【輸入參數】")
    print(f"  24小時備用損失 E24:        {input.E24_kWh:.3f} kWh")
    print(f"  熱水平均溫度 Th:            {input.T_hot_C:.1f} °C")
    print(f"  冰水平均溫度 Tc:            {input.T_cold_C:.1f} °C")
    print(f"  周圍溫度 T_amb:             {input.T_amb_C:.1f} °C")
    print(f"  熱水貯水桶容量 V1:          {result['V_hot_L']:.1f} L")
    print(f"  冰水貯水桶容量 V2:          {result['V_cold_L']:.1f} L")
    
    print("\n【計算結果】")
    print(f"  熱水溫度校正係數 K1:        {result['K1']:.3f}")
    print(f"  冰水溫度校正係數 K2:        {result['K2']:.3f}")
    print(f"  等效內容量 Veq:             {result['Veq_L']:.3f} L")
    print(f"  容許耗用能源基準:           {result['E_standard_kWh']:.3f} kWh")
    
    print("\n【能源效率分級門檻】")
    for grade in [1, 2, 3, 4, 5]:
        threshold = result['limits_kWh'][grade]
        status = "✓" if result['E24_kWh'] <= threshold else "✗"
        print(f"  {grade}級: E24 ≤ {threshold:.3f} kWh  {status}")
    
    print("\n【判定結果】")
    if result['grade'] is not None:
        print(f"  ✓ 符合容許耗用能源基準")
        print(f"  ✓ 能源效率等級: {result['grade']}級")
        print(f"  ✓ 餘裕量: {result['margin_kWh']:.3f} kWh ({result['margin_percent']:.1f}%)")
    else:
        print(f"  ✗ 不符合容許耗用能源基準")
        print(f"  ✗ 能源效率等級: 不合格")
        exceed = result['E24_kWh'] - result['E_standard_kWh']
        print(f"  超出基準值: {exceed:.3f} kWh ({abs(result['margin_percent']):.1f}%)")
    
    print("=" * 70)

def print_report(input: HotWarmDispenserInput, result: dict):
    """
    輸出格式化的測試報告
    """
    print("=" * 70)
    print("CNS 3910 溫熱型飲水機能源效率測試報告")
    print("=" * 70)
    print("\n【輸入參數】")
    print(f"  24小時備用損失 E24:        {input.E24_kWh:.3f} kWh")
    print(f"  熱水系統平均水溫 T_hot:     {input.T_hot24_C:.1f} °C")
    print(f"  周圍溫度 T_amb:             {input.T_amb_C:.1f} °C")
    print(f"  熱貯水桶標示容量 V:         {input.V_marked_L:.1f} L")
    
    print("\n【計算結果】")
    print(f"  溫度校正係數 K:             {result['K']:.6f}")
    print(f"  標準化待機損失 E_st,24:     {result['E_st24_kWh']:.3f} kWh")
    print(f"  容許耗用能源基準 MEPS:      {result['MEPS_kWh']:.3f} kWh")
    
    print("\n【能源效率分級門檻】")
    for grade in [1, 2, 3, 4, 5]:
        threshold = result['limits_kWh'][grade]
        status = "✓" if result['E_st24_kWh'] <= threshold else "✗"
        print(f"  {grade}級: E_st,24 ≤ {threshold:.3f} kWh  {status}")
    
    print("\n【判定結果】")
    if result['grade'] is not None:
        print(f"  ✓ 符合容許耗用能源基準（MEPS）")
        print(f"  ✓ 能源效率等級: {result['grade']}級")
    else:
        print(f"  ✗ 不符合容許耗用能源基準（MEPS）")
        print(f"  ✗ 能源效率等級: 不合格")
        exceed = result['E_st24_kWh'] - result['MEPS_kWh']
        print(f"  超出 MEPS 限值: {exceed:.3f} kWh ({exceed/result['MEPS_kWh']*100:.1f}%)")
    
    print("=" * 70)

# --- 範例（取你圖片中的數據）---
if __name__ == "__main__":
    print("【溫熱型飲水機測試】\n")
    
    demo = HotWarmDispenserInput(
        E24_kWh=1.152,   # 每24小時備用損失
        T_hot24_C=87.0,  # 熱水系統24h平均水溫
        T_amb_C=25.0,    # 周圍溫度
        V_marked_L=1.4   # 熱貯水桶標示容量
    )
    result = evaluate(demo)
    print_report(demo, result)
    
    print("\n" + "=" * 70)
    print("測試案例 2: 符合標準的溫熱型飲水機")
    print("=" * 70 + "\n")
    
    demo2 = HotWarmDispenserInput(
        E24_kWh=0.500,   # 較低的備用損失
        T_hot24_C=85.0,
        T_amb_C=25.0,
        V_marked_L=2.0
    )
    result2 = evaluate(demo2)
    print_report(demo2, result2)
    
    print("\n\n" + "=" * 70)
    print("【冰溫熱型飲水機測試】")
    print("=" * 70 + "\n")
    
    # 測試案例 3: 冰溫熱型 - Veq ≤ 12L
    demo3 = ColdHotDispenserInput(
        E24_kWh=1.200,   # 24小時備用損失
        T_hot_C=88.0,    # 熱水平均溫度
        T_cold_C=8.0,    # 冰水平均溫度
        T_amb_C=25.0,    # 周圍溫度
        V_hot_L=2.5,     # 熱水桶容量
        V_cold_L=3.0     # 冰水桶容量
    )
    result3 = evaluate_cold_hot(demo3)
    print_report_cold_hot(demo3, result3)
    
    print("\n" + "=" * 70)
    print("測試案例 4: 冰溫熱型 - Veq > 12L (大容量)")
    print("=" * 70 + "\n")
    
    # 測試案例 4: 冰溫熱型 - Veq > 12L
    demo4 = ColdHotDispenserInput(
        E24_kWh=1.500,   # 24小時備用損失
        T_hot_C=90.0,    # 熱水平均溫度
        T_cold_C=5.0,    # 冰水平均溫度
        T_amb_C=25.0,    # 周圍溫度
        V_hot_L=8.0,     # 熱水桶容量
        V_cold_L=10.0    # 冰水桶容量
    )
    result4 = evaluate_cold_hot(demo4)
    print_report_cold_hot(demo4, result4)

