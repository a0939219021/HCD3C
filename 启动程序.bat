@echo off
chcp 65001 >nul
title HCD3 冰温热型饮水供应机能效计算器
echo ========================================
echo HCD3 冰温热型饮水供应机能效计算器
echo ========================================
echo.
echo 正在启动程序...
echo.

REM 检查是否存在exe文件
if exist "HCD3_EnergyLevel_Cal_GUI_Simple.exe" (
    echo 启动简化版GUI程序...
    start "" "HCD3_EnergyLevel_Cal_GUI_Simple.exe"
) else if exist "dist\HCD3_EnergyLevel_Cal_GUI_Simple.exe" (
    echo 启动简化版GUI程序...
    start "" "dist\HCD3_EnergyLevel_Cal_GUI_Simple.exe"
) else (
    echo 未找到exe文件，尝试使用Python运行...
    python HCD3_EnergyLevel_Cal_GUI_Simple.py
)

echo.
echo 程序已启动！
echo 如果没有看到窗口，请检查任务栏。
echo.
pause
