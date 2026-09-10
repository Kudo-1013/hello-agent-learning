# Hello Agent 学习项目
独立于 Python 基础项目，目标：最小 Agent 闭环 → Yuan-Meeting → 简历技术点准备。

## 使用方式
1. 阅读 `docs/学习路线.md` 了解取舍。
2. 按 `docs/01_Agent循环.md` 到 `docs/04_多轮Agent循环.md` 对照示例代码。
3. `.env` 只保存在本地，不要提交或分享。

## 目录
- docs/：定制路线、第一课、新对话交接。
- examples/：本地教学示例，第一课是离线模拟。
- reference/：官方选定章节和第 1、4 章配套代码，保留相对目录。
- SOURCES.md：固定版本、来源与选取范围。

## 当前进度
- 已跑通真实模型、工具选择、Python 工具执行、结果回传和多轮调用的最小闭环。
- 已理解 `messages`、`tool_calls`、循环结束条件、异常回传和 `max_steps`。
- 已理解 ReAct、Plan-and-Solve、Reflection 以及避免无依据补全信息。
- Hello-Agents 入门阶段完成，下一阶段转入 Yuan-Meeting 源码。

## 后续学习
请在 `C:\Users\86187\Desktop\yuan-meeting-main` 中新开对话，并读取该项目的 `AGENTS.md` 和 `LEARNING_HANDOFF.md`。下一阶段直接结合项目学习必要的 LangChain、LangGraph 和 RAG。
