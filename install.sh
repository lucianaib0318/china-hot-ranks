#!/bin/bash
# 中国热榜聚合器 - 安装脚本
# 自动检查并安装所需依赖

set -e

echo "======================================"
echo "📊 中国热榜聚合器 - 安装向导"
echo "======================================"
echo ""

# 检查 Python
echo "🔍 检查 Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION"
else
    echo "❌ Python3 未安装"
    echo "💡 请安装 Python 3.6+: https://www.python.org/downloads/"
    exit 1
fi

# 检查 curl
echo ""
echo "🔍 检查 curl..."
if command -v curl &> /dev/null; then
    CURL_VERSION=$(curl --version | head -1)
    echo "✅ $CURL_VERSION"
else
    echo "❌ curl 未安装"
    echo "💡 请安装 curl:"
    echo "   Ubuntu/Debian: sudo apt install curl"
    echo "   macOS: brew install curl"
    echo "   CentOS: sudo yum install curl"
    exit 1
fi

# 检查 mcporter（可选）
echo ""
echo "🔍 检查 mcporter（可选）..."
if command -v mcporter &> /dev/null; then
    MCP_VERSION=$(mcporter --version 2>&1 | head -1)
    echo "✅ $MCP_VERSION"
    
    echo ""
    echo "🔍 检查 MCP 服务器..."
    mcporter list 2>/dev/null || echo "⚠️  无法列出 MCP 服务器"
    
    echo ""
    echo "🔍 检查微博 MCP..."
    if command -v mcp-server-weibo &> /dev/null; then
        echo "✅ 微博 MCP 已安装"
    else
        echo "⚠️  微博 MCP 未安装（可选）"
    fi
    
    echo ""
    echo "🔍 检查抖音 MCP..."
    if command -v mcp-server-douyin &> /dev/null; then
        echo "✅ 抖音 MCP 已安装"
    else
        echo "⚠️  抖音 MCP 未安装（可选）"
    fi
else
    echo "⚠️  mcporter 未安装（可选）"
    echo "💡 安装 mcporter 可以使用微博/抖音 MCP:"
    echo "   npm install -g mcporter"
    echo "   或参考：https://github.com/modelcontextprotocol/mcporter"
fi

# 检查代理（可选）
echo ""
echo "🔍 检查代理配置..."
if [ -n "$HTTPS_PROXY" ] || [ -n "$HTTP_PROXY" ]; then
    echo "✅ 代理已配置：${HTTPS_PROXY:-$HTTP_PROXY}"
else
    echo "⚠️  未检测到代理配置"
    echo "💡 GitHub 访问可能需要代理，可以设置:"
    echo "   export HTTPS_PROXY=http://127.0.0.1:7890"
    
    # 自动检测常见代理端口
    for port in 7890 10808 8888; do
        if curl -s -x "http://127.0.0.1:$port" --connect-timeout 2 https://www.google.com -o /dev/null 2>&1; then
            echo "✅ 检测到可用代理端口：$port"
            echo "💡 建议设置：export HTTPS_PROXY=http://127.0.0.1:$port"
            break
        fi
    done
fi

# 测试运行
echo ""
echo "🧪 测试运行..."
python3 hot_ranks.py baidu 2>&1 | head -5

echo ""
echo "======================================"
echo "✅ 安装完成！"
echo "======================================"
echo ""
echo "使用方法:"
echo "  python3 hot_ranks.py          # 获取所有热榜"
echo "  python3 hot_ranks.py weibo    # 微博热搜"
echo "  python3 hot_ranks.py github   # GitHub Trending"
echo ""
echo "详细说明请查看 README.md"
echo ""
