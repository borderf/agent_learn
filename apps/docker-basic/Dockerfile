# 基础镜像，slim是基于Debian的轻量级版本，适合生产环境
FROM python:3.14-slim

# 工作目录，容器中所有后续命令的当前目录都是/app，路径清晰，避免散落在根目录下
WORKDIR /app


# 分层复制，先复制依赖文件，再复制源码
# 如果只改源码不改依赖，第一步缓存直接命中，避免了改一行代码都要重装所有依赖
# 复制依赖文件
# pyproject.toml 声明了 readme = "README.md"，构建元数据时需要读取这个文件
COPY pyproject.toml requirements.txt README.md ./

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码（在 pyproject.toml 中 src 是源码目录）
COPY src/ ./src/

# 安装项目自身（将 src 纳入 Python 路径）
# -e 选项表示以可编辑模式安装，方便开发调试，修改代码后不需要重新安装
# 安装后，src 目录下的模块可以直接通过 import 导入，且修改后立即生效
RUN pip install --no-cache-dir -e .

# 暴露端口
EXPOSE 8000

# 默认启动 FastAPI 应用
CMD ["uvicorn", "docker_basic.apps.main:app", "--host", "0.0.0.0", "--port", "8000"]
