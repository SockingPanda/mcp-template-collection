# 快速开始指南

> **⚠️ 重要提示**: 这是一个基于模板项目的快速开始指南，包含示例模块和功能。在实际使用时，请根据你的具体项目需求进行相应的修改和调整。
> 
> **📝 特别提醒**: 请务必修改 `AGENT.md` 文件，将其中的示例模块名称、工具功能和业务逻辑替换为你的实际项目内容，以便 AI 代理能够正确理解和操作你的项目。

## 🚀 5分钟快速上手

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd mcp-with-mutiserver
```

### 2. 安装依赖

```bash
pip install fastmcp uvicorn
```

### 3. 运行服务器

```bash
uvicorn main:root --host 0.0.0.0 --port 8000
```

### 4. 测试连接

访问以下端点确认服务正常运行：

- http://localhost:8000/module_a/sse
- http://localhost:8000/module_a/streamable
- http://localhost:8000/module_b/sse
- http://localhost:8000/module_b/streamable

## 🔧 添加你的第一个工具

### 步骤 1: 创建新模块

```bash
mkdir -p modules/my_module/{tools,resources,prompts,examples,tests/unit,tests/integration,internal/{api,core,db}}
touch modules/my_module/{tools,resources,prompts}/__init__.py
touch modules/my_module/internal/{api,core,db}/__init__.py
touch modules/my_module/config.yaml
```

### 步骤 2: 创建服务器文件

```python
# modules/my_module/server.py
from fastmcp import FastMCP

mcp = FastMCP("My Module")

from .tools import *
from .resources import *
from .prompts import *
```

### 步骤 3: 添加工具

```python
# modules/my_module/tools/hello.py
from ..server import mcp

@mcp.tool("hello")
def hello(name: str) -> str:
    """向用户问好"""
    return f"你好，{name}！欢迎使用 MCP 多服务器模板！"
```

### 步骤 4: 更新 __init__.py

```python
# modules/my_module/tools/__init__.py
from .hello import hello

__all__ = ['hello']
```

### 步骤 5: 更新主路由

在 `main.py` 中添加：

```python
from modules.my_module.server import mcp as mcp_my

# 生成应用实例
app_my_sse = mcp_my.http_app(path="/", transport="sse")
app_my_streamable = mcp_my.http_app(path="/", transport="http")

# 在 combined_lifespan 中添加
for mcp_app in [app_a_sse, app_a_streamable, app_b_sse, app_b_streamable, 
                app_my_sse, app_my_streamable]:

# 在路由中添加
Mount("/my_module/sse", app=app_my_sse),
Mount("/my_module/streamable", app=app_my_streamable),
```

### 步骤 6: 添加内部代码（可选）

如果需要内部支持代码，可以在 `internal/` 目录中添加：

```python
# modules/my_module/internal/core/data_processing.py
def process_data(data):
    """处理数据"""
    return {"processed": data}

# modules/my_module/internal/api/client.py
def fetch_data():
    """获取数据"""
    return {"status": "success"}

# modules/my_module/internal/core/utils.py
def format_data(data):
    """格式化数据"""
    return f"processed: {data}"
```

然后在工具中使用：

```python
# modules/my_module/tools/hello.py
from ..server import mcp
from ..internal.core.data_processing import process_data

@mcp.tool("hello")
def hello(name: str) -> str:
    """向用户问好"""
    data = process_data({"name": name})
    return f"你好，{data['name']}！欢迎使用 MCP 多服务器模板！"
```

### 步骤 7: 添加测试（可选）

```python
# modules/my_module/tests/unit/test_example.py
def test_example():
    assert True

# modules/my_module/tests/integration/test_example.py
def test_example_integration():
    assert True
```

### 步骤 8: 重启服务器

```bash
uvicorn main:root --host 0.0.0.0 --port 8000 --reload
```

现在你可以访问：
- http://localhost:8000/my_module/sse
- http://localhost:8000/my_module/streamable

## 📝 常用命令

### 开发模式
```bash
uvicorn main:root --reload --host 0.0.0.0 --port 8000
```

### 生产模式
```bash
uvicorn main:root --host 0.0.0.0 --port 8000 --workers 4
```

### 指定端口
```bash
uvicorn main:root --host 0.0.0.0 --port 8001
```

### 后台运行
```bash
nohup uvicorn main:root --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

## 🔍 调试技巧

### 1. 查看日志
```bash
tail -f server.log
```

### 2. 检查端口占用
```bash
lsof -i :8000
```

### 3. 测试工具
```bash
curl -X POST http://localhost:8000/my_module/streamable \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}'
```

### 4. 热重载
使用 `--reload` 参数，代码修改后会自动重启服务器。

## 🐛 常见问题

### Q: 端口被占用怎么办？
A: 使用不同端口或停止占用端口的进程
```bash
lsof -i :8000
kill -9 <PID>
```

### Q: 导入错误怎么办？
A: 检查相对导入路径
```python
# 正确
from ..server import mcp

# 错误
from server import mcp
```

### Q: 模块找不到怎么办？
A: 确保创建了 `__init__.py` 文件
```bash
touch modules/your_module/__init__.py
```

### Q: 如何添加环境变量？
A: 创建 `.env` 文件
```bash
echo "DEBUG=True" > .env
echo "PORT=8000" >> .env
```

## 📚 下一步

1. 阅读 [开发指南](DEVELOPMENT_GUIDE.md) 了解详细技术说明
2. 查看 [README.md](../README.md) 了解项目特性
3. 探索现有模块的代码结构
4. 根据需要添加更多功能

## 🆘 获取帮助

- 查看 [故障排除](../README.md#故障排除) 部分
- 检查 [开发指南](DEVELOPMENT_GUIDE.md) 中的详细说明
- 提交 Issue 或 Pull Request

---

**提示**: 这个快速开始指南帮助你快速上手。建议在熟悉基本操作后，阅读详细的技术文档以充分利用项目功能。