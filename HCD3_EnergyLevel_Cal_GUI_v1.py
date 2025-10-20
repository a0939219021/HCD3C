#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNS 3910 温热型饮水机能源效率计算器 - GUI版本
支持中文/英文/韩文界面
"""

import tkinter as tk
from tkinter import ttk, messagebox
from HCD3_EnergyLevel_Cal_Core import HotWarmDispenserInput, evaluate

# 多语言支持
LANGUAGES = {
    'zh': {
        'title': 'CNS 3910 能源效率計算器',
        'lang_label': '語言 / Language / 언어:',
        'input_frame': '測試數據輸入',
        'E24_label': '24小時備用損失 (kWh):',
        'T_hot_label': '熱水系統平均水溫 (°C):',
        'T_amb_label': '周圍溫度 (°C):',
        'V_label': '熱貯水桶標示容量 (L):',
        'calculate_btn': '計算能效等級',
        'clear_btn': '清除',
        'result_frame': '計算結果',
        'K_label': '溫度校正係數 K:',
        'Est24_label': '標準化待機損失 E_st,24:',
        'MEPS_label': '容許基準 MEPS:',
        'grade_label': '能源效率等級:',
        'grade_thresholds': '分級門檻',
        'grade_1': '1級 (最高效)',
        'grade_2': '2級',
        'grade_3': '3級',
        'grade_4': '4級',
        'grade_5': '5級',
        'pass': '✓ 通過',
        'fail': '✗ 未通過',
        'not_qualified': '不合格',
        'error_title': '輸入錯誤',
        'error_msg': '請輸入有效的數字',
        'error_temp': '熱水溫度必須高於周圍溫度',
        'kWh_unit': 'kWh',
    },
    'en': {
        'title': 'CNS 3910 Energy Efficiency Calculator',
        'lang_label': 'Language / 語言 / 언어:',
        'input_frame': 'Test Data Input',
        'E24_label': '24h Standby Loss (kWh):',
        'T_hot_label': 'Hot Water Avg. Temp (°C):',
        'T_amb_label': 'Ambient Temperature (°C):',
        'V_label': 'Tank Capacity (L):',
        'calculate_btn': 'Calculate Efficiency',
        'clear_btn': 'Clear',
        'result_frame': 'Calculation Results',
        'K_label': 'Temperature Correction Factor K:',
        'Est24_label': 'Normalized Standby Loss E_st,24:',
        'MEPS_label': 'MEPS Standard:',
        'grade_label': 'Energy Efficiency Grade:',
        'grade_thresholds': 'Grade Thresholds',
        'grade_1': 'Grade 1 (Best)',
        'grade_2': 'Grade 2',
        'grade_3': 'Grade 3',
        'grade_4': 'Grade 4',
        'grade_5': 'Grade 5',
        'pass': '✓ Pass',
        'fail': '✗ Fail',
        'not_qualified': 'Not Qualified',
        'error_title': 'Input Error',
        'error_msg': 'Please enter valid numbers',
        'error_temp': 'Hot water temperature must be higher than ambient',
        'kWh_unit': 'kWh',
    },
    'ko': {
        'title': 'CNS 3910 에너지 효율 계산기',
        'lang_label': '언어 / Language / 語言:',
        'input_frame': '테스트 데이터 입력',
        'E24_label': '24시간 대기 손실 (kWh):',
        'T_hot_label': '온수 시스템 평균 온도 (°C):',
        'T_amb_label': '주변 온도 (°C):',
        'V_label': '온수 탱크 용량 (L):',
        'calculate_btn': '효율 등급 계산',
        'clear_btn': '지우기',
        'result_frame': '계산 결과',
        'K_label': '온도 보정 계수 K:',
        'Est24_label': '표준화 대기 손실 E_st,24:',
        'MEPS_label': '허용 기준 MEPS:',
        'grade_label': '에너지 효율 등급:',
        'grade_thresholds': '등급 임계값',
        'grade_1': '1등급 (최고 효율)',
        'grade_2': '2등급',
        'grade_3': '3등급',
        'grade_4': '4등급',
        'grade_5': '5등급',
        'pass': '✓ 합격',
        'fail': '✗ 불합격',
        'not_qualified': '부적격',
        'error_title': '입력 오류',
        'error_msg': '유효한 숫자를 입력하세요',
        'error_temp': '온수 온도는 주변 온도보다 높아야 합니다',
        'kWh_unit': 'kWh',
    }
}

class CNS3910Calculator:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'zh'  # 默认中文
        
        # 设置窗口
        self.root.title(LANGUAGES[self.current_lang]['title'])
        self.root.geometry("800x750")
        self.root.resizable(False, False)
        
        # 配色方案
        self.colors = {
            'bg': '#f0f4f8',
            'frame_bg': '#ffffff',
            'primary': '#2563eb',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'text': '#1f2937',
            'grade_1': '#10b981',  # 绿色
            'grade_2': '#3b82f6',  # 蓝色
            'grade_3': '#f59e0b',  # 橙色
            'grade_4': '#f97316',  # 深橙
            'grade_5': '#ef4444',  # 红色
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        self.create_widgets()
        
    def create_widgets(self):
        # 主容器
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题和语言选择
        self.create_header(main_container)
        
        # 输入区域
        self.create_input_section(main_container)
        
        # 按钮区域
        self.create_button_section(main_container)
        
        # 结果区域
        self.create_result_section(main_container)
        
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # 标题
        self.title_label = tk.Label(
            header_frame,
            text=LANGUAGES[self.current_lang]['title'],
            font=('Arial', 20, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        )
        self.title_label.pack(side='left')
        
        # 语言选择
        lang_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        lang_frame.pack(side='right')
        
        self.lang_label = tk.Label(
            lang_frame,
            text=LANGUAGES[self.current_lang]['lang_label'],
            font=('Arial', 10),
            bg=self.colors['bg']
        )
        self.lang_label.pack(side='left', padx=(0, 5))
        
        self.lang_var = tk.StringVar(value='中文')
        lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.lang_var,
            values=['中文', 'English', '한국어'],
            state='readonly',
            width=10
        )
        lang_combo.pack(side='left')
        lang_combo.bind('<<ComboboxSelected>>', self.change_language)
        
    def create_input_section(self, parent):
        input_frame = tk.LabelFrame(
            parent,
            text=LANGUAGES[self.current_lang]['input_frame'],
            font=('Arial', 12, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['text'],
            relief='solid',
            borderwidth=1,
            padx=20,
            pady=15
        )
        input_frame.pack(fill='x', pady=(0, 15))
        
        # 输入字段
        self.entries = {}
        fields = [
            ('E24', 'E24_label', '1.152'),
            ('T_hot', 'T_hot_label', '87.0'),
            ('T_amb', 'T_amb_label', '25.0'),
            ('V', 'V_label', '1.4')
        ]
        
        for i, (key, label_key, default) in enumerate(fields):
            frame = tk.Frame(input_frame, bg=self.colors['frame_bg'])
            frame.pack(fill='x', pady=8)
            
            label = tk.Label(
                frame,
                text=LANGUAGES[self.current_lang][label_key],
                font=('Arial', 11),
                bg=self.colors['frame_bg'],
                width=30,
                anchor='w'
            )
            label.pack(side='left')
            
            entry = tk.Entry(
                frame,
                font=('Arial', 11),
                width=20,
                relief='solid',
                borderwidth=1
            )
            entry.pack(side='right')
            entry.insert(0, default)
            
            self.entries[key] = {
                'entry': entry,
                'label': label,
                'label_key': label_key
            }
    
    def create_button_section(self, parent):
        btn_frame = tk.Frame(parent, bg=self.colors['bg'])
        btn_frame.pack(fill='x', pady=(0, 15))
        
        self.calc_btn = tk.Button(
            btn_frame,
            text=LANGUAGES[self.current_lang]['calculate_btn'],
            font=('Arial', 12, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            relief='flat',
            padx=30,
            pady=10,
            cursor='hand2',
            command=self.calculate
        )
        self.calc_btn.pack(side='left', padx=(0, 10))
        
        self.clear_btn = tk.Button(
            btn_frame,
            text=LANGUAGES[self.current_lang]['clear_btn'],
            font=('Arial', 12),
            bg='#6b7280',
            fg='white',
            relief='flat',
            padx=30,
            pady=10,
            cursor='hand2',
            command=self.clear_inputs
        )
        self.clear_btn.pack(side='left')
    
    def create_result_section(self, parent):
        self.result_frame = tk.LabelFrame(
            parent,
            text=LANGUAGES[self.current_lang]['result_frame'],
            font=('Arial', 12, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['text'],
            relief='solid',
            borderwidth=1,
            padx=20,
            pady=15
        )
        self.result_frame.pack(fill='both', expand=True)
        
        # 结果标签（初始为空）
        self.result_labels = {}
        
    def calculate(self):
        try:
            # 获取输入值
            E24 = float(self.entries['E24']['entry'].get())
            T_hot = float(self.entries['T_hot']['entry'].get())
            T_amb = float(self.entries['T_amb']['entry'].get())
            V = float(self.entries['V']['entry'].get())
            
            # 验证温度关系
            if T_hot <= T_amb:
                messagebox.showerror(
                    LANGUAGES[self.current_lang]['error_title'],
                    LANGUAGES[self.current_lang]['error_temp']
                )
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
            self.display_results(result)
            
        except ValueError:
            messagebox.showerror(
                LANGUAGES[self.current_lang]['error_title'],
                LANGUAGES[self.current_lang]['error_msg']
            )
    
    def display_results(self, result):
        # 清空之前的结果
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        lang = LANGUAGES[self.current_lang]
        
        # 基本结果
        results_data = [
            (lang['K_label'], f"{result['K']:.6f}"),
            (lang['Est24_label'], f"{result['E_st24_kWh']:.3f} {lang['kWh_unit']}"),
            (lang['MEPS_label'], f"{result['MEPS_kWh']:.3f} {lang['kWh_unit']}"),
        ]
        
        for label_text, value_text in results_data:
            frame = tk.Frame(self.result_frame, bg=self.colors['frame_bg'])
            frame.pack(fill='x', pady=5)
            
            label = tk.Label(
                frame,
                text=label_text,
                font=('Arial', 11),
                bg=self.colors['frame_bg'],
                width=30,
                anchor='w'
            )
            label.pack(side='left')
            
            value = tk.Label(
                frame,
                text=value_text,
                font=('Arial', 11, 'bold'),
                bg=self.colors['frame_bg'],
                fg=self.colors['primary']
            )
            value.pack(side='right')
        
        # 分割线
        separator = tk.Frame(self.result_frame, height=2, bg='#e5e7eb')
        separator.pack(fill='x', pady=15)
        
        # 等级门槛
        threshold_label = tk.Label(
            self.result_frame,
            text=lang['grade_thresholds'],
            font=('Arial', 11, 'bold'),
            bg=self.colors['frame_bg']
        )
        threshold_label.pack(anchor='w', pady=(0, 10))
        
        # 显示各等级
        for grade in [1, 2, 3, 4, 5]:
            self.display_grade_row(grade, result)
        
        # 最终判定 - 大图标显示
        self.display_final_grade(result)
    
    def display_grade_row(self, grade, result):
        lang = LANGUAGES[self.current_lang]
        threshold = result['limits_kWh'][grade]
        passed = result['E_st24_kWh'] <= threshold
        
        frame = tk.Frame(self.result_frame, bg=self.colors['frame_bg'])
        frame.pack(fill='x', pady=3)
        
        # 等级颜色
        color = self.colors[f'grade_{grade}']
        
        # 等级标签
        grade_label = tk.Label(
            frame,
            text=lang[f'grade_{grade}'],
            font=('Arial', 10),
            bg=self.colors['frame_bg'],
            fg=color,
            width=20,
            anchor='w'
        )
        grade_label.pack(side='left')
        
        # 门槛值
        threshold_label = tk.Label(
            frame,
            text=f"≤ {threshold:.3f} {lang['kWh_unit']}",
            font=('Arial', 10),
            bg=self.colors['frame_bg'],
            width=20
        )
        threshold_label.pack(side='left')
        
        # 通过/未通过
        status_text = lang['pass'] if passed else lang['fail']
        status_color = self.colors['success'] if passed else '#9ca3af'
        
        status_label = tk.Label(
            frame,
            text=status_text,
            font=('Arial', 10, 'bold'),
            bg=self.colors['frame_bg'],
            fg=status_color
        )
        status_label.pack(side='right')
    
    def display_final_grade(self, result):
        lang = LANGUAGES[self.current_lang]
        
        # 分割线
        separator = tk.Frame(self.result_frame, height=2, bg='#e5e7eb')
        separator.pack(fill='x', pady=15)
        
        # 最终等级显示
        final_frame = tk.Frame(self.result_frame, bg='#f9fafb', relief='solid', borderwidth=2)
        final_frame.pack(fill='x', pady=10, padx=10)
        
        grade_label = tk.Label(
            final_frame,
            text=lang['grade_label'],
            font=('Arial', 12, 'bold'),
            bg='#f9fafb'
        )
        grade_label.pack(pady=(15, 5))
        
        if result['grade'] is not None:
            grade = result['grade']
            color = self.colors[f'grade_{grade}']
            grade_text = f"{grade}"
            
            # 大号等级显示
            grade_value = tk.Label(
                final_frame,
                text=grade_text,
                font=('Arial', 48, 'bold'),
                bg='#f9fafb',
                fg=color
            )
            grade_value.pack(pady=10)
            
            # 等级文字
            grade_desc = tk.Label(
                final_frame,
                text=lang[f'grade_{grade}'],
                font=('Arial', 14),
                bg='#f9fafb',
                fg=color
            )
            grade_desc.pack(pady=(0, 15))
        else:
            # 不合格
            fail_label = tk.Label(
                final_frame,
                text=lang['not_qualified'],
                font=('Arial', 36, 'bold'),
                bg='#f9fafb',
                fg=self.colors['danger']
            )
            fail_label.pack(pady=20)
            
            # 超出数值
            exceed = result['E_st24_kWh'] - result['MEPS_kWh']
            exceed_label = tk.Label(
                final_frame,
                text=f"{lang['MEPS_label']} +{exceed:.3f} {lang['kWh_unit']} ({exceed/result['MEPS_kWh']*100:.1f}%)",
                font=('Arial', 11),
                bg='#f9fafb',
                fg=self.colors['danger']
            )
            exceed_label.pack(pady=(0, 15))
    
    def clear_inputs(self):
        # 清空输入
        self.entries['E24']['entry'].delete(0, tk.END)
        self.entries['T_hot']['entry'].delete(0, tk.END)
        self.entries['T_amb']['entry'].delete(0, tk.END)
        self.entries['V']['entry'].delete(0, tk.END)
        
        # 清空结果
        for widget in self.result_frame.winfo_children():
            widget.destroy()
    
    def change_language(self, event=None):
        lang_map = {'中文': 'zh', 'English': 'en', '한국어': 'ko'}
        selected = self.lang_var.get()
        self.current_lang = lang_map[selected]
        
        # 重建界面
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.create_widgets()

def main():
    root = tk.Tk()
    app = CNS3910Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

