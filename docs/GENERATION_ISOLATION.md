# Rubric 生成隔离规则

所有正式或开发生成请求只允许使用该条件的已校验 CS50 作业规格、可选参考实现和项目中明确版本化的 prompt。生成调用不得加载本机 skills、个人偏好、聊天历史、个人指令或用户配置。模型请求不得提供 shell、文件系统、浏览器、MCP 或其他工具；每题使用独立的无状态请求。

`python -m rubric_benchmark.luna_run --output <新目录>` 使用固定的 OpenAI Responses API 地址、显式 system 指令、`tools: []` 和 `store: false`。它仅读取 `OPENAI_API_KEY` 作为认证凭据，不使用 Codex CLI 或 Codex 用户配置。找不到凭据时，在创建输出目录或发送请求前失败。实际返回模型 ID、输入及响应哈希应保存在 manifest 中。生成请求不包含评估缺陷清单。

`run_smoke` 的可注入 callable 是开发辅助接口；它不限制调用者的能力，不能用于声称满足本规则的模型生成。调用方必须使用能证明相同隔离条件的适配器。

早期 Codex CLI 测试读取了本机 skill，相关输出已删除，不满足本规则。完成真正的隔离调用需要可用的 API 凭据和支持指定模型的 Responses API 部署；请求的模型和实际返回模型必须分别记录。
