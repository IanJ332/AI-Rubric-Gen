# Cash、Readability、DNA 本地验证记录

2026-11-18。官方来源与参考实现的哈希见各作业 `provenance.json`。三个规格文本按 Problem to Solve 和 Specification 提取，保留原始 HTML。DNA 官方 starter.zip 用于测试，哈希和 URL 已登记。参考实现为项目编写；DNA 参考独立实现最长连续匹配算法。

执行 `/tmp/cs500-audit-ebooks/ci-venv/bin/python -m pytest -q`，46 passed。后续增加反例计算检查后执行 `.../python -m pytest -q tests/test_remaining_assignments.py`，26 passed。Cash 与 Readability 的交互测试使用 CS50 输入 stub。DNA 的官方 starter 测试数据中 20 个官方示例均通过，另外覆盖参数个数、动态 STR、最长连续次数、精确匹配和无匹配。

15 项候选缺陷的正确行为已按 `tests/test_remaining_assignments.py` 运行或核对。部分数值反例通过独立计算检查；尚未对每项构造单缺陷程序或证明缺陷互相独立。清单因此保留 `reference_case_passed_counterexample_pending_independent_validation` 状态，待进一步验证与研究者复核。

本次未运行官方 check50、真实 CS50 库交互或 GPT-6 Luna 生成调用。当前会话未提供可选择该模型的调用接口或凭据，无法核实模型与 thinking effort；本地 mock 测试结果不能代替真实模型 smoke test。Readability 的舍入边界、空输入和异常空白需要依据官方规格与检查另行核实。

## 2026-11-18 追加验证

本次在临时目录生成 15 个单点代码变体，每个从相应参考实现做一次文本替换。执行 `python data/evaluation/mutation/run_mutations.py`，保存结果于 `data/evaluation/mutation/results.json`。每题参考实现通过该题全部 5 组输入，每个变体在自身对应的测试组失败。DNA 表头用例原先把正确匹配者放在第一行，硬编码字段的变体误通过；现将 Bea 放在 Ada 前，以观察错误匹配。

以下每行的五列按该题 `flaws.json` 的顺序，`X` 表示变体导致该用例失败，`.` 表示通过。矩阵证明每个变体可被自身用例区分，也展示测试用例间的重叠；它不证明所有可能的缺陷实现都互不影响。

```text
cash.reference          .....
cash.negative-reprompt  X....
cash.cents              .X...
cash.minimum            XXXX.
cash.remainder          .X.XX
cash.final-line         XXXXX
readability.reference   .....
readability.letters     X....
readability.words       .X...
readability.sentences   ..X..
readability.index       XXXX.
readability.grade-labels ....X
dna.reference           .....
dna.arity               X....
dna.csv-fields          .X.XX
dna.longest-run         ..X..
dna.exact-profile       ...X.
dna.no-match            ....X
```

Cash 最少硬币变体影响了其他金额结果，末行格式变体改变全部输出；Readability 截断可影响多个数值等级；DNA 固定字段也影响匹配与无匹配。这些观察不等于缺陷定义互斥，正式冻结前需要研究者决定评分边界。

在 `/tmp/cs50-verification-env` 安装 `cs50 9.5.0`、`check50 3.5.0`。用真实 CS50 库对 Cash 输入 `foo`、空行、`-1`、`0.41`，程序最终输出 4；Readability 输入官方 One fish 示例输出 `Before Grade 1`。使用 `check50 --local --no-download-checks --no-install-dependencies`，并把临时环境的 `bin` 放在 PATH 前，Cash 10/10、Readability 10/10、DNA 29/29 官方检查通过。第一次 Cash 运行未设置 PATH，检查进程使用了缺少 CS50 的系统 Python，出现九项失败。改用正确 PATH 后重跑全部通过。

这些自动检查仍不能代替研究者独立审查。详见 `data/evaluation/mutation/results.json` 中每次进程的输出和退出状态。早期 Luna smoke 输出及其评分已删除。
