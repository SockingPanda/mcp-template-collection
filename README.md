# MCP 多服务器模板项目

> **⚠️ 重要提示**: 这是一个模板项目，包含示例模块和功能。在实际使用时，请根据你的具体项目需求、业务逻辑和功能要求进行相应的修改和定制。
> 
> **📝 特别提醒**: 请务必修改 `AGENT.md` 文件，将其中的示例模块名称、工具功能和业务逻辑替换为你的实际项目内容，以便 AI 代理能够正确理解和操作你的项目。

这是一个基于 FastMCP 的多服务器 MCP (Model Context Protocol) 模板项目，旨在提供一个可扩展的框架来构建和管理多个 MCP 服务器。

## 🚀 项目特性

- **模块化设计**: 每个功能模块独立，便于维护和扩展
- **多服务器支持**: 支持同时运行多个 MCP 服务器
- **统一路由**: 通过单一入口点管理所有服务器
- **灵活传输**: 支持 SSE 和 HTTP 流式传输
- **完整示例**: 包含工具、资源和提示的完整示例

## 📁 项目结构

```
mcp-with-mutiserver/
├── main.py                 # 主入口文件，统一路由管理
├── modules/                # 模块目录
│   ├── module_a/          # 模块 A (数学工具示例)
│   │   ├── server.py      # 模块 A 的 MCP 服务器
│   │   ├── config.yaml    # 模块配置文件
│   │   ├── tools/         # 公开的工具
│   │   │   ├── __init__.py
│   │   │   └── math.py    # 数学工具 (add, subtract)
│   │   ├── resources/     # 公开的资源
│   │   │   ├── __init__.py
│   │   │   └── profile.py # 配置文件资源
│   │   ├── prompts/       # 公开的提示
│   │   │   ├── __init__.py
│   │   │   └── summary.py # 总结提示
│   │   ├── examples/      # 使用示例
│   │   ├── tests/         # 单元与集成测试
│   │   │   ├── unit/
│   │   │   └── integration/
│   │   └── internal/      # 私有的内部代码
│   │       ├── __init__.py
│   │       ├── api/       # API 客户端
│   │       │   └── client.py
│   │       ├── core/      # 核心逻辑与工具函数
│   │       │   ├── data_processing.py
│   │       │   └── utils.py
│   │       └── db/        # 数据库与缓存
│   └── module_b/          # 模块 B (文本工具示例)
│       ├── server.py      # 模块 B 的 MCP 服务器
│       ├── config.yaml    # 模块配置文件
│       ├── tools/         # 公开的工具
│       │   ├── __init__.py
│       │   └── text.py    # 文本工具 (reverse, uppercase, word_count)
│       ├── resources/     # 公开的资源
│       │   ├── __init__.py
│       │   └── items.py   # 项目资源
│       ├── prompts/       # 公开的提示
│       │   ├── __init__.py
│       │   └── summary.py # 总结提示
│       ├── examples/      # 使用示例
│       ├── tests/         # 单元与集成测试
│       │   ├── unit/
│       │   └── integration/
│       └── internal/      # 私有的内部代码
│           ├── __init__.py
│           ├── api/       # API 客户端
│           │   └── client.py
│           ├── core/      # 核心逻辑与工具函数
│           │   ├── data_processing.py
│           │   └── utils.py
│           └── db/        # 数据库与缓存
├── docs/                  # 文档目录
│   ├── QUICKSTART.md      # 快速开始指南
│   ├── DEVELOPMENT_GUIDE.md # 开发指南
│   └── CHANGELOG.md       # 变更日志
└── requirements.txt       # 项目依赖
```

## 🛠️ 快速开始

### 1. 安装依赖

```bash
pip install fastmcp uvicorn
```

### 2. 运行服务器

```bash
uvicorn main:root --host 0.0.0.0 --port 8000
```

### 3. 访问端点

- **模块 A SSE**: `http://localhost:8000/module_a/sse`
- **模块 A HTTP**: `http://localhost:8000/module_a/streamable`
- **模块 B SSE**: `http://localhost:8000/module_b/sse`
- **模块 B HTTP**: `http://localhost:8000/module_b/streamable`

## 🔧 如何扩展新模块

### 步骤 1: 创建新模块目录

```bash
mkdir -p modules/your_module/{tools,resources,prompts,examples,tests/unit,tests/integration,internal/{api,core,db}}
touch modules/your_module/{tools,resources,prompts}/__init__.py
touch modules/your_module/internal/{api,core,db}/__init__.py
touch modules/your_module/config.yaml
```

### 步骤 2: 创建服务器文件

在 `modules/your_module/server.py` 中：

```python
from fastmcp import FastMCP

mcp = FastMCP("Your Module Name")

# 导入所有功能
from .tools import *
from .resources import *
from .prompts import *
```

### 步骤 3: 添加工具

在 `modules/your_module/tools/your_tool.py` 中：

```python
from ..server import mcp

@mcp.tool("your_tool_name")
def your_tool(param1: str, param2: int) -> str:
    """工具描述"""
    # 工具实现
    return f"Result: {param1} {param2}"
```

在 `modules/your_module/tools/__init__.py` 中：

```python
from .your_tool import your_tool

__all__ = ['your_tool']
```

### 步骤 4: 添加资源

在 `modules/your_module/resources/your_resource.py` 中：

```python
from ..server import mcp

@mcp.resource("your_resource/{id}")
def your_resource(id: str) -> str:
    """资源描述"""
    return f"Resource {id} from Your Module"
```

在 `modules/your_module/resources/__init__.py` 中：

```python
from .your_resource import your_resource

__all__ = ['your_resource']
```

### 步骤 5: 添加提示

在 `modules/your_module/prompts/your_prompt.py` 中：

```python
from ..server import mcp

@mcp.prompt("your_prompt")
def your_prompt(text: str) -> str:
    """提示描述"""
    return f"Your prompt template: {text}"
```

在 `modules/your_module/prompts/__init__.py` 中：

```python
from .your_prompt import your_prompt

__all__ = ['your_prompt']
```

### 步骤 6: 更新主路由

在 `main.py` 中添加新模块：

```python
from modules.your_module.server import mcp as mcp_your

# 为你的模块生成 ASGI 应用实例
app_your_sse = mcp_your.http_app(path="/", transport="sse")
app_your_streamable = mcp_your.http_app(path="/", transport="http")

# 在 combined_lifespan 中添加
for mcp_app in [app_a_sse, app_a_streamable, app_b_sse, app_b_streamable, 
                app_your_sse, app_your_streamable]:

# 在路由中添加
Mount("/your_module/sse", app=app_your_sse),
Mount("/your_module/streamable", app=app_your_streamable),
```

## 📝 最佳实践

### 1. 模块命名
- 使用描述性的模块名称
- 保持目录结构一致
- 每个模块专注于特定功能领域

### 2. 工具设计
- 提供清晰的函数文档
- 使用类型注解
- 保持工具功能单一

### 3. 资源设计
- URI 模板必须包含参数 `{param_name}`
- 参数名要与函数参数匹配
- 提供有意义的资源描述

### 4. 提示设计
- 创建可重用的提示模板
- 使用清晰的参数名
- 提供示例用法

### 5. 导入管理
- 在 `__init__.py` 中导出所有公共接口
- 使用相对导入避免循环依赖
- 保持导入结构清晰

## 🔍 示例模块说明

### Module A (数学工具)
- **工具**: `add`, `subtract` - 基础数学运算
- **资源**: `profile/{id}` - 配置文件资源
- **提示**: `summary` - 3句话总结

### Module B (文本工具)
- **工具**: `reverse`, `uppercase`, `word_count` - 文本处理
- **资源**: `details/{id}` - 项目详情资源
- **提示**: `summary` - 2句话概述

## 🚀 部署建议

### 开发环境
```bash
uvicorn main:root --reload --host 0.0.0.0 --port 8000
```

### 生产环境
```bash
uvicorn main:root --host 0.0.0.0 --port 8000 --workers 4
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📝 项目文档

- [AGENT.md](AGENT.md) - AI代理操作指南
- [docs/QUICKSTART.md](docs/QUICKSTART.md) - 快速开始指南
- [docs/DEVELOPMENT_GUIDE.md](docs/DEVELOPMENT_GUIDE.md) - 详细开发指南
- [docs/CHANGELOG.md](docs/CHANGELOG.md) - 版本历史和变更记录

## 🙏 致谢

- [FastMCP](https://github.com/fastmcp/fastmcp) - 提供 MCP 服务器框架
- [Uvicorn](https://github.com/encode/uvicorn) - ASGI 服务器

---

**注意**: 这是一个模板项目，旨在帮助您快速构建多服务器 MCP 应用。请根据您的具体需求进行定制和扩展。

## 📝 项目定制要点

**重要**: 使用此模板项目时，请务必：

1. **修改 `AGENT.md`** - 更新示例模块名称和功能，让 AI 代理正确理解你的项目
2. **替换示例模块** - 将 `module_a`、`module_b` 替换为实际业务模块
3. **调整配置** - 根据部署环境更新端口、域名等配置
4. **更新依赖** - 根据实际技术栈调整 `requirements.txt` 
5. **查看变更历史** - 参考 [CHANGELOG.md](docs/CHANGELOG.md) 了解项目的演进历程 