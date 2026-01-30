# Vibe-Spec-Sync Skill

## 概述

这是一个用于保持 Vibe Coding 变更与 Spec 文档同步的 Skill。当检测到代码变更时，自动分析变更类型并提示更新相关 spec 文档。

> **⚠️ 重要提醒**: Spec-First 是推荐的工作方式，本 Skill 是在已发生 Vibe Coding 后的补救措施。
> 请先阅读 [变更规模与流程匹配指南](references/workflow-guide.md) 了解何时应该走完整的 Spec-First 流程。

## 适用场景

在使用本 Skill 之前，请先判断变更规模：

| 变更规模 | 推荐做法 | 是否使用本 Skill |
|----------|----------|-----------------|
| **微小修复** | 直接提交 | ❌ 不需要 |
| **小型 Bug** | 直接改 + 补 Change Log | ⚡ 可选使用 |
| **中型功能** | **应该先更新 Spec** | ✅ 如已 Vibe Coding，使用本 Skill 补救 |
| **大型重构** | **必须先写 ADR + Spec** | ✅ 如已 Vibe Coding，使用本 Skill 补救 |

详细分层标准见：[workflow-guide.md](references/workflow-guide.md)

## 触发条件

当以下情况发生时，自动触发此 Skill：
- 完成一次 Vibe Coding 修复或功能调整
- 用户明确请求同步 spec
- 检测到代码文件有实质性变更

## 工作流程

### Step 1: 检测上下文

1. 获取当前 Git 分支名称
2. 自动检测对应的 spec 目录（规则：`specs/{分支名}/`）
3. 读取 spec 目录下的核心文件：
   - `spec.md` - 主需求文档
   - `tasks.md` - 任务列表
   - `data-model.md` - 数据模型（如存在）
   - `api.md` - API 定义（如存在）

### Step 2: 分析变更

根据以下分类分析本次变更的类型：

| 变更类型 | 标识 | 说明 | Spec 更新点 |
|---------|------|------|-------------|
| Bug 修复 | `BUG_FIX` | 修复现有逻辑的错误 | 在 Change Log 中记录 |
| 行为变更 | `BEHAVIOR_CHANGE` | 改变了功能的行为方式 | 更新 spec.md 相关章节 |
| 数据结构 | `DATA_STRUCTURE` | 修改了数据模型/Schema | 更新 data-model.md |
| API 变更 | `API_CHANGE` | 修改了接口定义 | 更新 api.md |
| 性能优化 | `PERFORMANCE` | 优化性能但不改变行为 | 在 Change Log 中记录 |
| 紧急修复 | `HOTFIX` | 紧急生产问题修复 | 在 Change Log 中记录，标注优先级 |

### Step 3: 生成 Spec 更新

根据变更类型，生成相应的 spec 更新内容：

#### 3.1 Change Log 更新（所有变更必须）

在 `spec.md` 末尾的 `## Change Log` 章节添加记录：

```markdown
## Change Log

| 日期 | 类型 | 变更内容 | 影响需求 |
|------|------|----------|----------|
| YYYY-MM-DD | {变更类型} | {变更描述} | {影响的需求编号或"无"} |
```

#### 3.2 需求更新（BEHAVIOR_CHANGE / DATA_STRUCTURE / API_CHANGE）

- 定位到 spec.md 中受影响的需求章节
- 使用 `~~原内容~~` 标记废弃内容
- 添加新内容并标注 `[Updated: YYYY-MM-DD]`

### Step 4: ADR 决策

对于以下类型的变更，询问用户是否需要创建 ADR：

- `BEHAVIOR_CHANGE` - 推荐创建
- `DATA_STRUCTURE` - 推荐创建
- `API_CHANGE` - 推荐创建
- `BUG_FIX` - 如果修复揭示了设计缺陷，可选创建
- `PERFORMANCE` - 如果涉及架构权衡，可选创建

ADR 文件存放位置：`specs/{分支名}/decisions/ADR-{序号}-{描述}.md`

### Step 5: 输出同步总结

完成同步后，输出总结报告：

```markdown
## 📋 Spec 同步报告

**分支**: {分支名}
**变更类型**: {类型}
**同步时间**: {时间戳}

### 更新内容
- [x] spec.md Change Log 已更新
- [ ] data-model.md 已更新（如适用）
- [ ] api.md 已更新（如适用）
- [ ] ADR 已创建（如适用）

### 变更摘要
{简要描述本次变更}
```

## Spec 目录自动检测规则

```
当前分支: 002-doc-chunking-opt
  ↓
查找目录: specs/002-doc-chunking-opt/
  ↓
如果不存在，尝试模糊匹配（去除数字前缀）
  ↓
如果仍不存在，提示用户手动指定
```

## 注意事项

1. **保持原子性**: 每次只更新与本次变更相关的内容
2. **可追溯性**: 所有变更必须记录在 Change Log 中
3. **最小侵入**: 只修改必要的部分，不要重写整个文档
4. **确认优先**: 在实际修改 spec 文件前，先向用户展示将要做的更改
5. **Vibe 标记**: 如果是事后补救，在 Change Log 中添加 `[VIBE]` 标记

## 参考文档

- [变更规模与流程匹配指南](references/workflow-guide.md) - 何时使用 Spec-First vs Vibe Coding
- [变更类型分类指南](references/change-types.md) - 如何判断变更类型
- [ADR 模板](references/adr-template.md) - 架构决策记录模板
