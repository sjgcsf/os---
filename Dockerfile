# 使用Python 3.8的官方镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录，所有后续命令将在该目录中执行
WORKDIR /app

# 复制requirements.txt文件到容器中
COPY requirements.txt requirements.txt

# 安装项目所需的依赖项
RUN pip install -r requirements.txt

# 复制项目文件到容器中（包括main.py、.env等）
COPY . .

# 定义Docker容器启动时运行的命令
CMD ["python", "main.py"]
