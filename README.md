# MCP Template Collection

这是一个 MCP (Model Context Protocol) 模板集合项目，旨在为开发者提供各种 MCP 服务器实现模板。

## 🚀 项目概述

MCP (Model Context Protocol) 是一个标准化的协议，用于让 AI 模型能够安全地调用外部工具和服务。这个项目提供了多种 MCP 服务器实现模板，帮助开发者快速构建和部署 MCP 服务。

## 📁 分支结构

### 🌿 main 分支
- 项目介绍和文档
- 分支导航指南
- 贡献指南

### 🔧 multiserver 分支
**多服务器 MCP 模板**
- 模块化多服务器架构
- 支持工具、资源、提示三种功能类型
- 统一路由管理
- 支持 SSE 和 HTTP 流式传输
- 完整的中文文档和示例

## 🛠️ 快速开始

### 选择模板

根据您的需求选择合适的模板分支：

```bash
# 克隆项目
git clone <repository-url>
cd mcp-template-collection

# 查看所有分支
git branch -a

# 切换到多服务器模板
git checkout multiserver
```

### 多服务器模板

如果您需要构建支持多个独立服务器的 MCP 应用：

```bash
git checkout multiserver
```

该模板包含：
- ✅ 模块化服务器架构
- ✅ 工具、资源、提示示例
- ✅ 统一路由管理
- ✅ 详细开发文档
- ✅ 快速开始指南

## 🎯 使用场景

### 多服务器模板适用场景
- 需要管理多个独立功能模块
- 希望统一部署和管理多个 MCP 服务
- 需要支持不同的传输协议
- 团队协作开发大型 MCP 应用

## 📚 文档

每个模板分支都包含详细的文档：

- **README.md** - 项目介绍和使用指南
- **docs/DEVELOPMENT_GUIDE.md** - 详细开发指南
- **docs/QUICKSTART.md** - 快速开始教程

## 🤝 贡献

我们欢迎贡献新的模板！如果您有新的 MCP 实现想法：

1. Fork 项目
2. 创建新的功能分支
3. 添加您的模板实现
4. 提交 Pull Request

### 贡献指南

- 每个模板应该是一个独立的分支
- 包含完整的文档和示例
- 遵循项目的代码规范
- 提供清晰的安装和使用说明

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [FastMCP](https://github.com/fastmcp/fastmcp) - 提供 MCP 服务器框架
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP 协议规范

---

**提示**: 这是一个模板集合项目，旨在帮助开发者快速构建 MCP 应用。请根据您的具体需求选择合适的模板分支。 