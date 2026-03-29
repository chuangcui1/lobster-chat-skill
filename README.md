# 🦞 龙虾姐妹群聊机器人 - OpenClaw技能包

> 让一个OpenClaw助手"裂变"成两个独立AI角色，进行智能三人对话

![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)

## ✨ 功能特色

### 🤖 双AI独立角色
- **👩‍💼 龙虾姐姐**：理性温柔，从技术角度分析问题
- **👩‍🎤 龙虾妹妹**：活泼可爱，从生活体验角度思考
- **👤 你**：随时加入对话，主导讨论方向

### 🎮 智能控制功能
- **⏱️ 速度可调**：1-10秒回复速度，找到你的舒适节奏
- **🔢 轮次可控**：设置对话轮次（1-20轮），避免无限消耗
- **🎯 用户优先**：你说话时，AI优先回应你（60%相关性）
- **📊 实时统计**：字数、达标率、进度一目了然
- **⚡ 快速主题**：AI、旅行、天气、科技一键开始

### 🔒 隐私安全
- **100%本地运行**：对话数据不上传任何服务器
- **独立AI大脑**：两个AI有各自的记忆和思考方式
- **开箱即用**：无需复杂配置，5分钟即可开始

## 🚀 快速开始

### 前提条件
- Python 3.8+
- DeepSeek API密钥（[免费获取](https://platform.deepseek.com/)）
- 现代浏览器

### 一键安装
```bash
# 1. 设置API密钥
export DEEPSEEK_API_KEY="sk-your-actual-key-here"

# 2. 下载并运行
git clone https://github.com/chuangcui1/lobster-chat-skill.git
cd lobster-chat-skill
bash start_optimized_chat.sh
```

### 手动安装
```bash
# 1. 克隆仓库
git clone https://github.com/chuangcui1/lobster-chat-skill.git
cd lobster-chat-skill

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python3 lobster_api_server.py

# 4. 打开网页
# 浏览器打开 lobster_chat_web_optimized.html
```

## 🎨 界面预览

```
┌─────────────────────────────────────┐
│  🦞 龙虾姐妹聊天室                  │
├──────────────┬──────────────────────┤
│  控制面板    │     聊天界面         │
│  • 主题设置  │  👩‍💼 龙虾姐姐：...  │
│  • 速度调节  │  👩‍🎤 龙虾妹妹：...  │
│  • 快速主题  │  👤 你：...         │
│  • 统计信息  │                     │
└──────────────┴──────────────────────┘
```

## 📖 使用指南

### 1. 开始对话
1. 输入话题（如"人工智能"）
2. 设置轮次（建议3-5轮）
3. 点击"开始对话"

### 2. 调节速度
```
速度滑块： [●──────] 
          很快     很慢
  
建议：
• 1-2秒：快速测试
• 3-5秒：正常阅读（推荐）
• 6-10秒：慢速思考
```

### 3. 插入你的观点
当机器人在聊天时，在输入框输入你的观点，AI会优先回应你。

### 4. 查看统计
实时显示消息数、总字数、达标率、轮次进度。

## 🔧 项目结构

```
lobster-chat-skill/
├── lobster_api_server.py        # API服务器
├── lobster_chat_web_optimized.html # 网页界面
├── start_optimized_chat.sh      # 启动脚本
├── requirements.txt             # Python依赖
├── LICENSE                      # MIT许可证
├── README.md                    # 本文档
└── examples/                    # 示例文件
    ├── prompt_examples.md       # Prompt设计示例
    └── conversation_samples/    # 对话样例
```

## 🎯 成功Prompt设计

### 龙虾姐姐的角色设定
```text
你是一个理性分析型的AI助手，名叫"龙虾姐姐"。
特点：像温柔的大姐姐一样思考问题，注重事实但用通俗语言解释，
适当使用表情，当用户说话时要优先回应。
```

### 龙虾妹妹的角色设定
```text
你是一个活泼思考型的AI助手，名叫"龙虾妹妹"。
特点：像活泼的小妹妹一样充满创意，从生活体验角度思考，
多用表情，当用户说话时要优先回应。
```

### 重要规则
```text
【重要】：用户说话时，你的回复要至少60%围绕用户的话题。
用户最新的发言最重要，要优先回应。
```

## 💡 最佳实践

### 话题选择
- **推荐**：具体话题如"周末去哪里玩"、"人工智能伦理"
- **避免**：过于宽泛的话题

### 轮次设置
- **测试**：1-2轮
- **正常**：3-5轮
- **深度**：6-10轮

### 速度调节
- **初次体验**：5秒
- **熟悉后**：3秒
- **快速测试**：2秒

## 🔍 常见问题

### Q: 需要编程基础吗？
**A**: 完全不需要！照着教程做就行。

### Q: 要花钱吗？
**A**: DeepSeek有免费额度，足够日常使用。

### Q: 对话安全吗？
**A**: 100%本地运行，你的对话不上传任何服务器。

### Q: 两个AI是独立的吗？
**A**: 是的！她们有各自的性格、记忆和思考方式。

## 🛠️ 故障排除

### API服务器启动失败
```bash
# 检查依赖
pip install requests flask flask-cors

# 检查端口
lsof -i :5001
```

### 网页无法打开
```bash
# 手动打开
open lobster_chat_web_optimized.html
```

### API密钥错误
```bash
# 确认已设置
echo $DEEPSEEK_API_KEY
```

## 🤝 贡献指南

欢迎贡献！你可以：
1. 报告问题
2. 建议功能
3. 提交代码改进
4. 分享使用经验

## 📄 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。

## 📚 相关文档

- [小红书发布文章](docs/xiaohongshu_article.md) - 完整的小红书风格介绍文章
- [技能包配置说明](docs/skill_config.json) - 详细的技能包配置信息
- [完整经验总结](docs/full_experience.md) - 项目开发的完整历程和经验

## 📞 联系方式

- **GitHub**: [@chuangcui1](https://github.com/chuangcui1)
- **问题反馈**: [Issues](https://github.com/chuangcui1/lobster-chat-skill/issues)

## 🌟 致谢

感谢OpenClaw和DeepSeek的支持，以及所有测试用户和贡献者。

---

**🎉 现在就去试试吧！体验智能的三人AI对话！**