import json


def 转换_json_为_数组(json_data):
    # 获取节点数组
    节点 = json_data["节点"]

    # 获取边数组
    边 = []
    for 边项 in json_data["边"]:
        边列表 = [边项["节点1"], 边项["节点2"], 边项["属性"]]
        边.append(边列表)

    return 节点, 边


# # 示例 JSON 数据
# json_data = {
#     "节点": [
#         "蕾米莉亚",
#         "东方project",
#         "芙兰朵露",
#         "幻想乡",
#         "红魔馆",
#         "平常并不太易怒，但精神有些问题。"
#     ],
#     "边": [
#         {"节点1": "蕾米莉亚", "节点2": "东方project", "属性": "蕾米莉亚属于东方project这个游戏"},
#         {"节点1": "芙兰朵露", "节点2": "东方project", "属性": "芙兰朵露属于东方project这个游戏"},
#         {"节点1": "幻想乡", "节点2": "东方project", "属性": "幻想乡是东方project这个游戏里的世界名称"},
#         {"节点1": "红魔馆", "节点2": "东方project", "属性": "红魔馆是东方project这个游戏世界里的一个地区"},
#         {"节点1": "蕾米莉亚", "节点2": "芙兰朵露", "属性": "蕾米莉亚是芙兰朵露的姐姐"},
#         {"节点1": "蕾米莉亚", "节点2": "红魔馆", "属性": "蕾米莉亚住在红魔馆"},
#         {"节点1": "芙兰朵露", "节点2": "红魔馆", "属性": "芙兰朵露住在红魔馆"},
#         {"节点1": "平常并不太易怒，但精神有些问题。", "节点2": "芙兰朵露", "属性": "芙兰朵露的性格"}
#     ]
# }
#


import json
import os
import random

import torch
from matplotlib import pyplot as plt
from transformers import AutoModel
import networkx as nx
import numpy as np
import pickle

from 测试2 import 语言模型

# 获取当前文件夹路径
当前文件夹 = os.path.dirname(os.path.abspath(__file__))

# 设置模型下载路径为当前文件夹
模型路径 = os.path.join(当前文件夹, "模型文件夹")

# Initialize the model
model = AutoModel.from_pretrained("jinaai/jina-embeddings-v3", trust_remote_code=True, cache_dir=模型路径,
                                  device_map="cuda", torch_dtype=torch.float16)


texts1 = [
 "彈幕影片分享網站"
]

texts2 = [
 "弹幕视频分享网站"
]

# When calling the `encode` function, you can choose a `task` based on the use case:
# 'retrieval.query', 'retrieval.passage', 'separation', 'classification', 'text-matching'
# Alternatively, you can choose not to pass a `task`, and no specific LoRA adapter will be used.
embeddings1 = model.encode(texts1, task="text-matching")
embeddings2 = model.encode(texts2, task="text-matching")
# Compute similarities
print(embeddings1, embeddings2)
print(embeddings1[0] @ embeddings2[0].T)