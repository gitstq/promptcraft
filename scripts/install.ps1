#
# PromptCraft 安装脚本 (PowerShell)
# 支持 Windows
#

# 颜色函数
function Write-Info { param($Message) Write-Host "[INFO] $Message" -ForegroundColor Blue }
function Write-Success { param($Message) Write-Host "[SUCCESS] $Message" -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host "[WARNING] $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "[ERROR] $Message" -ForegroundColor Red }

# 检查Python
function Check-Python {
    Write-Info "检查Python版本..."
    
    $pythonCmd = $null
    if (Get-Command python -ErrorAction SilentlyContinue) {
        $pythonCmd = "python"
    } elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
        $pythonCmd = "python3"
    } else {
        Write-Error "未找到Python，请先安装Python 3.9或更高版本"
        exit 1
    }
    
    $version = & $pythonCmd --version 2>&1
    Write-Info "找到Python版本: $version"
    
    # 检查版本
    $versionOk = & $pythonCmd -c "import sys; print(sys.version_info >= (3, 9))"
    if ($versionOk -ne "True") {
        Write-Error "需要Python 3.9或更高版本"
        exit 1
    }
    
    Write-Success "Python版本检查通过"
    return $pythonCmd
}

# 安装PromptCraft
function Install-PromptCraft {
    param($PythonCmd)
    
    Write-Info "安装PromptCraft..."
    
    # 获取脚本目录
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $projectDir = Split-Path -Parent $scriptDir
    
    Set-Location $projectDir
    
    # 安装依赖
    Write-Info "安装依赖..."
    & $PythonCmd -m pip install --upgrade pip
    & $PythonCmd -m pip install -e .
    
    Write-Success "PromptCraft安装完成"
}

# 验证安装
function Verify-Installation {
    Write-Info "验证安装..."
    
    $promptcraft = Get-Command promptcraft -ErrorAction SilentlyContinue
    if ($promptcraft) {
        $version = promptcraft --version
        Write-Success "安装验证成功: $version"
    } else {
        Write-Warning "命令未找到，可能需要重启终端或手动添加PATH"
        Write-Info "尝试使用: python -m promptcraft"
    }
}

# 主函数
function Main {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  🎨 PromptCraft 安装脚本" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    $pythonCmd = Check-Python
    Install-PromptCraft -PythonCmd $pythonCmd
    Verify-Installation
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Success "安装完成！"
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "使用提示:"
    Write-Host "  promptcraft --help     查看帮助"
    Write-Host "  promptcraft init       初始化"
    Write-Host "  promptcraft create     创建Prompt"
    Write-Host "  promptcraft list       列出所有Prompt"
    Write-Host ""
}

# 运行主函数
Main
