#!/bin/bash
# DailyHotApi 服务安装 & 启动脚本
# 运行一次即可，服务会随系统启动自动运行

set -e

echo "======================================"
echo "🔥 DailyHotApi 服务安装向导"
echo "======================================"

# 检查 node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node 18+"
    exit 1
fi
echo "✅ Node.js $(node --version)"

# 检查 pm2
if ! command -v pm2 &> /dev/null; then
    echo "📦 安装 PM2..."
    npm install -g pm2
fi
echo "✅ PM2 已安装"

# 检查服务是否已部署
if [ -d "/tmp/DailyHotApi" ]; then
    echo "✅ DailyHotApi 已部署"
else
    echo "📦 克隆 DailyHotApi..."
    cd /tmp
    git clone https://ghproxy.net/https://github.com/imsyy/DailyHotApi.git --depth 1
    cd /tmp/DailyHotApi
    npm install
    npm run build
    echo "✅ DailyHotApi 构建完成"
fi

# 检查服务是否运行
if pm2 list | grep -q "online"; then
    echo "✅ DailyHotApi 服务运行中"
else
    echo "🚀 启动 DailyHotApi..."
    cd /tmp/DailyHotApi
    pm2 start ecosystem.config.cjs --name dailyhot-api
    pm2 save
    echo "✅ 服务已启动"
fi

# 验证
sleep 2
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:6688/weibo)
if [ "$RESPONSE" = "200" ]; then
    echo ""
    echo "======================================"
    echo "✅ 安装完成！服务运行在 http://localhost:6688"
    echo "======================================"
    echo ""
    echo "常用命令："
    echo "  pm2 list              # 查看服务状态"
    echo "  pm2 logs dailyhot-api # 查看日志"
    echo "  pm2 restart dailyhot-api  # 重启服务"
else
    echo "⚠️  服务启动异常，请运行 pm2 logs dailyhot-api 排查"
    exit 1
fi
