# # 与智能助手在终端中聊天
# from openai import OpenAI
#
# # 指向本地服务器
# 客户端 = OpenAI(base_url="http://localhost:4526/v1", api_key="lm-studio")
#
# # 历史记录 = [
# #     {"role": "system",
# #      "content": "你是一个智能助手。你总是提供正确且有帮助的回答。"},
# #     {"role": "user",
# #      "content": "你好，向第一次打开此程序的人介绍自己。简洁一些。20个字"},
# # ]
#
#
# def 语言模型(信息):
#     完成 = 客户端.chat.completions.create(
#         model="model-identifier",
#         messages=信息,
#         temperature=0.8,
#         stream=True,
#     )
#
#     # 用于收集生成的内容
#     生成结果 = ""
#
#     for 数据块 in 完成:
#         if 数据块.choices[0].delta.content:
#             # 拼接生成内容
#             生成结果 += 数据块.choices[0].delta.content
#             print(数据块.choices[0].delta.content, end="", flush=True)
#
#     # 返回完整的生成结果
#     return 生成结果
#
#
# # print(语言模型(历史记录))

from http import HTTPStatus
import dashscope

from http import HTTPStatus
import dashscope

消息 = [{"role": "system", "content": "你是人工智能助手"},
        {"role": "user", "content": "你好"}]


def 语言模型(消息):
    响应结果 = dashscope.Generation.call(
        model="qwen-max",
        api_key="xxxx",
        messages=消息,
        stream=True,
        result_format='message',  # 将返回结果格式设置为 message
        top_p=0.8,
        temperature=0.7,
        enable_search=False
    )

    最终回答 = ""  # 用来保存最终的回答

    for 响应 in 响应结果:
        if 响应.status_code == HTTPStatus.OK:
            # 获取最后一个选择的内容
            最终回答 = 响应.output.choices[-1].message.content
        else:
            最终回答 = f"请求 ID: {响应.request_id}, 状态码: {响应.status_code}, 错误码: {响应.code}, 错误信息: {响应.message}"

    return 最终回答  # 返回最后一个完整的回答文本


# print(语言模型(消息))
