#!/bin/bash

# 设置Conda初始化路径
source ~/miniconda3/etc/profile.d/conda.sh

# 激活环境
conda activate dalle

# 启动Python服务，记录日志
HF_ENDPOINT=https://hf-mirror.com nohup uvicorn main:app --host 0.0.0.0 --port 8080 > app.log 2>&1 &

echo "服务已启动，日志写入 app.log"
