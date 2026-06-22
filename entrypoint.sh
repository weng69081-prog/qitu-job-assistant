#!/bin/bash
# 启动脚本 - 捕获错误
set -e

echo "=== 启动启途 AI 求职助手 ==="
echo "当前目录: $(pwd)"
echo "文件列表:"
ls -la
echo ""

echo "=== 检查 main.py ==="
if [ -f "main.py" ]; then
    echo "main.py 存在"
else
    echo "ERROR: main.py 不存在！"
    find /app -name "main.py" 2>/dev/null
fi

echo ""
echo "=== 启动 uvicorn ==="
exec uvicorn main:app --host 0.0.0.0 --port 8000