# 启动热成像 API 服务 - Windows PowerShell 脚本

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🔥 热成像报告生成 API 服务" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python 是否安装
$pythonCmd = $null
$pythonVersions = @('python.exe', 'python3.exe')

foreach ($cmd in $pythonVersions) {
    try {
        $result = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = $cmd
            Write-Host "✅ 找到 Python: $cmd" -ForegroundColor Green
            Write-Host "   版本: $result" -ForegroundColor Gray
            break
        }
    } catch {
        # 继续尝试下一个命令
    }
}

if ($null -eq $pythonCmd) {
    Write-Host "❌ 未找到 Python 安装" -ForegroundColor Red
    Write-Host "   请先安装 Python 3.7+ (https://www.python.org)" -ForegroundColor Yellow
    Read-Host "按 Enter 退出"
    exit 1
}

# 检查必要的依赖
Write-Host ""
Write-Host "检查依赖..." -ForegroundColor Cyan
$requiredPackages = @('flask', 'python-docx')
$missingPackages = @()

foreach ($package in $requiredPackages) {
    try {
        $result = & $pythonCmd -c "import $($package.Replace('-', '_'))" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $package 已安装" -ForegroundColor Green
        } else {
            $missingPackages += $package
        }
    } catch {
        $missingPackages += $package
    }
}

# 提示安装缺失的包
if ($missingPackages.Count -gt 0) {
    Write-Host ""
    Write-Host "缺失的包: $($missingPackages -join ', ')" -ForegroundColor Yellow
    Write-Host ""
    $install = Read-Host "是否现在安装? (y/n)"
    
    if ($install -eq 'y' -or $install -eq 'Y') {
        Write-Host "安装中..." -ForegroundColor Cyan
        & $pythonCmd -m pip install -r requirements.txt
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ 安装失败，请手动运行: pip install -r requirements.txt" -ForegroundColor Red
            Read-Host "按 Enter 继续启动..."
        }
    }
}

# 检查必要的文件
Write-Host ""
Write-Host "检查必要文件..." -ForegroundColor Cyan
$requiredFiles = @('thermal_api.py', 'thermal_report_template.docx', 'generate_report.py')
$missingFiles = @()

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file 不存在" -ForegroundColor Red
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️ 缺失必要文件，API 可能无法正常运行" -ForegroundColor Yellow
}

# 启动 API 服务
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "启动 API 服务..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "服务地址: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "可用端点:" -ForegroundColor Yellow
Write-Host "  GET  /health                  - 健康检查" -ForegroundColor Gray
Write-Host "  GET  /api/v1/status           - 服务状态" -ForegroundColor Gray
Write-Host "  POST /api/v1/generate-pdf     - 单个生成 PDF" -ForegroundColor Gray
Write-Host "  POST /api/v1/batch-generate   - 批量生成 PDF" -ForegroundColor Gray
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

# 启动服务
& $pythonCmd thermal_api.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ 服务启动失败" -ForegroundColor Red
    Write-Host "   请检查错误信息并确保所有依赖已安装" -ForegroundColor Yellow
    Read-Host "按 Enter 退出"
    exit 1
}
