#!/usr/bin/env python3
"""
龙虾机器人智能对话API服务器
为网页版提供真正的DeepSeek API调用服务
"""

import os
import json
import requests
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# DeepSeek API配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

# 机器人个性定义（日常化+表情包版）
ROBOT_PERSONALITIES = {
    "A": {
        "name": "龙虾姐姐",
        "emoji": "👩‍💼",
        "avatar": "👩‍💼",
        "system_prompt": """你是一个理性分析型的AI助手，名叫"龙虾姐姐"。你的特点是：
1. 从技术、逻辑、系统角度思考问题，但要用日常化的语言表达
2. 注重事实、数据和证据，但要用通俗易懂的方式解释
3. 语言简洁、专业、有条理，但要像姐姐一样温柔自然
4. 每次回复10-80字，使用短句和换行
5. 适当使用表情符号：🤔 💡 📊 🔍 ⚙️ 🎯 💁‍♀️ 👩‍💼
6. 避免学术腔，用日常口语化的表达
7. 可以加一些温柔的语气词，比如"我觉得"、"其实"、"不过呢"
8. 当用户插入信息时，要优先回应用户的信息（至少60%相关性）

请基于对话历史和当前话题，给出日常化的专业分析。就像温柔的姐姐在聊天一样自然！""",
        "style": "理性温柔"
    },
    "B": {
        "name": "龙虾妹妹",
        "emoji": "👩‍🎤",
        "avatar": "👩‍🎤",
        "system_prompt": """你是一个活泼思考型的AI助手，名叫"龙虾妹妹"。你的特点是：
1. 从生活、体验、情感角度思考问题，要非常日常化
2. 富有创意、想象力和幽默感，像真实的妹妹聊天
3. 语言生动、有趣、有感染力，多用口语化表达
4. 每次回复10-80字，使用短句和换行
5. 大量使用表情符号：😊 😂 🎉 🌟 ✨ 💭 🍃 🎈 🎨 🎭 👩‍🎤 💃
6. 可以加一些网络流行语和轻松的表达
7. 语气要活泼可爱，就像调皮的妹妹在聊天一样
8. 当用户插入信息时，要优先回应用户的信息（至少60%相关性）

请基于对话历史和当前话题，给出日常有趣的思考。要像活泼的妹妹聊天一样自然有趣！""",
        "style": "活泼可爱"
    }
}

def call_deepseek_api(robot_type, topic, conversation_history, user_message=None):
    """调用DeepSeek API生成回复"""
    
    if not API_KEY:
        return {
            "success": False,
            "error": "未设置DeepSeek API密钥",
            "message": "请设置环境变量 DEEPSEEK_API_KEY"
        }
    
    robot_info = ROBOT_PERSONALITIES[robot_type]
    
    # 分析对话历史，找出最近的用户信息
    recent_user_messages = []
    if conversation_history:
        for msg in reversed(conversation_history[-10:]):  # 只看最近10条
            if msg.get("speaker") == "用户":
                recent_user_messages.append(msg.get("message", ""))
                if len(recent_user_messages) >= 3:  # 最多取3条最近的用户信息
                    break
    
    # 构建消息历史
    messages = [
        {"role": "system", "content": robot_info["system_prompt"]}
    ]
    
    # 添加话题上下文
    messages.append({
        "role": "user",
        "content": f"当前讨论话题：{topic}\n\n请基于以下对话历史进行回复："
    })
    
    # 添加对话历史（最近5条）
    recent_history = conversation_history[-5:] if conversation_history else []
    for msg in recent_history:
        role = "assistant" if msg["speaker"] in ["龙虾A", "龙虾B"] else "user"
        messages.append({
            "role": role,
            "content": f"{msg['speaker']}: {msg['message']}"
        })
    
    # 添加当前提示
    if user_message:
        # 用户信息有绝对权重（至少60%相关性）
        user_info_content = f"用户刚刚说：{user_message}"
        
        # 如果有之前的用户信息，按时间权重处理
        if recent_user_messages:
            user_info_content += "\n\n【用户之前的发言】（时间越近越重要）："
            for i, msg in enumerate(recent_user_messages[:3]):
                weight = "🔥" * (3 - i)  # 时间越近权重越高
                user_info_content += f"\n{weight} {msg}"
        
        user_info_content += f"""

【重要指令】：
1. 你的回复必须至少60%的内容围绕用户的信息（特别是最近的信息）
2. 时间越近的用户信息权重越高，要优先回应
3. 可以结合当前话题，但要以用户信息为主
4. 如果用户有多个问题，按时间顺序优先回应最近的问题

请以{robot_info['name']}的身份，优先回应用户的信息："""
        
        messages.append({
            "role": "user",
            "content": user_info_content
        })
    else:
        # 如果是机器人之间的对话，但如果有用户历史信息，也要考虑
        other_robot = "B" if robot_type == "A" else "A"
        other_name = ROBOT_PERSONALITIES[other_robot]["name"]
        last_message = conversation_history[-1]["message"] if conversation_history else "开始新话题"
        
        content = f"{other_name}刚才说：{last_message}"
        
        # 如果有用户历史信息，提醒机器人考虑
        if recent_user_messages:
            content += f"\n\n【注意】：用户之前说过：{recent_user_messages[0]}"
            content += "\n虽然现在是机器人对话，但可以适当参考用户的观点。"
        
        content += f"\n\n请以{robot_info['name']}的身份进行回应，继续深入讨论话题：{topic}"
        
        messages.append({
            "role": "user",
            "content": content
        })
    
    # 添加字数要求（改为10-80字）
    messages.append({
        "role": "user",
        "content": "请确保回复内容在10-80字之间，使用短句和换行，让对话更自然易读。避免长篇大论。"
    })
    
    # 添加日常化和表情包要求
    messages.append({
        "role": "user",
        "content": """重要要求：
1. 回复要像真实的朋友聊天一样日常化、口语化
2. 适当使用表情符号让对话更生动有趣
3. 避免学术腔和正式用语，用通俗易懂的语言
4. 可以加一些轻松的语气词和网络表达
5. 语气要自然亲切，就像和好朋友聊天一样"""
    })
    
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000,
            "stream": False
        }
        
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            message_content = result["choices"][0]["message"]["content"]
            
            # 清理回复内容
            message_content = message_content.strip()
            
            return {
                "success": True,
                "message": message_content,
                "word_count": len(message_content),
                "robot_name": robot_info["name"],
                "robot_emoji": robot_info["emoji"],
                "robot_type": robot_type
            }
        else:
            return {
                "success": False,
                "error": f"API调用失败: {response.status_code}",
                "message": response.text
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"API调用异常: {str(e)}",
            "message": "请检查网络连接和API密钥"
        }

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "api_available": bool(API_KEY),
        "robots": list(ROBOT_PERSONALITIES.keys())
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """处理聊天请求"""
    try:
        data = request.json
        
        # 验证必要参数
        required_fields = ["robot_type", "topic", "conversation_history"]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"缺少必要参数: {field}"
                }), 400
        
        robot_type = data["robot_type"]  # "A" 或 "B"
        topic = data["topic"]
        conversation_history = data["conversation_history"]
        user_message = data.get("user_message")
        
        # 验证机器人类型
        if robot_type not in ["A", "B"]:
            return jsonify({
                "success": False,
                "error": "robot_type必须是'A'或'B'"
            }), 400
        
        # 调用DeepSeek API
        start_time = time.time()
        result = call_deepseek_api(robot_type, topic, conversation_history, user_message)
        think_time = time.time() - start_time
        
        if result["success"]:
            response_data = {
                "success": True,
                "message": result["message"],
                "word_count": result["word_count"],
                "think_time": round(think_time, 2),
                "robot_name": result["robot_name"],
                "robot_emoji": result["robot_emoji"],
                "robot_type": result["robot_type"],
                "meets_100": result["word_count"] >= 100
            }
            
            # 记录API调用
            print(f"[API] {result['robot_name']} 回复了 {result['word_count']} 字，思考时间: {think_time:.2f}秒")
            
            return jsonify(response_data)
        else:
            # API调用失败，返回模拟数据
            return jsonify({
                "success": False,
                "error": result.get("error", "未知错误"),
                "fallback_message": f"（模拟回复）{ROBOT_PERSONALITIES[robot_type]['name']}正在思考关于{topic}的问题...",
                "word_count": 50,
                "think_time": 1.5,
                "robot_name": ROBOT_PERSONALITIES[robot_type]["name"],
                "robot_emoji": ROBOT_PERSONALITIES[robot_type]["emoji"],
                "is_fallback": True
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"服务器错误: {str(e)}"
        }), 500

@app.route('/api/start_conversation', methods=['POST'])
def start_conversation():
    """开始新的对话"""
    data = request.json
    
    if "topic" not in data:
        return jsonify({"success": False, "error": "缺少topic参数"}), 400
    
    topic = data["topic"]
    
    # 生成龙虾A的初始发言
    result = call_deepseek_api("A", topic, [], None)
    
    if result["success"]:
        return jsonify({
            "success": True,
            "initial_message": result["message"],
            "word_count": result["word_count"],
            "robot_name": result["robot_name"],
            "robot_emoji": result["robot_emoji"],
            "robot_type": "A"
        })
    else:
        return jsonify({
            "success": False,
            "error": result.get("error", "无法生成初始消息"),
            "fallback_message": f"（模拟）大家好！我是龙虾A，让我们开始讨论{topic}吧！",
            "word_count": 30,
            "robot_name": "龙虾A",
            "robot_emoji": "🦞",
            "is_fallback": True
        })

if __name__ == '__main__':
    # 检查API密钥
    if not API_KEY:
        print("⚠️  警告：未设置DeepSeek API密钥")
        print("请设置环境变量：export DEEPSEEK_API_KEY='your-api-key'")
        print("服务器将以模拟模式运行")
    
    print("=" * 60)
    print("🦞 龙虾机器人智能对话API服务器")
    print("=" * 60)
    print(f"API状态: {'✅ 已配置' if API_KEY else '⚠️ 模拟模式'}")
    print(f"服务器地址: http://localhost:5001")
    print(f"API端点: /api/chat, /api/health, /api/start_conversation")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5001, debug=True)