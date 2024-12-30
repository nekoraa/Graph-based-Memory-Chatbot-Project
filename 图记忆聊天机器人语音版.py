import json
import os

import 基本信息文档

# from 测试2 import 语言模型
# from 语言模型函数 import 语言模型
from lms语言函数 import 语言模型

from 记忆体 import 记忆图操作函数
from 记忆体.记忆图操作函数 import 检查或加载记忆图
from 语音识别实时翻译 import 录音并识别, 列出音频设备, 选择音频设备


def add_to_chat(role, content):
    消息.append({"role": role, "content": content})


默认信息 = 基本信息文档.人格信息

with open("系统设定.txt", "r", encoding="utf-8") as 文件:
    文件内容 = 文件.read()

系统设定 = 文件内容

if __name__ == "__main__":
    设备列表 = 列出音频设备()
    选择的设备 = 选择音频设备(设备列表)
    记忆图 = 检查或加载记忆图()

    # 判断是否存在且是文件夹
    if os.path.isfile("记忆体/聊天记录.json"):
        with open("记忆体/聊天记录.json", "r", encoding="utf-8") as file:
            消息 = json.load(file)
            print("读取成功")
    else:
        消息 = [
            {"role": "system", "content": 系统设定},
        ]
    while True:
        print("当前字数:" + str(记忆图操作函数.计算消息字符数(消息)))
        if 记忆图操作函数.计算消息字符数(消息) >= 30000:
            记忆图 = 记忆图操作函数.更新记忆函数(记忆图, 消息, 使用次数阈值=4, 休眠轮数阈值=30, 删除休眠轮数阈值=20)
            系统设定 = 记忆图操作函数.更新性格与设定(系统设定, 消息)
            消息 = [
                {"role": "system", "content": 系统设定},
            ]
            break
        输入 = 录音并识别(选择的设备)
        if 输入 == "停止":
            break
        if 输入 == "开始执行记忆整理":
            记忆图 = 记忆图操作函数.更新记忆函数(记忆图, 消息, 使用次数阈值=4, 休眠轮数阈值=30, 删除休眠轮数阈值=20)
            系统设定 = 记忆图操作函数.更新性格与设定(系统设定, 消息)
            消息 = [
                {"role": "system", "content": 系统设定},
            ]
            break

        add_to_chat("user", 输入)

        图数组 = 记忆图操作函数.检索图函数(记忆图, 输入, 3, 0.6, 2.5)
        提取记忆 = 记忆图操作函数.提取整理记忆(图数组)

        消息[0][
            "content"] = 系统设定 + "        " + "更具检索获得的记忆信息:" + 提取记忆 + "        当前时间:" + 记忆图操作函数.获取当前时间()

        输出 = 语言模型(消息)
        add_to_chat("assistant", 输出)


        print("風鈴:" + 输出)
        记忆图操作函数.文字转语音(输出)

    记忆图操作函数.保存图为_json(记忆图, "记忆图.pkl")

    folder_path = "记忆体"
    file_path = os.path.join(folder_path, "聊天记录.json")

    # 确保文件夹存在
    os.makedirs(folder_path, exist_ok=True)

    with open("系统设定.txt", "w", encoding="utf-8") as 文件:
        文件.write(系统设定)

    # 保存到文件
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(消息, file, ensure_ascii=False, indent=4)

    print(f"文件已保存到 {file_path}")
