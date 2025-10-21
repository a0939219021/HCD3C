#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HCD3 冰温热型饮水供应机能效计算器 - 简化版GUI
专门针对冰温热型，界面更清晰
"""

import tkinter as tk
from tkinter import ttk, messagebox
from HCD3_EnergyLevel_Cal_Core import ColdHotDispenserInput, evaluate_cold_hot

# 多语言支持
LANGUAGES = {
    'zh': {
        'title': 'HCD3 冰溫熱型飲水供應機能效計算器',
        'lang_label': '語言:',
        'input_frame': '測試數據輸入',
        'E24_label': '24小時備用損失 E24 (kWh):',
        'T_hot_label': '熱水平均溫度 Th (°C):',
        'T_cold_label': '冰水平均溫度 Tc (°C):',
        'T_amb_label': '周圍溫度 T_amb (°C):',
        'V_hot_label': '熱水貯水桶容量 V1 (L):',
        'V_cold_label': '冰水貯水桶容量 V2 (L):',
        'calculate_btn': '計算能效等級',
        'clear_btn': '清除',
        'result_frame': '計算結果',
        'K1_label': '熱水校正係數 K1:',
        'K2_label': '冰水校正係數 K2:',
        'Veq_label': '等效內容量 Veq:',
        'E_standard_label': '容許耗用能源基準:',
        'grade_label': '能源效率等級:',
        'grade_thresholds': '能效分級門檻',
        'grade_1': '1級 (最高效)',
        'grade_2': '2級',
        'grade_3': '3級',
        'grade_4': '4級',
        'grade_5': '5級',
        'pass': '✓ 通過',
        'fail': '✗ 未通過',
        'qualified': '✓ 合格',
        'not_qualified': '✗ 不合格',
        'error_title': '輸入錯誤',
        'error_msg': '請輸入有效的數字',
        'error_temp': '熱水溫度必須高於周圍溫度',
        'error_temp_cold': '冰水溫度必須低於周圍溫度',
        'kWh_unit': 'kWh',
        'L_unit': 'L',
    },
    'en': {
        'title': 'HCD3 Cold-Hot Water Dispenser Energy Calculator',
        'lang_label': 'Language:',
        'input_frame': 'Test Data Input',
        'E24_label': '24h Standby Loss E24 (kWh):',
        'T_hot_label': 'Hot Water Avg. Temp Th (°C):',
        'T_cold_label': 'Cold Water Avg. Temp Tc (°C):',
        'T_amb_label': 'Ambient Temperature T_amb (°C):',
        'V_hot_label': 'Hot Water Tank Capacity V1 (L):',
        'V_cold_label': 'Cold Water Tank Capacity V2 (L):',
        'calculate_btn': 'Calculate Energy Grade',
        'clear_btn': 'Clear',
        'result_frame': 'Calculation Results',
        'K1_label': 'Hot Water Factor K1:',
        'K2_label': 'Cold Water Factor K2:',
        'Veq_label': 'Equivalent Volume Veq:',
        'E_standard_label': 'Energy Consumption Standard:',
        'grade_label': 'Energy Efficiency Grade:',
        'grade_thresholds': 'Grade Thresholds',
        'grade_1': 'Grade 1 (Best)',
        'grade_2': 'Grade 2',
        'grade_3': 'Grade 3',
        'grade_4': 'Grade 4',
        'grade_5': 'Grade 5',
        'pass': '✓ Pass',
        'fail': '✗ Fail',
        'qualified': '✓ Qualified',
        'not_qualified': '✗ Not Qualified',
        'error_title': 'Input Error',
        'error_msg': 'Please enter valid numbers',
        'error_temp': 'Hot water temperature must be higher than ambient',
        'error_temp_cold': 'Cold water temperature must be lower than ambient',
        'kWh_unit': 'kWh',
        'L_unit': 'L',
    },
    'ko': {
        'title': 'HCD3 냉온열 정수기 에너지 효율 계산기',
        'lang_label': '언어:',
        'input_frame': '테스트 데이터 입력',
        'E24_label': '24시간 대기 손실 E24 (kWh):',
        'T_hot_label': '온수 평균 온도 Th (°C):',
        'T_cold_label': '냉수 평균 온도 Tc (°C):',
        'T_amb_label': '주변 온도 T_amb (°C):',
        'V_hot_label': '온수 탱크 용량 V1 (L):',
        'V_cold_label': '냉수 탱크 용량 V2 (L):',
        'calculate_btn': '에너지 등급 계산',
        'clear_btn': '지우기',
        'result_frame': '계산 결과',
        'K1_label': '온수 보정 계수 K1:',
        'K2_label': '냉수 보정 계수 K2:',
        'Veq_label': '등가 용량 Veq:',
        'E_standard_label': '에너지 소비 기준:',
        'grade_label': '에너지 효율 등급:',
        'grade_thresholds': '등급 임계값',
        'grade_1': '1등급 (최고 효율)',
        'grade_2': '2등급',
        'grade_3': '3등급',
        'grade_4': '4등급',
        'grade_5': '5등급',
        'pass': '✓ 합격',
        'fail': '✗ 불합격',
        'qualified': '✓ 적격',
        'not_qualified': '✗ 부적격',
        'error_title': '입력 오류',
        'error_msg': '유효한 숫자를 입력하세요',
        'error_temp': '온수 온도는 주변 온도보다 높아야 합니다',
        'error_temp_cold': '냉수 온도는 주변 온도보다 낮아야 합니다',
        'kWh_unit': 'kWh',
        'L_unit': 'L',
    }
}

class HCD3ColdHotCalculator:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'zh'
        
        self.root.title(LANGUAGES[self.current_lang]['title'])
        
        # RWD: 获取屏幕尺寸并设置初始窗口大小为屏幕的70%
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.7)
        window_height = int(screen_height * 0.7)
        
        # 设置最小窗口尺寸
        min_width = 800
        min_height = 700
        self.root.minsize(min_width, min_height)
        
        # 居中显示窗口
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(True, True)
        
        # RWD: 保存当前窗口尺寸，用于计算缩放比例
        self.current_width = window_width
        self.current_height = window_height
        self.base_width = 1000  # 基准宽度
        self.base_height = 900  # 基准高度
        
        # 配色
        self.colors = {
            'bg': '#f0f4f8',
            'frame_bg': '#ffffff',
            'primary': '#2563eb',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'text': '#1f2937',
            'grade_1': '#10b981',
            'grade_2': '#3b82f6',
            'grade_3': '#f59e0b',
            'grade_4': '#f97316',
            'grade_5': '#ef4444',
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # RWD: 创建带滚动条的主容器
        self.create_scrollable_frame()
        self.create_widgets()
        
        # RWD: 监听窗口大小变化
        self.root.bind('<Configure>', self.on_window_resize)
    
    def create_scrollable_frame(self):
        """RWD: 创建带滚动条的可滚动容器"""
        # 创建主容器框架
        container = tk.Frame(self.root, bg=self.colors['bg'])
        container.pack(fill="both", expand=True)
        
        # 创建画布和滚动条
        self.canvas = tk.Canvas(container, bg=self.colors['bg'], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        
        # 创建内部框架
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg'])
        
        # 配置滚动区域
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # 在画布上创建窗口
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # 布局
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # RWD: 确保内容填充整个 Canvas 宽度
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # 鼠标滚轮支持
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_canvas_configure(self, event):
        """RWD: Canvas 大小变化时，调整内部框架宽度"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def _on_mousewheel(self, event):
        """RWD: 处理鼠标滚轮事件"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def on_window_resize(self, event):
        """RWD: 响应窗口大小变化"""
        # 只处理根窗口的resize事件，避免处理子组件的事件
        if event.widget == self.root:
            new_width = event.width
            new_height = event.height
            
            # 防止频繁更新（只在尺寸变化超过50像素时更新）
            if abs(new_width - self.current_width) > 50 or abs(new_height - self.current_height) > 50:
                self.current_width = new_width
                self.current_height = new_height
                # 可以在这里添加字体大小调整等响应式操作
    
    def get_responsive_font_size(self, base_size):
        """RWD: 根据窗口大小计算响应式字体大小"""
        scale_factor = min(self.current_width / self.base_width, 
                          self.current_height / self.base_height)
        # 限制缩放范围在0.8到1.2之间
        scale_factor = max(0.8, min(1.2, scale_factor))
        return int(base_size * scale_factor)
    
    def get_responsive_padding(self, base_padding):
        """RWD: 根据窗口大小计算响应式内边距"""
        scale_factor = min(self.current_width / self.base_width, 
                          self.current_height / self.base_height)
        scale_factor = max(0.8, min(1.2, scale_factor))
        return int(base_padding * scale_factor)
        
    def create_widgets(self):
        # RWD: 使用可滚动的容器而不是固定的frame
        padding = self.get_responsive_padding(10)  # 从20减少到10，更紧密
        main_container = tk.Frame(self.scrollable_frame, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=padding, pady=padding)
        
        # RWD: 使用grid布局以获得更好的响应式效果
        main_container.grid_columnconfigure(0, weight=1)
        
        self.create_header(main_container)
        self.create_input_section(main_container)
        self.create_button_section(main_container)
        self.create_result_section(main_container)
        
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 10))  # 从20减少到10
        
        # RWD: 响应式标题字体
        title_font_size = self.get_responsive_font_size(18)
        label_font_size = self.get_responsive_font_size(10)
        
        self.title_label = tk.Label(
            header_frame,
            text=LANGUAGES[self.current_lang]['title'],
            font=('Arial', title_font_size, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        )
        self.title_label.pack(side='left')
        
        lang_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        lang_frame.pack(side='right')
        
        self.lang_label = tk.Label(
            lang_frame,
            text=LANGUAGES[self.current_lang]['lang_label'],
            font=('Arial', label_font_size),
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
        # RWD: 响应式字体
        frame_font = self.get_responsive_font_size(12)
        padding = self.get_responsive_padding(15)  # 从20减少到15
        
        self.input_frame = tk.LabelFrame(
            parent,
            text=LANGUAGES[self.current_lang]['input_frame'],
            font=('Arial', frame_font, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['text'],
            relief='solid',
            borderwidth=1,
            padx=padding,
            pady=10  # 从15减少到10
        )
        self.input_frame.pack(fill='x', pady=(0, 10))  # 从15减少到10
        
        # 冰温热型输入字段
        fields = [
            ('E24', 'E24_label', '0.400'),
            ('T_hot', 'T_hot_label', '88.0'),
            ('T_cold', 'T_cold_label', '8.0'),
            ('T_amb', 'T_amb_label', '25.0'),
            ('V_hot', 'V_hot_label', '2.5'),
            ('V_cold', 'V_cold_label', '3.0'),
        ]
        
        self.entries = {}
        for key, label_key, default in fields:
            self.add_input_field(key, LANGUAGES[self.current_lang][label_key], default)
    
    def add_input_field(self, key, label_text, default_value):
        # RWD: 使用grid布局代替固定宽度
        frame = tk.Frame(self.input_frame, bg=self.colors['frame_bg'])
        frame.pack(fill='x', pady=5, padx=5)  # 从pady=8,padx=10减少到5,5
        
        # RWD: 配置grid权重，让组件自动伸缩
        frame.grid_columnconfigure(0, weight=2)  # 标签占2份
        frame.grid_columnconfigure(1, weight=1)  # 输入框占1份
        
        font_size = self.get_responsive_font_size(11)
        
        label = tk.Label(
            frame,
            text=label_text,
            font=('Arial', font_size),
            bg=self.colors['frame_bg'],
            anchor='w'
        )
        label.grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        entry = tk.Entry(
            frame,
            font=('Arial', font_size),
            relief='solid',
            borderwidth=1
        )
        entry.grid(row=0, column=1, sticky='ew')
        entry.insert(0, default_value)
        
        self.entries[key] = {'entry': entry, 'label': label}
    
    def create_button_section(self, parent):
        btn_frame = tk.Frame(parent, bg=self.colors['bg'])
        btn_frame.pack(fill='x', pady=(0, 10))  # 从15减少到10
        
        lang = LANGUAGES[self.current_lang]
        
        # RWD: 响应式按钮字体和内边距
        btn_font = self.get_responsive_font_size(12)
        btn_padx = self.get_responsive_padding(20)  # 从30减少到20
        btn_pady = self.get_responsive_padding(8)   # 从10减少到8
        
        self.calc_btn = tk.Button(
            btn_frame,
            text=lang['calculate_btn'],
            font=('Arial', btn_font, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            relief='flat',
            padx=btn_padx,
            pady=btn_pady,
            cursor='hand2',
            command=self.calculate
        )
        self.calc_btn.pack(side='left', padx=(0, 10))
        
        self.clear_btn = tk.Button(
            btn_frame,
            text=lang['clear_btn'],
            font=('Arial', btn_font),
            bg='#6b7280',
            fg='white',
            relief='flat',
            padx=btn_padx,
            pady=btn_pady,
            cursor='hand2',
            command=self.clear_inputs
        )
        self.clear_btn.pack(side='left')
    
    def create_result_section(self, parent):
        lang = LANGUAGES[self.current_lang]
        
        # RWD: 响应式字体和内边距
        frame_font = self.get_responsive_font_size(12)
        padding = self.get_responsive_padding(15)  # 从20减少到15
        
        self.result_frame = tk.LabelFrame(
            parent,
            text=lang['result_frame'],
            font=('Arial', frame_font, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['text'],
            relief='solid',
            borderwidth=1,
            padx=padding,
            pady=10  # 从15减少到10
        )
        self.result_frame.pack(fill='both', expand=True)
    
    def calculate(self):
        lang = LANGUAGES[self.current_lang]
        
        try:
            E24 = float(self.entries['E24']['entry'].get())
            T_hot = float(self.entries['T_hot']['entry'].get())
            T_cold = float(self.entries['T_cold']['entry'].get())
            T_amb = float(self.entries['T_amb']['entry'].get())
            V_hot = float(self.entries['V_hot']['entry'].get())
            V_cold = float(self.entries['V_cold']['entry'].get())
            
            if T_hot <= T_amb:
                messagebox.showerror(lang['error_title'], lang['error_temp'])
                return
            
            if T_cold >= T_amb:
                messagebox.showerror(lang['error_title'], lang['error_temp_cold'])
                return
            
            input_data = ColdHotDispenserInput(
                E24_kWh=E24,
                T_hot_C=T_hot,
                T_cold_C=T_cold,
                T_amb_C=T_amb,
                V_hot_L=V_hot,
                V_cold_L=V_cold
            )
            
            result = evaluate_cold_hot(input_data)
            self.display_results(result)
            
        except ValueError:
            messagebox.showerror(lang['error_title'], lang['error_msg'])
    
    def display_results(self, result):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        lang = LANGUAGES[self.current_lang]
        
        # 基本结果
        results_data = [
            (lang['K1_label'], f"{result['K1']:.3f}"),
            (lang['K2_label'], f"{result['K2']:.3f}"),
            (lang['Veq_label'], f"{result['Veq_L']:.3f} {lang['L_unit']}"),
            (lang['E_standard_label'], f"{result['E_standard_kWh']:.3f} {lang['kWh_unit']}"),
            (f"E24 {lang['kWh_unit']}", f"{result['E24_kWh']:.3f} {lang['kWh_unit']}"),
        ]
        
        for label_text, value_text in results_data:
            self.add_result_row(label_text, value_text, bold=True)
        
        self.add_separator()
        
        # 等级门槛
        threshold_label = tk.Label(
            self.result_frame,
            text=lang['grade_thresholds'],
            font=('Arial', 12, 'bold'),
            bg=self.colors['frame_bg']
        )
        threshold_label.pack(anchor='w', pady=(0, 8))  # 从15减少到8
        
        # 显示各等级
        for grade in [1, 2, 3, 4, 5]:
            self.display_grade_row(grade, result)
        
        # 最终判定
        self.display_final_grade(result)
    
    def add_result_row(self, label_text, value_text, bold=False):
        # RWD: 使用grid布局代替固定宽度
        frame = tk.Frame(self.result_frame, bg=self.colors['frame_bg'])
        frame.pack(fill='x', pady=3, padx=5)  # 从pady=6,padx=10减少到3,5
        
        # RWD: 配置grid权重
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=0)
        
        font_weight = 'bold' if bold else 'normal'
        font_size = self.get_responsive_font_size(11)
        
        label = tk.Label(
            frame,
            text=label_text,
            font=('Arial', font_size, font_weight),
            bg=self.colors['frame_bg'],
            anchor='w'
        )
        label.grid(row=0, column=0, sticky='w')
        
        value = tk.Label(
            frame,
            text=value_text,
            font=('Arial', font_size, font_weight),
            bg=self.colors['frame_bg'],
            fg=self.colors['primary']
        )
        value.grid(row=0, column=1, sticky='e', padx=(10, 0))
    
    def add_separator(self):
        separator = tk.Frame(self.result_frame, height=2, bg='#e5e7eb')
        separator.pack(fill='x', pady=8)  # 从15减少到8
    
    def display_grade_row(self, grade, result):
        lang = LANGUAGES[self.current_lang]
        threshold = result['limits_kWh'][grade]
        E24_value = result['E24_kWh']
        passed = E24_value <= threshold
        
        # RWD: 使用grid布局
        frame = tk.Frame(self.result_frame, bg=self.colors['frame_bg'])
        frame.pack(fill='x', pady=3, padx=5)  # 从pady=5,padx=10减少到3,5
        
        # RWD: 配置grid权重
        frame.grid_columnconfigure(0, weight=2)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_columnconfigure(2, weight=1)
        
        color = self.colors[f'grade_{grade}']
        font_size = self.get_responsive_font_size(11)
        
        grade_label = tk.Label(
            frame,
            text=lang[f'grade_{grade}'],
            font=('Arial', font_size),
            bg=self.colors['frame_bg'],
            fg=color,
            anchor='w'
        )
        grade_label.grid(row=0, column=0, sticky='w')
        
        threshold_label = tk.Label(
            frame,
            text=f"≤ {threshold:.3f} {lang['kWh_unit']}",
            font=('Arial', font_size),
            bg=self.colors['frame_bg']
        )
        threshold_label.grid(row=0, column=1, sticky='w', padx=(10, 0))
        
        status_text = lang['pass'] if passed else lang['fail']
        status_color = self.colors['success'] if passed else '#9ca3af'
        
        status_label = tk.Label(
            frame,
            text=status_text,
            font=('Arial', font_size, 'bold'),
            bg=self.colors['frame_bg'],
            fg=status_color
        )
        status_label.grid(row=0, column=2, sticky='e')
    
    def display_final_grade(self, result):
        lang = LANGUAGES[self.current_lang]
        
        self.add_separator()
        
        final_frame = tk.Frame(self.result_frame, bg='#f9fafb', relief='solid', borderwidth=2)
        final_frame.pack(fill='x', pady=8, padx=5)  # 从pady=15,padx=10减少到8,5
        
        # RWD: 响应式字体大小
        title_font = self.get_responsive_font_size(14)
        large_font = self.get_responsive_font_size(48)
        medium_font = self.get_responsive_font_size(36)
        small_font = self.get_responsive_font_size(12)
        
        grade_label = tk.Label(
            final_frame,
            text=lang['grade_label'],
            font=('Arial', title_font, 'bold'),
            bg='#f9fafb'
        )
        grade_label.pack(pady=(10, 5))  # 从(15,10)减少到(10,5)
        
        if result['grade'] is not None:
            grade = result['grade']
            color = self.colors[f'grade_{grade}']
            
            grade_value = tk.Label(
                final_frame,
                text=str(grade),
                font=('Arial', large_font, 'bold'),
                bg='#f9fafb',
                fg=color
            )
            grade_value.pack(pady=5)  # 从10减少到5
            
            grade_desc = tk.Label(
                final_frame,
                text=lang[f'grade_{grade}'],
                font=('Arial', title_font),
                bg='#f9fafb',
                fg=color
            )
            grade_desc.pack(pady=(0, 10))  # 从(0,15)减少到(0,10)
        else:
            fail_label = tk.Label(
                final_frame,
                text=lang['not_qualified'],
                font=('Arial', medium_font, 'bold'),
                bg='#f9fafb',
                fg=self.colors['danger']
            )
            fail_label.pack(pady=10)  # 从20减少到10
            
            # 显示超出数值
            exceed = result['E24_kWh'] - result['E_standard_kWh']
            exceed_label = tk.Label(
                final_frame,
                text=f"{lang['E_standard_label']} +{exceed:.3f} {lang['kWh_unit']} ({exceed/result['E_standard_kWh']*100:.1f}%)",
                font=('Arial', small_font),
                bg='#f9fafb',
                fg=self.colors['danger']
            )
            exceed_label.pack(pady=(0, 10))  # 从(0,15)减少到(0,10)
    
    def clear_inputs(self):
        for key, widget_dict in self.entries.items():
            widget_dict['entry'].delete(0, tk.END)
        
        for widget in self.result_frame.winfo_children():
            widget.destroy()
    
    def change_language(self, event=None):
        lang_map = {'中文': 'zh', 'English': 'en', '한국어': 'ko'}
        selected = self.lang_var.get()
        self.current_lang = lang_map[selected]
        
        # RWD: 清除滚动框架内的内容而不是root
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.create_widgets()

def main():
    root = tk.Tk()
    app = HCD3ColdHotCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
