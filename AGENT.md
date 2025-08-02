# MCP 多服务器项目 - AI 代理指南

> **⚠️ 重要提示**: 这是一个示例文档，基于当前项目的模板结构编写。在实际使用时，请根据你的具体项目需求、模块功能和业务逻辑进行相应的修改和调整。

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
│   ├── common/             # 公共内部代码
│   │   ├── core/           # 核心共享逻辑
│   │   ├── db/             # 数据库与缓存封装
│   │   └── tests/          # 公共测试
│   ├── module_a/          # 数学工具模块
│   │   ├── server.py      # 模块 A 的 MCP 服务器
│   │   ├── config.yaml    # 模块配置文件
│   │   ├── tools/         # 公开的工具 (add, subtract)
│   │   ├── resources/     # 公开的资源 (profile)
│   │   ├── prompts/       # 公开的提示 (summary)
│   │   ├── examples/      # 使用示例
│   │   ├── tests/         # 单元与集成测试
│   │   │   ├── unit/      # 单元测试
│   │   │   └── integration/ # 集成测试
│   │   └── internal/      # 私有的内部代码
│   │       ├── api/       # API 客户端
│   │       ├── core/      # 核心逻辑与工具函数
│   │       └── db/        # 数据库与缓存
│   └── module_b/          # 文本工具模块
│       ├── server.py      # 模块 B 的 MCP 服务器
│       ├── config.yaml    # 模块配置文件
│       ├── tools/         # 公开的工具 (reverse, uppercase, word_count)
│       ├── resources/     # 公开的资源 (items)
│       ├── prompts/       # 公开的提示 (summary)
│       ├── examples/      # 使用示例
│       ├── tests/         # 单元与集成测试
│       │   ├── unit/      # 单元测试
│       │   └── integration/ # 集成测试
│       └── internal/      # 私有的内部代码
│           ├── api/       # API 客户端
│           ├── core/      # 核心逻辑与工具函数
│           └── db/        # 数据库与缓存
├── docs/                  # 文档目录
└── requirements.txt       # 项目依赖
```

上述结构中：
- `common/` 目录用于存放跨模块共享的内部代码，并附带相应的测试。
- `config.yaml` 存放模块级配置，可根据环境调整参数。
- `examples/` 提供工具和资源的调用示例，便于快速参考。
- `tests/` 目录包含 `unit/` 与 `integration/` 子目录，分别用于单元测试和集成测试。
- `internal/` 现拆分为 `api/`、`core/` 和 `db/`，使 API 客户端、核心逻辑和数据库代码解耦。

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
- [docs/CHANGELOG.md](docs/CHANGELOG.md) - 代码、文档和开发流程的历史变更记录

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

## 📝 文档定制建议

### 需要根据实际项目调整的内容：

1. **模块名称和功能**: 
   - 将 `module_a`、`module_b` 替换为实际模块名
   - 更新工具、资源和提示的具体功能描述

2. **端点 URL**: 
   - 根据实际部署环境调整端口号
   - 更新域名和路径

3. **工具示例**: 
   - 替换为实际项目的工具功能
   - 更新参数和返回值类型

4. **业务逻辑**: 
   - 根据实际业务需求调整开发流程
   - 更新代码规范和最佳实践

5. **测试命令**: 
   - 根据实际工具更新测试用例
   - 调整 curl 命令的参数

### 建议的定制步骤：

1. 阅读整个文档，理解结构
2. 识别需要替换的示例内容
3. 根据实际项目功能进行替换
4. 测试更新后的指南是否准确
5. 定期更新文档以反映项目变化 

## 🛡️ 模块修改规则

为保证项目结构和功能的稳定性、可维护性，进行模块（如 module_a、module_b 等）修改时，请遵循以下规范：

### 1. 兼容性优先
- **避免破坏性变更**：如需更改接口、参数、返回值等，优先考虑向后兼容，必要时保留旧接口一段时间。
- **如需重构或删除功能**，请在文档和代码中明确标注“已废弃/即将移除”，并在CHANGELOG或文档中说明影响范围。

### 2. 变更流程
- **先本地测试**：所有修改应在本地充分测试，确保不影响其他模块和主流程。
- **同步更新文档**：每次修改后，务必同步更新相关文档（README、AGENT、QUICKSTART、DEVELOPMENT_GUIDE），并在文档中注明“已更新至最新结构”。
- **代码注释**：对重要变更、兼容性处理、临时方案等，需在代码中写明注释，便于后续维护。

### 3. 代码规范
- **保持风格一致**：遵循项目既有的代码风格和目录结构。
- **类型注解与文档字符串**：新增或修改的函数、类、接口等，需补全类型注解和 docstring。
- **导入管理**：如有新增/删除/重命名的工具、资源、提示，务必同步维护各自的 `__init__.py`。

### 4. 回滚与审查
- **建议使用分支开发**，合并前由团队成员或AI代理进行代码审查。
- **如发现问题，优先回滚到上一个稳定版本**，并在文档中记录问题与解决方案。

### 5. 变更记录
- **维护CHANGELOG**：每次重要修改需在CHANGELOG或文档中记录变更内容、影响范围和升级建议。

---

## 🔄 提交与协作流程

为保证项目质量和团队协作效率，所有代码和文档的提交请遵循以下流程：

### 1. 分支管理
- **主分支（main/master）**：仅用于存放稳定、可部署的代码。
- **功能分支（feature/xxx）**：每个新功能、修复或文档更新建议在独立分支上开发，命名如 `feature/module_a-api`、`fix/typo-in-readme`。
- **合并请求（Pull Request, PR）**：开发完成后通过 PR 合并到主分支，禁止直接在主分支上推送代码。

### 2. 提交规范
- **原子提交**：每次提交只做一件事，便于回滚和追踪。
- **提交信息格式**：
  - 推荐格式：
    - **单行标题**（类型+简要描述）
    - **空一行**
    - **条目式详细说明**（如有多项变更，建议每项用 `-` 开头单独列出）
    
    **示例：**
    ```
    feat: 新增module_a加法工具

    - 实现 add 工具函数，支持两个参数相加
    - 增加 add 工具的类型注解和文档字符串
    - 在 tools/__init__.py 中导出 add
    - 补充 add 工具的单元测试
    ```
  - **type 类型建议**：
    - feat: 新功能
    - fix: 修复bug
    - docs: 文档变更
    - style: 代码格式（不影响功能，如空格、分号等）
    - refactor: 重构（即不是新增功能，也不是修复bug）
    - test: 增加或修改测试
    - chore: 构建过程或辅助工具的变动
    - perf: 性能优化
    - revert: 回滚提交
  - **更多示例**：
    - `fix: 修复module_a资源导入bug`
    - `docs: 完善AGENT.md模块开发流程`
    - `refactor: 优化module_b主路由注册逻辑`
    - `test: 增加module_a工具单元测试`
    - `chore: 升级依赖fastmcp到1.2.0`
    - `revert: 回滚feature/module_a-api相关提交`
- **关联Issue/任务**：如有相关Issue或任务编号，请在提交信息或PR描述中注明。

### 3. 代码评审
- **自查**：提交前自测功能、检查代码风格、确保无明显bug。
- **团队/AI代理评审**：PR需由至少一名团队成员或AI代理审核通过后方可合并。
- **评审内容**：关注代码规范、兼容性、文档同步、潜在风险等。

### 4. 合并与发布
- **Squash合并**：推荐使用Squash合并，保持主分支提交历史简洁。
- **合并后同步**：合并后如有依赖变更、数据库迁移等，需在PR或CHANGELOG中说明。
- **发布标签**：重要版本发布时，建议打Tag并在CHANGELOG中记录。

### 5. 文档同步
- **每次合并/发布**：务必同步更新相关文档（README、AGENT、QUICKSTART、DEVELOPMENT_GUIDE、CHANGELOG等）。
- **文档PR**：文档更新也建议单独PR，便于追踪和回滚。 

## 🗒️ CHANGELOG 维护规范

为便于团队追踪项目历史变更，所有代码和文档的重要修改都应记录在 docs/CHANGELOG.md 中。请遵循以下规范：

### 1. 记录内容
- 每次重要功能、接口、修复、重构、依赖升级等变更，均需在 docs/CHANGELOG.md 中记录。
- 文档结构、开发流程等相关调整，也请同步记录在 docs/CHANGELOG.md。

### 2. 格式要求
- 按时间倒序分段，建议以版本号或日期为标题。
- **必须使用实际的当前日期**，不要使用过去或未来的日期。
- 每条变更简明扼要，必要时可分条列出。
- 推荐格式：
  ```
  ## [1.2.0] - 2024-07-01
  ### Added
  - 新增 module_b 文本反转工具
  - 增加主路由统一生命周期管理

  ### Changed
  - 优化 module_a 加法工具性能

  ### Fixed
  - 修复 module_b 资源导入路径错误
  ```
  **注意**: 上述日期应该是实际的当前日期，不是示例中写死的日期。
- 也可采用更简洁的日期分段：
  ```
  ### 2024-07-01
  - 新增 module_a/subtract 工具
  - 更新 AGENT.md 协作流程
  ```
  **注意**: 请始终使用实际的当前日期，不要复制示例中的日期。

### 3. 更新时机
- 每次合并 PR、发布新版本、重要文档调整后，**务必同步更新 docs/CHANGELOG.md**。
- 如有多人协作，建议由合并人或负责人统一补充。

### 4. 协作建议
- 变更内容应与实际提交、PR描述保持一致。
- 重要 breaking change、废弃接口等需特别标注。
- docs/CHANGELOG.md 也建议通过 PR 方式维护，便于团队审阅和追溯。

### 5. 版本号管理规范
- 推荐采用 [语义化版本（Semantic Versioning, SemVer）](https://semver.org/lang/zh-CN/) 进行版本号管理，格式为 `主版本号.次版本号.修订号`（如 1.2.0）。
- 变更规则：
  - **主版本号**（X.y.z）：有不兼容的 API 变更、大型重构或重大功能发布时递增。
  - **次版本号**（x.Y.z）：向下兼容地新增功能时递增。
  - **修订号**（x.y.Z）：向下兼容地修复 bug 或小幅优化时递增。
- 每次发布新版本、合并重要功能或修复时，请在 docs/CHANGELOG.md 中同步更新版本号。
- 版本号应与实际发布的 tag、PR 标题等保持一致。
- 示例：
  ```
  ## [2.0.0] - 2024-07-01
  - 重构主路由，移除旧接口，新增统一认证模块

  ## [1.3.0] - 2024-06-15
  - 新增 module_c 及相关工具

  ## [1.2.1] - 2024-06-01
  - 修复 module_b 工具参数校验 bug
  ```
  **重要**: 在实际使用中，请始终使用真实的日期，最新版本应使用当前日期，而不是复制示例中的日期。

--- 