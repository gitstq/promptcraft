#!/bin/bash
#
# PromptCraft 安装脚本
# 支持 Linux/macOS
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Python版本
check_python() {
    print_info "检查Python版本..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "未找到Python，请先安装Python 3.9或更高版本"
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    print_info "找到Python版本: $PYTHON_VERSION"
    
    # 检查版本是否>=3.9
    REQUIRED_VERSION="3.9"
    if [ "$($PYTHON_CMD -c "import sys; print(sys.version_info >= (3, 9))")" != "True" ]; then
        print_error "需要Python 3.9或更高版本"
        exit 1
    fi
    
    print_success "Python版本检查通过"
}

# 安装PromptCraft
install_promptcraft() {
    print_info "安装PromptCraft..."
    
    # 获取脚本所在目录
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
    
    cd "$PROJECT_DIR"
    
    # 安装依赖
    print_info "安装依赖..."
    $PYTHON_CMD -m pip install --upgrade pip
    $PYTHON_CMD -m pip install -e .
    
    print_success "PromptCraft安装完成"
}

# 验证安装
verify_installation() {
    print_info "验证安装..."
    
    if command -v promptcraft &> /dev/null; then
        VERSION=$(promptcraft --version)
        print_success "安装验证成功: $VERSION"
    else
        print_warning "命令未找到，可能需要手动添加PATH"
        print_info "尝试使用: $PYTHON_CMD -m promptcraft"
    fi
}

# 主函数
main() {
    echo "========================================"
    echo "  🎨 PromptCraft 安装脚本"
    echo "========================================"
    echo ""
    
    check_python
    install_promptcraft
    verify_installation
    
    echo ""
    echo "========================================"
    print_success "安装完成！"
    echo "========================================"
    echo ""
    echo "使用提示:"
    echo "  promptcraft --help     查看帮助"
    echo "  promptcraft init       初始化"
    echo "  promptcraft create     创建Prompt"
    echo "  promptcraft list       列出所有Prompt"
    echo ""
}

# 运行主函数
main
