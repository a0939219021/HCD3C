@echo off
chcp 65001 >nul
title HCD3 冰温热型饮水供应机能效计算器 - 命令行版本
echo ========================================
echo HCD3 冰温热型饮水供应机能效计算器
echo 命令行版本
echo ========================================
echo.

REM 检查是否存在exe文件
if exist "HCD3_EnergyLevel_Cal_Core.exe" (
    echo 启动核心计算模块...
    "HCD3_EnergyLevel_Cal_Core.exe"
) else if exist "dist\HCD3_EnergyLevel_Cal_Core.exe" (
    echo 启动核心计算模块...
    "dist\HCD3_EnergyLevel_Cal_Core.exe"
) else (
    echo 未找到exe文件，尝试使用Python运行...
    python HCD3_EnergyLevel_Cal_Core.py
)

echo.
pause
