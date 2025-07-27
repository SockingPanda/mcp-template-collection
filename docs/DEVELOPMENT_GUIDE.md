# MCP 多服务器开发指南

> **⚠️ 重要提示**: 这是一个基于模板项目的开发指南，包含示例代码和最佳实践。在实际使用时，请根据你的具体项目需求、技术栈和业务逻辑进行相应的修改和调整。

## 📋 目录

1. [架构概述](#架构概述)
2. [模块开发](#模块开发)
3. [工具开发](#工具开发)
4. [资源开发](#资源开发)
5. [提示开发](#提示开发)
6. [路由配置](#路由配置)
7. [测试指南](#测试指南)
8. [故障排除](#故障排除)

## 🏗️ 架构概述

### 核心组件

1. **FastMCP**: 核心 MCP 服务器框架
2. **Starlette**: ASGI 应用框架
3. **Uvicorn**: ASGI 服务器
4. **模块化设计**: 每个功能模块独立

### 数据流

```
客户端请求 → Uvicorn → Starlette → FastMCP → 模块功能 → 响应
```

## 🔧 模块开发

### 模块结构模板

```python
# modules/your_module/server.py
from fastmcp import FastMCP

mcp = FastMCP("Your Module Name")

# 导入所有功能
from .tools import *
from .resources import *
from .prompts import *

# 内部代码可以通过相对导入使用
# from .internal.data_processing import process_data
# from .internal.api_client import fetch_data
# from .internal.utils import format_data
```

### 模块命名规范

- 使用小写字母和下划线
- 名称应该描述模块功能
- 避免使用 Python 保留字

**示例**:
- ✅ `math_operations`
- ✅ `text_processing`
- ❌ `math` (可能冲突)
- ❌ `import` (保留字)

### 模块目录结构

每个模块应包含以下目录：

- **tools/**: 公开的工具函数
- **resources/**: 公开的资源
- **prompts/**: 公开的提示
- **internal/**: 私有的内部代码（可选，可根据需要自定义）

## 🛠️ 工具开发

### 工具装饰器语法

```python
@mcp.tool("tool_name")
def tool_function(param1: type, param2: type) -> return_type:
    """工具描述"""
    # 实现逻辑
    return result
```

### 参数类型支持

- **基本类型**: `str`, `int`, `float`, `bool`
- **复杂类型**: `list`, `dict`, `Optional`, `Union`
- **自定义类型**: 需要实现序列化

### 工具开发最佳实践

1. **单一职责**: 每个工具只做一件事
2. **类型注解**: 提供完整的类型信息
3. **文档字符串**: 清晰描述功能和参数
4. **错误处理**: 优雅处理异常情况
5. **日志记录**: 记录重要操作

### 示例工具

```python
from typing import List, Optional
from ..server import mcp
from ..internal.data_processing import process_data
from ..internal.api_client import fetch_data

@mcp.tool("calculate_average")
def calculate_average(numbers: List[float]) -> float:
    """计算数字列表的平均值"""
    if not numbers:
        raise ValueError("数字列表不能为空")
    return sum(numbers) / len(numbers)

@mcp.tool("format_text")
def format_text(text: str, uppercase: bool = False) -> str:
    """格式化文本"""
    # 使用内部数据处理
    processed_text = process_data({"text": text, "uppercase": uppercase})
    result = processed_text["text"].strip()
    if uppercase:
        result = result.upper()
    return result
```

## 📦 资源开发

### 资源装饰器语法

```python
@mcp.resource("resource_path/{param_name}")
def resource_function(param_name: str) -> str:
    """资源描述"""
    return resource_content
```

### URI 模板规则

- 必须包含至少一个参数
- 参数用 `{param_name}` 格式
- 参数名要与函数参数匹配
- 支持路径参数和查询参数

### 资源类型

1. **静态资源**: 返回固定内容
2. **动态资源**: 根据参数返回不同内容
3. **计算资源**: 执行计算后返回结果

### 示例资源

```python
from ..server import mcp
from ..internal.api_client import fetch_data
from ..internal.utils import format_data

@mcp.resource("user/{user_id}")
def get_user_profile(user_id: str) -> str:
    """获取用户配置文件"""
    # 使用内部 API 客户端获取数据
    user_data = fetch_data()
    return f"用户 {user_id} 的配置文件"

@mcp.resource("config/{config_name}")
def get_config(config_name: str) -> str:
    """获取配置信息"""
    configs = {
        "database": "数据库配置信息",
        "api": "API 配置信息",
        "security": "安全配置信息"
    }
    # 使用内部工具函数格式化
    return format_data(configs.get(config_name, "配置不存在"))
```

## 🔧 内部代码开发

### 内部代码结构

每个模块的 `internal/` 目录包含私有代码，用于支持公开的工具、资源和提示。内部文件可根据模块需求自定义：

```
internal/
├── __init__.py           # 包初始化
├── data_processing.py    # 数据处理逻辑（可选）
├── api_client.py         # API 客户端（可选）
├── utils.py              # 内部工具函数（可选）
└── ...                   # 其他自定义文件
```

### 内部代码使用原则

1. **私有性**: `internal/` 目录中的代码不直接暴露给外部
2. **支持性**: 内部代码用于支持公开接口的功能
3. **可重用性**: 内部函数应该可以在多个公开接口中重用
4. **简洁性**: 保持内部代码简洁，专注于核心功能
5. **灵活性**: 内部文件结构可根据模块需求自定义

### 内部代码示例

```python
# internal/data_processing.py（可选）
def process_data(data):
    """处理数据"""
    return {"processed": data}

# internal/api_client.py（可选）
def fetch_data():
    """获取外部数据"""
    return {"status": "success", "data": []}

# internal/utils.py（可选）
def format_data(data):
    """格式化数据"""
    return f"processed: {data}"

# 其他自定义文件示例
# internal/database.py
def get_db_connection():
    """数据库连接"""
    pass

# internal/cache.py
def cache_data(key, value):
    """缓存数据"""
    pass
```

### 在公开接口中使用内部代码

```python
# tools/your_tool.py
from ..server import mcp
from ..internal.data_processing import process_data
from ..internal.api_client import fetch_data

@mcp.tool("process_external_data")
def process_external_data() -> str:
    """处理外部数据"""
    # 获取数据
    raw_data = fetch_data()
    # 处理数据
    processed_data = process_data(raw_data)
    return f"处理完成: {processed_data}"
```

## 💬 提示开发

### 提示装饰器语法

```python
@mcp.prompt("prompt_name")
def prompt_function(text: str) -> str:
    """提示描述"""
    return prompt_template
```

### 提示设计原则

1. **可重用性**: 设计通用的提示模板
2. **参数化**: 使用参数使提示灵活
3. **清晰性**: 提示应该清晰易懂
4. **一致性**: 保持提示风格一致

### 示例提示

```python
from ..server import mcp
from ..internal.data_processing import process_data

@mcp.prompt("summarize")
def summarize_text(text: str) -> str:
    """生成文本摘要"""
    # 使用内部数据处理
    processed_text = process_data({"text": text})
    return f"请用简洁的语言总结以下内容：\n\n{processed_text['text']}"

@mcp.prompt("translate")
def translate_text(text: str, target_language: str = "英文") -> str:
    """翻译文本"""
    return f"请将以下文本翻译成{target_language}：\n\n{text}"

@mcp.prompt("analyze")
def analyze_text(text: str, analysis_type: str = "情感") -> str:
    """分析文本"""
    return f"请对以下文本进行{analysis_type}分析：\n\n{text}"
```

## 🛣️ 路由配置

### 主路由文件结构

```python
# main.py
from fastmcp import FastMCP
from contextlib import AsyncExitStack, asynccontextmanager
from starlette.applications import Starlette
from starlette.routing import Mount

# 导入模块
from modules.module_a.server import mcp as mcp_a
from modules.module_b.server import mcp as mcp_b

# 生成应用实例
app_a_sse = mcp_a.http_app(path="/", transport="sse")
app_a_streamable = mcp_a.http_app(path="/", transport="http")

# 统一生命周期管理
@asynccontextmanager
async def combined_lifespan(app):
    async with AsyncExitStack() as stack:
        for mcp_app in [app_a_sse, app_a_streamable]:
            if mcp_app.lifespan:
                await stack.enter_async_context(mcp_app.lifespan(app))
        yield

# 路由配置
root = Starlette(
    routes=[
        Mount("/module_a/sse", app=app_a_sse),
        Mount("/module_a/streamable", app=app_a_streamable),
    ],
    lifespan=combined_lifespan
)
```

### 传输类型

1. **SSE (Server-Sent Events)**: 单向实时通信
2. **HTTP Streamable**: 双向流式通信

### 路由命名规范

- 使用模块名作为路径前缀
- 区分传输类型 (sse/streamable)
- 保持路径简洁明了

## 🧪 测试指南

### 单元测试

```python
# test_module_a.py
import pytest
from modules.module_a.tools.math import add, subtract

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(1, 1) == 0
```

### 集成测试

```python
# test_integration.py
import pytest
from fastapi.testclient import TestClient
from main import root

client = TestClient(root)

def test_module_a_sse():
    response = client.get("/module_a/sse")
    assert response.status_code == 200

def test_module_a_tools():
    response = client.post("/module_a/streamable", json={
        "method": "tools/list"
    })
    assert response.status_code == 200
```

### 测试最佳实践

1. **测试覆盖**: 覆盖所有公共接口
2. **边界测试**: 测试边界条件和异常情况
3. **性能测试**: 测试响应时间和吞吐量
4. **集成测试**: 测试模块间交互

## 🔍 故障排除

### 常见问题

#### 1. 导入错误

**问题**: `ModuleNotFoundError: No module named 'server'`

**解决方案**: 使用相对导入
```python
# 错误
from server import mcp

# 正确
from ..server import mcp
```

#### 2. URI 模板错误

**问题**: `ValueError: URI template must contain at least one parameter`

**解决方案**: 确保资源 URI 包含参数
```python
# 错误
@mcp.resource("profile")

# 正确
@mcp.resource("profile/{id}")
```

#### 3. 循环导入

**问题**: 模块间相互导入导致循环依赖

**解决方案**: 
- 使用相对导入
- 重构代码结构
- 使用延迟导入

#### 4. 端口冲突

**问题**: 端口已被占用

**解决方案**:
```bash
# 查看端口占用
lsof -i :8000

# 使用不同端口
uvicorn main:root --port 8001
```

### 调试技巧

1. **日志记录**: 添加详细的日志输出
2. **断点调试**: 使用 `pdb` 或 IDE 调试器
3. **热重载**: 开发时使用 `--reload` 参数
4. **健康检查**: 实现健康检查端点

## 📚 高级用法

### 自定义中间件

```python
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

root = Starlette(
    routes=[...],
    middleware=[
        Middleware(CORSMiddleware, allow_origins=["*"])
    ]
)
```

### 环境配置

```python
import os
from dotenv import load_dotenv

load_dotenv()

# 使用环境变量
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
PORT = int(os.getenv("PORT", "8000"))
```

### 性能优化

1. **异步处理**: 使用 `async/await`
2. **连接池**: 复用数据库连接
3. **缓存**: 缓存频繁访问的数据
4. **负载均衡**: 使用多个工作进程

---

**提示**: 这个开发指南提供了详细的技术说明和最佳实践。建议在开发过程中经常参考此文档。

## 📝 指南定制建议

### 需要根据实际项目调整的内容：

1. **技术栈**: 
   - 根据实际使用的技术栈调整架构说明
   - 更新依赖和版本要求
   - 调整性能优化建议

2. **代码示例**: 
   - 将示例代码替换为实际业务逻辑
   - 更新工具、资源和提示的具体实现
   - 调整错误处理和日志记录策略

3. **最佳实践**: 
   - 根据实际项目需求调整开发规范
   - 更新测试策略和部署方法
   - 调整安全性和性能考虑

4. **故障排除**: 
   - 根据实际项目经验更新常见问题
   - 调整调试技巧和解决方案
   - 更新性能监控方法

### 建议的定制步骤：

1. 理解开发指南的整体结构
2. 识别需要替换的示例内容
3. 根据实际技术栈和业务需求进行定制
4. 测试定制后的开发流程
5. 定期更新指南以反映项目演进 