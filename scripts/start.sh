#!/bin/bash

# 获取 conda.sh 文件的路径。根据需要更新此路径。
CONDA_PATH="/c/Users/HRR/Anaconda/etc/profile.d/conda.sh"

# 检查 conda.sh 文件是否存在
if [ -f "$CONDA_PATH" ]; then
    # 源化 conda.sh 文件
    source "$CONDA_PATH"
else
    echo "Conda 路径不存在：$CONDA_PATH"
    exit 1
fi

# 激活您的 conda 环境
conda activate faculty_info

# 运行您的 Python 程序
python /c/Users/HRR/Desktop/faculty_info/main.py

