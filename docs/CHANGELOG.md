# 变更日志

本文档记录项目的所有重要变更。

## [2.4.0] - 2025-08-02

### Changed
- 移除内存数据库适配器，统一使用 SQLAlchemy 后端
- 重构 DataRepository 以直接依赖 SQLAlchemyDatabase

## [2.3.0] - 2025-08-02

### Added
- 新增 `SQLAlchemyDatabase`，使用 SQLAlchemy 兼容多种关系型数据库
- 更新文档和依赖说明

## [2.2.0] - 2025-08-02

### Added
- 引入异步数据库抽象层及内存实现
- 新增 `DataRepository`，实现“查库→外部获取→入库”流程
- 提供示例工具和单元测试演示数据仓储逻辑
- 更新 README 与 DEVELOPMENT_GUIDE 说明数据库抽象层

## [2.1.0] - 2025-08-02

### Added
- 为每个模块新增 `config.yaml`、`examples` 和 `tests` 目录
- 重构 `internal` 目录为 `api`、`core` 和 `db` 子包
- 更新 `AGENT.md`、`README.md`、`QUICKSTART.md` 和 `DEVELOPMENT_GUIDE.md`

### Changed
- 调整项目结构说明，补充测试与示例用法

## [2.0.0] - 2025-07-28

### Added
- 完善AGENT.md，新增模块修改规则
- 添加提交与协作流程指南
- 新增CHANGELOG维护规范
- 补充版本号管理规则

### Changed
- 简化文档结构，移除重复的定制建议
- 保留README.md中的定制要点，优化文档层次结构
- 避免文档中的重复内容
- 在README.md中添加对CHANGELOG的引用和项目文档章节

## [1.3.0] - 2025-07-28

### Added
- 添加示例项目提示和定制指南
- 为所有文档添加警告提示，明确标识为模板项目
- 帮助用户根据实际需求进行项目定制

## [1.2.0] - 2025-07-28

### Added
- 添加AGENT.md - AI代理操作指南
- 为AI代理提供项目结构理解、开发流程、代码规范和调试指南
- 提升AI代理与项目的协作效率

## [1.1.0] - 2025-07-28

### Added
- 添加内部代码支持，增加internal目录
- 为模块添加API客户端、数据处理和工具类

### Changed
- 修改README.md，明确模块目录结构
- 更新DEVELOPMENT_GUIDE.md，添加内部代码使用原则和示例
- 更新QUICKSTART.md，提供创建内部代码的步骤和示例

### Removed
- 删除不再使用的utils/registry.py文件

## [1.0.0] - 2025-07-27

### Added
- 初始提交：MCP多服务器模板项目
- 添加模块化MCP服务器架构
- 包含示例模块（数学工具、文本处理）
- 添加完整文档（README、开发指南、快速开始）
- 添加正确的Python项目结构，包含init.py文件
- 包含requirements.txt和.gitignore
- 支持SSE和HTTP流式传输
- 提供工具、资源和提示示例 