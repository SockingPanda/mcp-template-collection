# MCP 多服务器项目 - AI 代理指南

## 🤖 代理概述

这是一个基于 FastMCP 的多服务器 MCP (Model Context Protocol) 模板项目。作为 AI 代理，你可以通过以下方式与项目交互：

### 项目特性
- **模块化设计**: 每个功能模块独立，便于维护和扩展
- **多服务器支持**: 支持同时运行多个 MCP 服务器
- **统一路由**: 通过单一入口点管理所有服务器
- **灵活传输**: 支持 SSE 和 HTTP 流式传输

## 📁 项目结构理解

```
mcp-template-collection/
├── main.py                 # 主入口文件，统一路由管理
├── modules/                # 模块目录
│   ├── module_a/          # 数学工具模块
│   │   ├── server.py      # 模块 A 的 MCP 服务器
│   │   ├── tools/         # 公开的工具 (add, subtract)
│   │   ├── resources/     # 公开的资源 (profile)
│   │   ├── prompts/       # 公开的提示 (summary)
│   │   └── internal/      # 私有的内部代码
│   └── module_b/          # 文本工具模块
│       ├── server.py      # 模块 B 的 MCP 服务器
│       ├── tools/         # 公开的工具 (reverse, uppercase, word_count)
│       ├── resources/     # 公开的资源 (items)
│       ├── prompts/       # 公开的提示 (summary)
│       └── internal/      # 私有的内部代码
├── docs/                  # 文档目录
└── requirements.txt       # 项目依赖
```

## 🛠️ 常用操作指南

### 1. 启动服务器
```bash
# 开发模式（支持热重载）
uvicorn main:root --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn main:root --host 0.0.0.0 --port 8000 --workers 4
```

### 2. 访问端点
- **模块 A SSE**: `http://localhost:8000/module_a/sse`
- **模块 A HTTP**: `http://localhost:8000/module_a/streamable`
- **模块 B SSE**: `http://localhost:8000/module_b/sse`
- **模块 B HTTP**: `http://localhost:8000/module_b/streamable`

### 3. 测试工具功能
```bash
# 测试模块 A 的数学工具
curl -X POST http://localhost:8000/module_a/streamable \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "add", "arguments": {"a": 5, "b": 3}}}'

# 测试模块 B 的文本工具
curl -X POST http://localhost:8000/module_b/streamable \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "reverse", "arguments": {"text": "Hello World"}}}'
```

## 🔧 开发新模块的步骤

### 步骤 1: 创建模块目录结构
```bash
mkdir -p modules/new_module/{tools,resources,prompts,internal}
touch modules/new_module/{tools,resources,prompts,internal}/__init__.py
```

### 步骤 2: 创建服务器文件
```python
# modules/new_module/server.py
from fastmcp import FastMCP

mcp = FastMCP("New Module")

from .tools import *
from .resources import *
from .prompts import *
```

### 步骤 3: 添加工具
```python
# modules/new_module/tools/example.py
from ..server import mcp

@mcp.tool("example_tool")
def example_tool(param: str) -> str:
    """示例工具"""
    return f"处理结果: {param}"
```

### 步骤 4: 更新 __init__.py
```python
# modules/new_module/tools/__init__.py
from .example import example_tool

__all__ = ['example_tool']
```

### 步骤 5: 更新主路由 (main.py)
```python
# 在 main.py 中添加
from modules.new_module.server import mcp as mcp_new

# 生成应用实例
app_new_sse = mcp_new.http_app(path="/", transport="sse")
app_new_streamable = mcp_new.http_app(path="/", transport="http")

# 在 combined_lifespan 中添加
for mcp_app in [app_a_sse, app_a_streamable, app_b_sse, app_b_streamable, 
                app_new_sse, app_new_streamable]:

# 在路由中添加
Mount("/new_module/sse", app=app_new_sse),
Mount("/new_module/streamable", app=app_new_streamable),
```

## 📝 代码规范

### 工具开发规范
- 使用 `@mcp.tool("tool_name")` 装饰器
- 提供完整的类型注解
- 编写清晰的文档字符串
- 保持功能单一

### 资源开发规范
- 使用 `@mcp.resource("path/{param}")` 装饰器
- URI 模板必须包含参数
- 参数名要与函数参数匹配

### 提示开发规范
- 使用 `@mcp.prompt("prompt_name")` 装饰器
- 设计可重用的提示模板
- 使用参数化设计

## 🔍 调试和故障排除

### 常见问题解决

1. **端口被占用**
```bash
lsof -i :8000
kill -9 <PID>
```

2. **导入错误**
```python
# 使用相对导入
from ..server import mcp
```

3. **模块找不到**
```bash
# 确保创建了 __init__.py 文件
touch modules/your_module/__init__.py
```

### 调试技巧
- 使用 `--reload` 参数进行热重载
- 查看服务器日志
- 使用 curl 测试端点

## 📚 相关文档

- [README.md](README.md) - 项目概述和特性
- [docs/QUICKSTART.md](docs/QUICKSTART.md) - 快速开始指南
- [docs/DEVELOPMENT_GUIDE.md](docs/DEVELOPMENT_GUIDE.md) - 详细开发指南

## 🎯 最佳实践建议

### 作为 AI 代理，你应该：

1. **理解模块化设计**: 每个模块都是独立的，可以单独开发和测试
2. **遵循命名规范**: 使用描述性的模块和工具名称
3. **保持代码简洁**: 每个工具只做一件事
4. **提供完整文档**: 为每个工具编写清晰的文档字符串
5. **测试功能**: 在开发新功能后，使用 curl 或其他工具测试
6. **使用相对导入**: 避免循环导入问题
7. **遵循目录结构**: 保持项目结构的一致性

### 开发新功能时的检查清单：

- [ ] 创建了正确的目录结构
- [ ] 添加了 `__init__.py` 文件
- [ ] 使用了正确的装饰器
- [ ] 提供了类型注解
- [ ] 编写了文档字符串
- [ ] 更新了主路由文件
- [ ] 测试了功能是否正常工作

---

**注意**: 这个指南帮助 AI 代理更好地理解和操作 MCP 多服务器项目。请根据具体需求调整和扩展功能。 