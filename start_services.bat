@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM 清屏
cls

echo.
echo ========================================
echo 🔥 热成像 API 和前端应用启动工具
echo ========================================
echo.

REM 定义路径
set PROJECT_PATH=C:\Users\1\Desktop\新
set API_PATH=%PROJECT_PATH%\red_pdf
set CONDA_ENV=dip

echo 📍 项目路径: %PROJECT_PATH%
echo 📍 API 路径: %API_PATH%
echo 📍 conda 环境: %CONDA_ENV%
echo.

echo 选择要启动的服务:
echo.
echo 1) 启动 API 服务 (Flask)
echo 2) 启动前端应用 (npm)
echo 3) 同时启动 API 和前端
echo 4) 打开 API 测试页面
echo 5) 运行 API 测试脚本
echo 6) 全部启动 (API + 前端 + 测试页面)
echo.

set /p choice="请选择 (1-6): "

if "%choice%"=="1" (
    call :start_api
) else if "%choice%"=="2" (
    call :start_frontend
) else if "%choice%"=="3" (
    call :start_both
) else if "%choice%"=="4" (
    call :open_test_page
) else if "%choice%"=="5" (
    call :run_test_script
) else if "%choice%"=="6" (
    call :start_all
) else (
    echo ❌ 无效的选择
    exit /b 1
)

exit /b 0

:start_api
echo.
echo ========================================
echo 🔧 启动 API 服务...
echo ========================================
echo.
echo 命令: conda activate %CONDA_ENV% && cd %API_PATH% && python thermal_api.py
echo.
call conda activate %CONDA_ENV%
cd /d %API_PATH%
python thermal_api.py
exit /b 0

:start_frontend
echo.
echo ========================================
echo 📦 启动前端应用...
echo ========================================
echo.
echo 命令: cd %PROJECT_PATH% && npm run dev
echo.
cd /d %PROJECT_PATH%
npm run dev
exit /b 0

:start_both
echo.
echo ========================================
echo 🚀 启动 API 和前端...
echo ========================================
echo.
echo 启动 API (后台运行)...
start "API服务" cmd /k "conda activate %CONDA_ENV% && cd /d %API_PATH% && python thermal_api.py"
echo ✅ API 已在新窗口启动

timeout /t 3 /nobreak

echo.
echo 启动前端应用...
start "前端应用" cmd /k "cd /d %PROJECT_PATH% && npm run dev"
echo ✅ 前端已在新窗口启动

echo.
echo ========================================
echo ✅ 启动完成！
echo ========================================
echo 📍 API 地址: http://localhost:5000
echo 📍 前端地址: http://localhost:5173 (可能不同，请查看输出)
echo.
pause
exit /b 0

:open_test_page
echo.
echo ========================================
echo 🧪 打开 API 测试页面...
echo ========================================
echo.
echo URL: file:///%PROJECT_PATH:\=/%/API_TEST.html
echo.
start "" "file:///%PROJECT_PATH:\=/%/API_TEST.html"
echo ✅ 测试页面已在浏览器中打开
echo.
pause
exit /b 0

:run_test_script
echo.
echo ========================================
echo 🧪 运行 API 测试脚本...
echo ========================================
echo.
cd /d %PROJECT_PATH%
call conda activate %CONDA_ENV%
python test_api_direct.py
echo.
pause
exit /b 0

:start_all
echo.
echo ========================================
echo 🌟 全部启动 (API + 前端 + 测试页面)
echo ========================================
echo.

echo 启动 API (后台运行)...
start "API服务" cmd /k "conda activate %CONDA_ENV% && cd /d %API_PATH% && python thermal_api.py"
echo ✅ API 已启动

timeout /t 2 /nobreak

echo 启动前端应用 (后台运行)...
start "前端应用" cmd /k "cd /d %PROJECT_PATH% && npm run dev"
echo ✅ 前端已启动

timeout /t 3 /nobreak

echo 打开测试页面...
start "" "file:///%PROJECT_PATH:\=/%/API_TEST.html"
echo ✅ 测试页面已打开

echo.
echo ========================================
echo ✅ 所有服务已启动！
echo ========================================
echo.
echo 📍 API 地址: http://localhost:5000
echo 📍 前端地址: http://localhost:5173 (可能不同)
echo 📍 测试页面: 已在浏览器中打开
echo.
echo 💡 提示:
echo   • API 窗口会显示详细日志
echo   • 前端窗口会显示编译信息
echo   • 关闭任何窗口会停止对应服务
echo.
pause
exit /b 0
