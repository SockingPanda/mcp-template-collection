# MCP 模板项目 - AI 代理操作框架

> 本文档为 AI 代理提供在本仓库中协作的通用流程与约定。具体模块实现、功能说明和目录细节请参阅 `README.md`。

## 🧱 项目架构
- 基于 **FastMCP 多服务器** 模式，`main.py` 统一挂载各模块路由
- `modules/common` 提供共享的数据库适配器与通用逻辑
- 各业务模块（`module_a`、`module_b`）遵循一致目录结构，可独立开发与部署

## 🛠 技术栈
- Python ≥ 3.11
- [FastMCP](https://github.com/fastmcp/fastmcp)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)（可选数据库层）

## 📁 通用目录约定
```
mcp-template-collection/
├── main.py                     # 入口，组合所有 MCP 服务器
├── modules/
│   ├── common/                 # 共享组件（数据库与核心逻辑）
│   ├── module_a/               # 示例模块 A
│   └── module_b/               # 示例模块 B
├── docs/                       # 文档目录
└── requirements.txt            # 依赖声明
```

单个模块的标准目录：

```
modules/<module>/
├── server.py           # MCP 服务器定义
├── config.yaml         # 模块配置（可选）
├── tools/              # 对外工具
├── resources/          # 对外资源
├── prompts/            # 对外提示
├── examples/           # 使用示例
├── tests/
│   ├── unit/           # 单元测试
│   └── integration/    # 集成测试
└── internal/           # 私有实现
    ├── api/            # 外部 API 客户端
    ├── core/           # 业务逻辑与工具函数
    └── db/             # 数据库与缓存封装
```

## 🚀 常用操作
### 启动服务器
```bash
# 开发模式
uvicorn main:root --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn main:root --host 0.0.0.0 --port 8000 --workers 4
```

### 访问端点
任意模块在路由前缀 `<name>` 下暴露 SSE 与 HTTP 两种传输方式：
- `http://localhost:8000/<name>/sse`
- `http://localhost:8000/<name>/streamable`

### 测试示例
```bash
curl -X POST http://localhost:8000/<name>/streamable \
  -H "Content-Type: application/json" \
  -d '{"method":"tools/call","params":{"name":"tool_name","arguments":{}}}'
```

### 运行测试
```bash
pytest -q
```

## 🛠️ 开发新模块
1. **创建目录结构**
    ```bash
    mkdir -p modules/your_module/{tools,resources,prompts,examples,tests/{unit,integration},internal/{api,core,db}}
    touch modules/your_module/{tools,resources,prompts}/__init__.py
    touch modules/your_module/internal/{api,core,db}/__init__.py
    touch modules/your_module/config.yaml
    ```
2. **编写服务器文件**
    ```python
    # modules/your_module/server.py
    from fastmcp import FastMCP

    mcp = FastMCP("Your Module")

    from .tools import *
    from .resources import *
    from .prompts import *
    ```
3. **在 `main.py` 注册路由**：生成 SSE/HTTP 应用并挂载到 `/your_module/*`
4. **补充测试与文档**：为新功能编写 `tests/` 并更新 `README.md`、`AGENT.md` 与 `docs/CHANGELOG.md`

## 🔧 代码修改原则
- 修改现有模块时，保持上述目录结构，避免将共享逻辑散落各处
- 任何对外接口（工具、资源、提示）更改后需同步更新 `__init__.py`
- 若涉及数据库或通用逻辑，优先抽取到 `modules/common`
- 所有变更需附带对应单元/集成测试与文档
- 保持向后兼容，如有破坏性改动须在 `docs/CHANGELOG.md` 说明
- 提交前运行 `pytest -q` 确认测试通过
- 相关 README、`AGENT.md` 与 `docs/CHANGELOG.md` 同步更新

## 🛠️ 工具开发规范
- 使用 `@mcp.tool("name")` 装饰器
- 参数与返回值必须提供类型注解
- 写明清晰的 docstring，描述行为与异常
- 优先使用 **async 函数** 处理网络或 I/O
- 函数保持单一职责，避免副作用
- 在 `tools/__init__.py` 中导出，并使用 `tool.fn` 进行单元测试

## 📐 编码与提交规范
- 保持目录结构与类型注解一致
- 所有公开函数需编写 docstring
- 采用原子提交，遵循 `<type>: <desc>` 约定
- 常用类型：`feat`、`fix`、`docs`、`refactor`、`test`、`chore` 等

## 🏷️ 版本号规范
- 遵循语义化版本号 `MAJOR.MINOR.PATCH`
- MAJOR：不兼容的接口变更
- MINOR：向后兼容的新功能
- PATCH：向后兼容的问题修复或文档更新

## 🔄 协作流程
1. 在独立分支上开发并自测
2. 提交前运行相关测试：
    ```bash
    pytest modules/<module>/tests/unit -q
    pytest modules/<module>/tests/integration -q  # 如有
    ```
3. 创建 PR 并等待审核
4. 合并后同步更新文档与 `docs/CHANGELOG.md`

## 🗒️ CHANGELOG 维护
- 所有重要变更需在 `docs/CHANGELOG.md` 中记录，使用实际日期
- 遵循语义化版本号 `MAJOR.MINOR.PATCH`

## 🧪 测试指引
- 单元测试与集成测试分离
- 对被 `@mcp.tool` 装饰的函数，可通过 `.fn` 访问原始实现以便 mock
- 以 `pytest` 为主要测试框架

---
如需了解现有模块的具体实现与接口，请查阅 `README.md` 及相关模块目录下的文档。

