#!/bin/bash

# 龙虾机器人优化版启动脚本

echo "=================================================="
echo "🦞 龙虾机器人优化版对话系统"
echo "=================================================="
echo ""
echo "🎯 优化特性："
echo "   1. 📝 简洁回复：10-80字，短句换行"
echo "   2. ⏱️  速度控制：1-5秒可调节回复速度"
echo "   3. 🎨 优化界面：更好的消息排版"
echo "   4. 💾 记忆功能：记住速度偏好"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到Python3"
    exit 1
fi

# 检查requests库
echo "🔍 检查Python依赖..."
python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 安装requests库..."
    pip3 install requests flask flask-cors
fi

# 检查API密钥
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "⚠️  警告：未设置DeepSeek API密钥"
    echo ""
    echo "请设置环境变量："
    echo "   export DEEPSEEK_API_KEY='your-api-key'"
    echo ""
    read -p "是否继续以模拟模式运行？(y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "退出..."
        exit 1
    fi
    echo "将以模拟模式运行..."
else
    echo "✅ DeepSeek API密钥已设置"
fi

echo ""
echo "🚀 启动步骤："
echo ""

# 1. 启动API服务器
echo "1. 启动Python API服务器..."
cd ~/.openclaw
python3 lobster_api_server.py &
API_PID=$!
echo "   API服务器PID: $API_PID"
echo "   等待服务器启动..."

# 等待服务器启动
sleep 3

# 检查服务器是否运行
if curl -s http://localhost:5001/api/health > /dev/null; then
    echo "   ✅ API服务器运行正常"
else
    echo "   ⚠️  API服务器可能未启动，请检查端口5001"
fi

echo ""

# 2. 打开网页
echo "2. 打开优化版网页界面..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "   在浏览器中打开: lobster_chat_web_optimized.html"
    echo ""
    echo "💡 推荐使用Chrome或Safari浏览器"
    
    read -p "是否自动在浏览器中打开？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "正在打开网页..."
        open lobster_chat_web_optimized.html
    fi
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "   在浏览器中打开: lobster_chat_web_optimized.html"
    echo ""
    echo "💡 推荐使用Chrome或Firefox浏览器"
    
    read -p "是否自动在浏览器中打开？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "正在打开网页..."
        xdg-open lobster_chat_web_optimized.html 2>/dev/null || \
        echo "请手动打开: lobster_chat_web_optimized.html"
    fi
    
else
    # 其他系统
    echo "   请手动在浏览器中打开文件："
    echo "   ~/.openclaw/lobster_chat_web_optimized.html"
fi

echo ""
echo "🎮 使用方法："
echo "   1. 在左侧输入主题和轮次"
echo "   2. 使用滑块调节回复速度（1-5秒）"
echo "   3. 点击'开始对话'按钮"
echo "   4. 观察两个机器人的简洁对话"
echo "   5. 可以在输入框中插入消息参与讨论"
echo ""
echo "⚡ 速度调节建议："
echo "   • 1-2秒：快速对话，适合测试"
echo "   • 3-5秒：正常阅读，推荐"
echo "   • 6-10秒：慢速思考，适合仔细品味"
echo ""
echo "📊 速度记忆："
echo "   系统会记住你的速度偏好，下次自动使用"
echo ""

echo "🛑 停止系统："
echo "   1. 在终端按 Ctrl+C 停止API服务器"
echo "   2. 或者运行: kill $API_PID"
echo ""

echo "📁 文件列表："
ls -la ~/.openclaw/lobster_*.py ~/.openclaw/lobster_*.html 2>/dev/null | grep -E "(api_server|chat_web_optimized)" || echo "文件未找到"
echo ""

echo "=================================================="
echo "🎉 优化版系统启动完成！"
echo "=================================================="

# 等待用户按Ctrl+C
echo ""
echo "按 Ctrl+C 停止API服务器..."
wait $API_PID