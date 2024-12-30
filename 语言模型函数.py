import torch

from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import 基本信息文档

# 获取当前文件夹路径
当前文件夹 = os.path.dirname(os.path.abspath(__file__))

# 设置模型下载路径为当前文件夹
模型路径 = os.path.join(当前文件夹, "模型文件夹")

# 加载预训练模型和分词器，指定模型缓存目录
模型 = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-1.5B-Instruct",
    cache_dir=模型路径,
    torch_dtype=torch.float16,
    device_map="auto"
)
分词器 = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct", cache_dir=模型路径)

停止参数 = 0


def 语言模型(消息):
    global 分词器
    global 停止参数

    # 使用分词器创建聊天模板
    聊天文本 = 分词器.apply_chat_template(
        消息,
        tokenize=False,
        add_generation_prompt=True
    )

    分词器 = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct", cache_dir=模型路径)

    生成文本 = ""

    输入 = 分词器(聊天文本, return_tensors="pt").to(模型.device)
    生成的ID = 输入.input_ids.clone()

    模型.eval()
    max_new_tokens = 512
    with torch.no_grad():
        for _ in range(max_new_tokens):
            输出 = 模型(生成的ID)

            # 应用温度调整采样
            logits = 输出.logits[:, -1, :] / 0.7  # 设置温度，0.7 为示例值
            概率 = torch.softmax(logits, dim=-1)
            下一个Token = torch.multinomial(概率, num_samples=1)  # 根据概率采样

            生成的ID = torch.cat([生成的ID, 下一个Token], dim=-1)

            # 解码并添加到存储变量中
            解码文本 = 分词器.batch_decode(下一个Token, skip_special_tokens=True)[0]

            生成文本 += 解码文本
            print(解码文本, end="", flush=True)

            if 停止参数 == 1:
                生成文本 = 生成文本 + "[[[_被用户打断_]]]"
                break
            # 如果遇到结束标志则停止
            if 下一个Token.item() == 分词器.eos_token_id:
                break
    print()
    return 生成文本





def add_to_chat(role, content):
    消息.append({"role": role, "content": content})


if __name__ == "__main__":
    系统设定 = "你是一个具有以下人格特征的虚拟角色：" + 基本信息文档.人格信息 + " 。你已经掌握了这些基本的人格记忆：" + "你的回答尽可能模仿人类,简短一点"
    消息 = [
        {"role": "system", "content": 系统设定},
    ]
    while True:
        输入 = input(">>>:")
        add_to_chat("user", 输入)

        输出 = 语言模型(消息)
        add_to_chat("assistant", 输出)
