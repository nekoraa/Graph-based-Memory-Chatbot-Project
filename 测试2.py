import os
import requests
import json

import 基本信息文档


# from 记忆体 import 记忆图操作函数




def 语言模型(消息):
    # 从环境变量中获取 API 密钥（确保你已将 API 密钥设置为环境变量）
    api_key = 'xai-0QoO7ze0t2mLnMj6rfdQhlX8VtM5N26SGPPH5YFslTcCw5tWtXxAdqcTRM4Bi6PrDm9sqmumqu26GBJ8'

    if not api_key:
        return {"error": "API 密钥缺失"}

    # 定义 API 端点
    url = 'https://api.x.ai/v1/chat/completions'

    # 设置请求头
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # 定义请求的负载（数据）
    data = {
        "messages": 消息,
        "model": "grok-beta",  # 假设使用这个模型
        "stream": False,
        "temperature": 0
    }

    try:
        # 发送 POST 请求到 API
        response = requests.post(url, headers=headers, json=data)  # 使用json参数来自动序列化数据

        # 检查响应状态并返回回答内容
        if response.status_code == 200:
            # 提取并返回回答的内容
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return {"error": f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"请求出错: {str(e)}"}


消息 = [
    {"role": "system", "content": "你是聊天机器人"},
    {"role": "user", "content": "你好"}
]



print(语言模型(消息))
