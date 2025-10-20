@echo off
chcp 65001 >nul
echo ========================================
echo HCD3 冰温热型饮水供应机能效计算器
echo 打包工具
echo ========================================
echo.

echo 正在打包简化版GUI程序...
pyinstaller --onefile --windowed --name "HCD3_EnergyLevel_Cal_GUI_Simple" HCD3_EnergyLevel_Cal_GUI_Simple.py

echo.
echo 正在打包完整版GUI程序...
pyinstaller --onefile --windowed --name "HCD3_EnergyLevel_Cal_GUI" HCD3_EnergyLevel_Cal_GUI.py

echo.
echo 正在打包核心计算模块...
pyinstaller --onefile --console --name "HCD3_EnergyLevel_Cal_Core" HCD3_EnergyLevel_Cal_Core.py

echo.
echo 正在打包交互式命令行工具...
pyinstaller --onefile --console --name "HCD3_EnergyLevel_Cal_Interactive" HCD3_EnergyLevel_Cal_Interactive.py

echo.
echo 正在打包批量处理工具...
pyinstaller --onefile --console --name "HCD3_EnergyLevel_Cal_Batch" HCD3_EnergyLevel_Cal_Batch.py

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 生成的文件位置：
echo   dist\HCD3_EnergyLevel_Cal_GUI_Simple.exe  - 简化版GUI（推荐）
echo   dist\HCD3_EnergyLevel_Cal_GUI.exe         - 完整版GUI
echo   dist\HCD3_EnergyLevel_Cal_Core.exe        - 核心计算模块
echo   dist\HCD3_EnergyLevel_Cal_Interactive.exe - 交互式命令行
echo   dist\HCD3_EnergyLevel_Cal_Batch.exe       - 批量处理工具
echo.
echo 双击运行 HCD3_EnergyLevel_Cal_GUI_Simple.exe 开始使用！
echo.
pause
