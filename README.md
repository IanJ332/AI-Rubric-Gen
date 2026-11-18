# AI-Rubric-Gen

研究如何根据 CS50x 2026 作业材料生成评分 rubric，并评估其是否覆盖预先定义的程序缺陷。当前提供 Mario More、Cash、Readability 和 DNA 四个作业的数据包。

## 生成 rubric

需要 Python 3.13 或更新版本、可用的 OpenAI API 凭据，以及支持 `gpt-6-luna` 和 `high` reasoning effort 的 API 部署。在本机安全地设置环境变量 `OPENAI_API_KEY`。不要把密钥写入仓库或聊天。

```sh
python -m rubric_benchmark.luna_run --output runs/luna-high-01
```

命令为四题分别创建独立的 spec-only、point-based 请求。`runs/luna-high-01/raw_data/<assignment>/` 保存输入、请求、响应和 rubric，`manifest.json` 保存状态、模型标识和哈希。输出目录必须是新目录。生成时不向模型提供 tools、个人 skills 或对话历史，评估缺陷清单也不进入 prompt。详情见 [生成隔离规则](docs/GENERATION_ISOLATION.md)。

**当前限制：**以上 API 端到端请求尚未用真实凭据验证，不能保证部署支持模型 ID 或参数。生成程序目前只支持这四个已归档作业；新课程材料须先整理为符合 `data/assignments/<assignment>/` 格式的数据包，并调整生成入口。模型生成后仍需结合课程规格与 `data/evaluation` 中的缺陷清单编写评分报告；当前尚无自动评分报告命令。

可以对 agent 说：

> 使用本仓库的隔离生成轨道，为 Mario More、Cash、Readability 和 DNA 分别生成 point-based rubric。保存每份原始输入和输出，再依据各题官方规格与缺陷清单逐项评分，生成报告。报告指出缺失、模糊或不符合课程要求的标准，并记录模型身份和验证限制。不要使用个人 skills、配置或先前生成的 rubric 作为评分依据。

## 研究与本地验证

```sh
python -m rubric_benchmark matrix --config config/experiment.toml
python -m pip install -e '.[test]'
python -m pytest -q
```

矩阵命令列举 48 个实验条件，不调用模型。每题包含官方规格、参考实现与独立的评估缺陷记录；缺陷仍需研究者复核。参考实现需要 CS50 Python 库。运行结果被 `.gitignore` 排除，避免将生成的 rubric 和个人数据推送到远端。

[实施方案](docs/IMPLEMENTATION_PLAN.md) · [三个作业的详细方案](docs/CS50X_REMAINING_ASSIGNMENTS_PLAN.md) · [验证记录](docs/THREE_ASSIGNMENTS_VALIDATION.md) · [需求追踪](docs/REQUIREMENTS_TRACEABILITY.md)
