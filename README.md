# Vibe-Spec-Sync

<p align="center">
  <strong>🔄 让 Vibe Coding 变更与 Spec 文档保持同步的 AI Skill</strong>
</p>

<p align="center">
  <a href="#特性">特性</a> •
  <a href="#安装">安装</a> •
  <a href="#使用方法">使用方法</a> •
  <a href="#工作流程">工作流程</a> •
  <a href="#参考文档">参考文档</a> •
  <a href="#许可证">许可证</a>
</p>

---

## 简介

**Vibe-Spec-Sync** 是一个专为 AI 辅助编程设计的 Skill，用于解决 Vibe Coding（即兴编程）后 Spec 文档与实际代码不同步的问题。

当你在 AI 助手的帮助下快速修复 Bug 或调整功能后，这个 Skill 会自动分析变更类型，并帮助你更新相关的 Spec 文档，保持文档与代码的一致性。

> ⚠️ **重要提醒**: Spec-First 是推荐的工作方式，本 Skill 是在已发生 Vibe Coding 后的补救措施。

## 特性

- 🔍 **自动检测**: 根据 Git 分支名自动定位对应的 Spec 目录
- 📊 **智能分类**: 自动识别变更类型（Bug 修复、行为变更、API 变更等）
- 📝 **增量更新**: 最小侵入式更新，只修改必要的文档部分
- 📋 **Change Log**: 自动维护变更日志，保证可追溯性
- 🏗️ **ADR 支持**: 对重大变更推荐创建架构决策记录

## 安装

将此 Skill 添加到你的 AI 编程助手中：

```bash
# 克隆仓库
git clone https://github.com/your-username/vibe-spec-sync.git

# 将 SKILL.md 添加到你的项目或 AI 工具配置中
```

## 使用方法

### 适用场景

在使用本 Skill 之前，请先判断变更规模：

| 变更规模 | 推荐做法 | 是否使用本 Skill |
|----------|----------|-----------------|
| **微小修复** | 直接提交 | ❌ 不需要 |
| **小型 Bug** | 直接改 + 补 Change Log | ⚡ 可选使用 |
| **中型功能** | **应该先更新 Spec** | ✅ 如已 Vibe Coding，使用本 Skill 补救 |
| **大型重构** | **必须先写 ADR + Spec** | ✅ 如已 Vibe Coding，使用本 Skill 补救 |

### 触发方式

当以下情况发生时，可触发此 Skill：

1. 完成一次 Vibe Coding 修复或功能调整
2. 明确请求同步 Spec
3. 检测到代码文件有实质性变更

### 变更类型

| 变更类型 | 标识 | 说明 | Spec 更新点 |
|---------|------|------|-------------|
| Bug 修复 | `BUG_FIX` | 修复现有逻辑的错误 | 在 Change Log 中记录 |
| 行为变更 | `BEHAVIOR_CHANGE` | 改变了功能的行为方式 | 更新 spec.md 相关章节 |
| 数据结构 | `DATA_STRUCTURE` | 修改了数据模型/Schema | 更新 data-model.md |
| API 变更 | `API_CHANGE` | 修改了接口定义 | 更新 api.md |
| 性能优化 | `PERFORMANCE` | 优化性能但不改变行为 | 在 Change Log 中记录 |
| 紧急修复 | `HOTFIX` | 紧急生产问题修复 | 在 Change Log 中记录，标注优先级 |

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                    Vibe-Spec-Sync 工作流                      │
└─────────────────────────────────────────────────────────────┘

     ┌──────────────┐
     │  Vibe Coding │
     │   完成变更    │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │ Step 1:      │
     │ 检测上下文    │  ──→ 获取分支名，定位 Spec 目录
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │ Step 2:      │
     │ 分析变更类型  │  ──→ BUG_FIX / BEHAVIOR_CHANGE / ...
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │ Step 3:      │
     │ 生成Spec更新  │  ──→ Change Log + 需求更新
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │ Step 4:      │
     │ ADR 决策     │  ──→ 重大变更推荐创建 ADR
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │ Step 5:      │
     │ 输出同步总结  │  ──→ 生成同步报告
     └──────────────┘
```

## 目录结构

```
vibe-spec-sync/
├── README.md              # 本文件
├── SKILL.md               # Skill 定义文件
├── LICENSE                # MIT 许可证
├── references/            # 参考文档
│   ├── workflow-guide.md  # 变更规模与流程匹配指南
│   ├── change-types.md    # 变更类型分类指南
│   └── adr-template.md    # ADR 模板
└── scripts/               # 辅助脚本
```

## 参考文档

- [变更规模与流程匹配指南](references/workflow-guide.md) - 何时使用 Spec-First vs Vibe Coding
- [变更类型分类指南](references/change-types.md) - 如何判断变更类型
- [ADR 模板](references/adr-template.md) - 架构决策记录模板

## 最佳实践

1. **Spec-First 优先**: 尽量在编码前先更新 Spec
2. **及时同步**: Vibe Coding 后立即运行 Skill 同步
3. **保持原子性**: 每次只同步与本次变更相关的内容
4. **添加 VIBE 标记**: 事后补救的变更在 Change Log 中添加 `[VIBE]` 标记

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

---

<p align="center">
  Made with ❤️ for better documentation
</p>
