import os
import sys
import torch
import sounddevice as sd
import numpy as np
from colorama import Fore
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import 语言模型函数, 基本信息文档

# 音频录制参数
采样率 = 16000  # Whisper 模型要求的采样率为 16kHz
时长 = 0.2  # 每次录制 0.2 秒音频块（用于检测）
声音阈值 = 0.0086 # 声音活动检测的阈值，值越大越敏感
静音阈值 = 3  # 检测到多少次连续静音后停止录音
保留参数 = 2

# 设置设备和模型
设备 = "cuda" if torch.cuda.is_available() else "cpu"
torch数据类型 = torch.float16 if torch.cuda.is_available() else torch.float32
# 模型ID = "openai/whisper-large-v3-turbo"
模型ID = "BELLE-2/Belle-whisper-large-v3-turbo-zh"

# 指定模型下载路径为当前 Python 文件夹
缓存目录 = os.path.dirname(os.path.abspath(__file__))

模型 = AutoModelForSpeechSeq2Seq.from_pretrained(
    模型ID,
    torch_dtype=torch数据类型,
    low_cpu_mem_usage=True,
    use_safetensors=True,
    cache_dir=缓存目录
)
模型.to(设备)

处理器 = AutoProcessor.from_pretrained(模型ID, cache_dir=缓存目录)

流水线 = pipeline(
    "automatic-speech-recognition",
    model=模型,
    tokenizer=处理器.tokenizer,
    feature_extractor=处理器.feature_extractor,
    torch_dtype=torch数据类型,
    device=设备,
    generate_kwargs={"forced_decoder_ids": 处理器.get_decoder_prompt_ids(language="zh", task="transcribe")}
)


def 识别模型(x1):
    # 语言模型函数.停止参数 = 0
    with torch.no_grad():
        # 输入数据 = 输入数据.to(设备)  # 将输入传送到GPU
        结果 = 流水线(x1)  # 在GPU上进行处理
    # 打印识别出的文本
    sys.stdout.write(f'\r ')
    print(Fore.BLUE + "用户:" + 结果["text"])

    # 语言模型函数.停止参数 = 0
    return 结果["text"]


def 是否有声音活动(音频):
    """通过计算音频信号能量来判断是否有声音活动"""
    return np.mean(np.abs(音频)) > 声音阈值


def 列出音频设备():
    """列出可用的音频输入设备"""
    设备列表 = sd.query_devices()
    输入设备 = [设备 for 设备 in 设备列表 if 设备['max_input_channels'] > 0]

    print("可用的音频输入设备:")
    for i, 设备 in enumerate(输入设备):
        print(f"{i + 1}: {设备['name']} (ID: {设备['index']})")

    return 输入设备


def 选择音频设备(设备列表):
    """让用户选择音频设备"""
    while True:
        try:
            选择 = int(input("请选择音频设备 (输入设备编号): ")) - 1
            if 0 <= 选择 < len(设备列表):
                return 设备列表[选择]['index']  # 返回设备的索引
            else:
                print("无效的设备编号，请重试。")
        except ValueError:
            print("请输入一个有效的数字。")


def 录音并识别(输入设备):
    """录音并进行语音识别"""
    音频缓冲区 = []
    静音计数 = 0
    正在录音 = False

    if 音频缓冲区:
        音频缓冲区 = 音频缓冲区[-(静音阈值-1):]
    else:
        音频缓冲区 = []

    计数次数 = 0
    while True:

        # 录制一小块音频
        音频 = sd.rec(int(时长 * 采样率), samplerate=采样率, channels=1, dtype="float32", device=输入设备)
        sd.wait()

        音频 = np.squeeze(音频)  # 去除多余的维度

        # 检测是否有声音活动
        if 是否有声音活动(音频):

            音频缓冲区.append(音频)  # 将有声音的音频片段加入缓冲区
            正在录音 = True
            静音计数 = 0
            # 语言模型函数.停止参数 = 1

            # print("检测到声音，正在录音...")
        elif 正在录音:
            音频缓冲区.append(音频)
            静音计数 += 1
            # print(f"静音检测中...{静音计数}")
            if 静音计数 >= 静音阈值:
                # 认为语音结束，开始识别

                # 将缓冲区中的音频片段拼接在一起
                全部音频 = np.concatenate(音频缓冲区)
                sys.stdout.write(f'\r ')

                return 识别模型(全部音频)

        else:
            音频缓冲区.append(音频)
            音频缓冲区 = 音频缓冲区[-保留参数:]
            pass


if __name__ == "__main__":
    # 列出音频设备并选择
    设备列表 = 列出音频设备()
    选择的设备 = 选择音频设备(设备列表)

    while True:
        print(录音并识别(选择的设备))
