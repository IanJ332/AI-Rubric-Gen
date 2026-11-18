# CS50x 2026 rubric benchmark 实施方案

范围为 Problem Set 6 的 Python **Cash、Readability、DNA**。完成标准是三项作业均可通过同一个生成入口运行，沿用现有四项作业的 48 个实验条件。本文给出资料清单、输入合同、15 项候选缺陷、验证用例及执行门槛。方案中的文件、命令和 API 请求均属于后续实施。

## 1. 资料来源与使用

| 资料 | 在工程中的用途 |
| --- | --- |
| 用户提供的 *Harvard CS50x 2026 Assignments*，第 4–5 页 | 定位 Problem Set 6 的三个 Python 版本。Cash 在 PSet 1 也有同名 C 题，Readability 在 PSet 2 也有同名 C 题，归档时用版本和 Python 文件名复核。 |
| [CS50x 2026 Problem Set 6](https://cs50.harvard.edu/x/psets/6/) 和三题官方页面 | 作业要求、术语、输入输出和官方测试的依据。分别归档作业页面，保留版本标识、抓取时间及哈希。 |
| [Week 6 讲义](https://cs50.harvard.edu/x/notes/6/) | 核对 Python 教学背景。讲义示范只供研究者理解课程，不转化为评分条件。 |
| Check-in #2，第 2–3 页 | 确定四因素、每题五项缺陷、每格一次正式生成、两名研究者独立标注。 |
| 用户提供的 *CS500 Check-in 2 Research Dossier*，第 5–11 页 | 采用同题同字节、预先冻结缺陷、验证单一可观察错误、记录有效替代实现和模型版本等建议。按 Check-in #2 执行 rubric 文本覆盖研究。 |

优先读取各题官方页面的 `Problem to Solve`、`Specification` 和 `How to Test`。DNA 另外归档官方 [2026 starter ZIP](https://cdn.cs50.net/2026/x/psets/6/dna.zip)，验证其中的 `dna.py`、`databases/`、`sequences/`，记录归档与采用文件的 SHA-256。获取课程资料时保留 Harvard 署名、来源、改动说明及许可链接，并单独记录 ZIP 内文件附带的许可或来源说明。公开分发前复核各材料的适用条款。 [CS50x 许可](https://cs50.harvard.edu/x/license/)

### 数据包与 prompt 边界

沿用 [Mario 的目录、字段和校验方式](../data/assignments/mario-more/provenance.json)。最初实现中直接复用 `load_generation_input`。

| 计划路径 | 内容及消费方 |
| --- | --- |
| `data/assignments/<id>/source.html` | 官方原始页面。供溯源与人工审阅。 |
| `data/assignments/<id>/specification.txt` | 给 LLM 的唯一课程文本，UTF-8、LF、保留有语义的空白和标点。 |
| `data/assignments/<id>/reference.py` | 团队编写、按官方用例验证的一个 Python 示例。在 `spec-reference` 条件下按冻结字节加入。 |
| `data/assignments/<id>/provenance.json` | 沿用 `assignment_id`、`publisher`、`requested_url`、`resolved_url`、`redirect_status`、`accessed_at_utc`、`edition`、`selection`、`license`、`reference_author`、`sha256` 和 `requirements`。增记官方检查 ID、提取规则版本、参考运行环境及 DNA starter 来源。 |
| `data/evaluation/<id>/flaws.json`、`evidence.json`、`fixtures/` | 每题五项稳定缺陷 ID、要求 ID、预期与错误行为、用例和证据位置、状态、复核记录。官方用例、靶向用例和正确替代实现的证据在此侧归档。 |

**建议冻结的文本规则**：四题统一将官方 `Problem to Solve` 和 `Specification` 提取到 prompt。官方 `How to Test`、讲义、安装步骤、DNA ZIP 及自制用例用于验证。DNA 在规格块里保留官方关于 `longest_match` 的说明。当前 Mario 开发版包含测试示例，若团队采用此规则，在正式冻结时用同一规则重建 Mario 的 `specification.txt` 和哈希，保留原开发快照及变更记录。团队在 pilot 前复核四题均使用同一提取规则。

每个数据包先验收当前页面明确标示 CS50x 2026、实际跳转及哈希，然后逐段核对提取文本。保留标题、公式、输出字面量、源代码符号和原有条件。生成进程只读校验后的规格和可选参考，离线预检负责核查其他材料及清单摘要。

## 2. 各题工程任务

### Cash · `cash`

**规格与参考。** 在官方路径 `sentimental-cash/cash.py` 上验证。参考使用 CS50 `get_float` 读美元金额，重复拒绝负值，接受零。将两位以内的有效小数金额转换为整数美分，按 25、10、5、1 美分求最小硬币数。参考可以使用 `divmod` 并保留每一步余量，最后一行输出整数和换行。评分以行为为准，允许符合规格的其他策略。规格未指定不足一美分的舍入约定。 [Cash 官方规格与用例](https://cs50.harvard.edu/x/psets/6/cash/)

| 候选 flaw ID | 验证输入与正确行为 | 区分的错误 |
| --- | --- | --- |
| `cash.negative-reprompt` | 依次给出 `-1`、`-0.25`、`0.50`，读取三次，最后输出 `2\n`。 | 接受负数、在负数时停止，或只允许重试一次。 |
| `cash.cents` | `0.29` 按 29¢ 计算，输出 `5\n`。 | 直接截断二进制浮点乘积得到 28¢，输出 `4\n`。 |
| `cash.minimum` | `0.50` 输出 `2\n`。此用例可整除，无剩余分币。 | 以五枚 10¢ 凑出正确总额，未用最少枚数。 |
| `cash.remainder` | 官方 `0.41` 输出 `4\n`，可行组合为 25+10+5+1。 | 前三种硬币正确后遗漏最后 1¢，输出 `3\n`。 |
| `cash.final-line` | `0.01` 的最后一行是 `1\n`，可有先前的提示。 | 数值正确但末行写成 `1 coin\n`，或缺少结尾换行。 |

**验证。** 用 `get_float` stub 测负数重试次数和有效零。真实 CS50 库再跑非数字、空行后给合法输入的交互用例，区分库的解析行为和程序的非负约束。执行官方所有示例，包括 `0.15 → 2`、`1.60 → 7`、`23 → 92`、`4.2 → 18`。对人工用例用独立的整数最小硬币计算复核。官方检查 ID 为 `cs50/problems/2026/x/sentimental/cash`。

### Readability · `readability`

**规格与参考。** 在 `sentimental-readability/readability.py` 上验证。使用 CS50 `get_string`，统计 ASCII 字母、以空格分隔的词，以及 `.`、`!`、`?`。设字母数、词数、句子数为 `a, w, s`，则 `L = 100*a/w`、`S = 100*s/w`，指数为 `0.0588*L - 0.296*S - 15.8`。按官方规则取最近整数，输出 `Grade X`、`Grade 16+` 或 `Before Grade 1`。认可字符判断、正则或等价计数方法。 [Readability 官方规格与用例](https://cs50.harvard.edu/x/psets/6/readability/)

| 候选 flaw ID | 验证输入、计数 `(a,w,s)` 与期望输出 | 区分的错误 |
| --- | --- | --- |
| `readability.letters` | `Green birds fly high above lakes 1234567890.` → `(27,7,1)` → `Grade 3`。 | 把数字算成字母会输出 `Grade 11`。另加含非 ASCII 字母的用例复核范围。 |
| `readability.words` | `Don't stop looking around the garden.` → `(30,6,1)` → `Grade 9`。 | 把 `Don't` 拆成两个词会输出 `Grade 5`。 |
| `readability.sentences` | `Bright stars! Silver moons? Lanterns shine.` → `(35,6,3)` → `Grade 4`。 | 只识别句号会输出 `Grade 14`。 |
| `readability.index` | `Bright stars shine above the lake.` → `(28,6,1)`，原始指数约 `6.7067`，输出 `Grade 7`。 | 截断得到 `Grade 6`，漏掉每百词归一化得到 `Before Grade 1`。归为同一指数计算与取整项。 |
| `readability.grade-labels` | `Small cats nap.` → `Before Grade 1`，`Extraordinary discoveries inspire curiosity.` → `Grade 16+`。 | 对低端或高端直接输出数值等级，或使用错误标签。 |

**验证。** 跑官方全部输入文本和输出，另对合成用例用手算或精确有理数独立算出计数、原始指数和标签。覆盖 ASCII 范围、句子标点、普通等级及两端等级。若要用跨阈值舍入的例子，先对照官方文字、[所引用的 PSet 2 说明](https://cs50.harvard.edu/x/psets/2/readability/) 和能取得的 2026 Python 检查，分别记录原始指数与取整后等级。正式缺陷用例采用远离阈值的上述两端例子。空输入、连续空格及恰好半整数的行为在官方证据未明确前作为研究者备注。官方检查 ID 为 `cs50/problems/2026/x/sentimental/readability`。

### DNA · `dna`

**规格与参考。** 在 `dna/dna.py` 上验证。按 CSV 在前、序列文本在后的顺序接收两个文件路径，其余参数数量打印错误。正确参数数量下，官方允许假设两个文件都有效。读取 CSV 表头，以 `name` 后的字段确定要比较的 STR。对每个字段计算最长连续重复次数，对同一人的所有字段做精确匹配，输出姓名或 `No match`。以官方 starter 为参考实现起点，记录 `longest_match` 来源，归档为单文件可运行的参考。允许功能等价的解析和实现。 [DNA 官方规格与用例](https://cs50.harvard.edu/x/psets/6/dna/)

下表用 `/` 分隔 CSV 的行。实施时写成真实的 CSV 和文本文件。

| 候选 flaw ID | 验证输入与正确行为 | 区分的错误 |
| --- | --- | --- |
| `dna.arity` | 分别以 0、1、3 个文件参数运行，均打印错误并结束。以 2 个有效文件路径验证正常分支。 | 错误个数触发未处理异常，或继续访问参数。错误文案由作者选择。 |
| `dna.csv-fields` | CSV `name,CG / Ada,2 / Bea,1`，文本 `CGCG`，输出 `Ada`。再用官方大小数据库覆盖不同列数。 | 写死某套 STR 列，或依赖特定的官方数据库形状。 |
| `dna.longest-run` | CSV `name,AC / Ada,3 / Bea,4`，文本 `ACACACGGAC`，输出 `Ada`。 | 累加分隔出现的次数得到 4，误报 `Bea`。 |
| `dna.exact-profile` | CSV `name,AC,GT / Bea,2,2 / Ada,2,1`，文本 `ACACGT`，输出 `Ada`。 | 前一行仅首个字段相同，若接受部分匹配会误报 `Bea`。 |
| `dna.no-match` | CSV `name,AC,GT / Ada,1,2`，文本 `ACACGT`，输出 `No match`。 | 无匹配时静默结束、输出错误文案或返回某人姓名。 |

**验证。** 以真实文件和子进程验证参数顺序、错误分支和标准输出。跑官方文档的 20 组示例，四组使用小库，十六组使用大库。至少保留一正一负的跑通证据，例如小库的 `1.txt → Bob`、`2.txt → No match`，并保存全部用例的状态。题目未要求特定 CSV 库、无效文件恢复或多重完全匹配处理。官方检查 ID 为 `cs50/problems/2026/x/dna`。

## 3. 参考与缺陷验收

1. 每题先冻结官方来源，再编写参考。记录 Python、CS50 库和 `check50` 的实际版本、运行命令、用例 ID、期望值和观察值。按原作业目录运行匹配的 `check50`；若环境或认证限制，保留受限原因及官方示例本地运行结果，明确两类证据。
2. 每个候选先按官方要求标注来源小节，再核查参考通过针对性用例，错误行为会得到不同结果。优先采用小幅变体或可独立复算的对照结果。输出格式按原始行核对，避免 `strip()` 隐藏换行或额外字符。口头例子也记录推导、输入和结果。
3. 针对概念重叠做复核。Cash 的金额转换、硬币选择和余量分别用不同输入区分。DNA 的连续次数、部分匹配和无匹配分别有可区分的 CSV。若同一错误会同时触发几项，标注受影响行为和判分边界。证据不足时在冻结前调整定义。
4. 每题保留一种正确替代路径的用例证据。例如 Cash 用逐次找零替代 `divmod`，Readability 用字符范围判断替代一个正则，DNA 用 `csv.reader` 替代 `DictReader`。两名研究者核对官方要求、参考行为和五项缺陷，签署版本化清单。连同 Mario 共 20 项。

## 4. 生成工程

### 统一入口

- 复用 `matrix.py` 的 `Condition` 和四个维度。新增共用 `build_prompt(condition, generation_input)`，迁移现有 Mario 开发 smoke 的 prompt 拼装逻辑；生成入口接收矩阵条件，覆盖任意已登记作业。建议实现 `python -m rubric_benchmark generate --mode dry-run --config config/experiment.toml --output <new-dir>`，可加 `--assignment` 查看单题。保留现有 `matrix` CLI。
- 固定英文通用任务说明，要求每个评分项写出应观察的行为或证据、影响得分或等级的表现，并用简明语言写出可供学生理解的反馈。只要求官方规格明确规定的约束，并接受其他合规实现。正文只有该题 canonical spec、该格格式块和可选的示例参考块。三题专属信息来自规格，缺陷清单与合成用例留给评估。
- `points` 候选要求每项满分、可辨别的部分得分和总分，例如固定 100 分。 `levels` 候选要求每个标准下给出 Meets / Partially Meets / Does Not Meet 的行为描述。两种格式共享覆盖范围。总分、等级名称和确切文本由团队在正式冻结前定稿。格式适配只记录符合情况，有用但格式偏离的输出按预先确定的规则纳入标注。
- 每次用新的无历史请求。模型槽只决定调用哪个已配置部署。按每格存下 `condition_id`、模板版本、spec/reference SHA-256、最终 prompt 哈希和有效请求参数。保存原始响应、模型及路由元数据、结束原因、用量、UTC 时间、错误与尝试编号。按 [总方案](IMPLEMENTATION_PLAN.md) 实施隔离的 pilot/formal 命名空间及恢复规则。

### 运行与失败处理

- `dry-run` 先验证选定条件和所有所需输入，再按 `condition_id` 输出 manifest 与每格 `input.json`。清单至少包含模式、版本、条件 ID、模板和数据哈希。遇到缺作业包、缺参考或哈希不符时，把错误定位到具体作业和文件，并在任何 API 调用前退出。正式模式要求完整矩阵。
- 后端适配器负责鉴权、参数映射和原始响应落盘。记录请求模型和返回模型，标明供应商不支持的参数以及无法核实的有效值。将正常响应、空响应、拒答、截断、超时、格式偏离及模型不符分别记录。是否重试由冻结规则决定。重试使用原条件 ID 和新尝试号。
- 先持久化原始输出、哈希和尝试完成记录，再发布该格结果。恢复时验证清单及输入哈希，跳过已经接受的格。发送状态未知的尝试进入待核对状态，避免重复调用。预检和报告都保留每格完整记录，便于解释失败和缺失。
- Pilot 可先为每个模型分别选两格，一格 points、一格 levels，一格 spec-only、一格 spec-reference，三题均有代表。用 dry-run 实测长度后，纳入最长的输入场景，再冻结具体六格和预算。人工查看三份作业内容是否被正确引用，并确认截断和格式检查有效。

### 实施顺序与门槛

| 步骤 | 交付 | 验收 |
| --- | --- | --- |
| 1 · 冻结课程输入 | 三题 HTML 与规格、来源记录、DNA ZIP 按需归档、四题统一提取规则 | 题名、年度、语言和官方 ID 对齐。源文件、规范文本和实用资产均可按记录复查。 |
| 2 · 验证参考和评估包 | 三个 `reference.py`、15 项缺陷、证据及复核记录 | 每题通过文档示例和目标用例，5 个 ID 唯一且各有可观察证据。四题共 20 项通过双人复核。 |
| 3 · 接入离线生成 | 通用 prompt builder、dry-run、mock 输出和实际运行记录 | 三题分别各 12 格，共 36 格；加 Mario 共 48 格。相同作业、上下文和格式跨模型得到同字节消息。24 组上下文对只改变参考块，24 组格式对只改变格式块。 |
| 4 · 验证隔离和持久化 | 清单、hash 校验、漏读探针、provider mock 及失败记录 | 只有 spec 的请求内容不含 reference。移除评估目录后生成仍能运行。将独有字串放入缺陷和证据文件后，实际 mock 请求中无该字串。改动一个输入字节会触发哈希校验失败。mock 全矩阵可生成并追溯每格结果。 |
| 5 · Pilot 与正式冻结 | exact 模型 ID、运行预算、原始样稿、代码本、协议签署 | 团队批准预算后，按总方案最多六次 live pilot，覆盖三个部署、两种上下文和两种格式，加入实际测得最长的输入。核对返回部署、截断和格式，再冻结四题、模板、部署及代码本。pilot 使用独立目录。 |
| 6 · 正式生成及评价 | 48 格结果清单、两人独立批注、仲裁和描述性结果 | 每格最多一份接受的 rubric；失败有独立状态。每位研究者最多完成 240 个缺陷评分和 48 个实现偏差判断。保存两份原始判断后计算加权 Cohen’s κ，再仲裁。 |

## 5. 如何判断 rubric 对教师和学生有用

评分对象是 rubric 明示的检查能力。对于 Cash，笼统要求“正确处理输入”可评 1 分，明确要求“负数后反复重新询问，直至获得非负值”可评 2 分。缺少适用评分项则评 0 分。Readability 和 DNA 共用同一标准，证据可引用 rubric 条目或多个条目的组合。

每份 rubric 另做一次实施偏差判断。若强制 Cash 使用 `divmod`、Readability 必须用某个正则、DNA 必须使用 `DictReader`，记录违规条目、官方依据和可验证的正确替代路径。显式要求的 CS50 输入函数按规格处理。

报告每份 rubric 的五项平均覆盖分（0–2）、显式覆盖比例（评分为 2 的比例）、实现偏差，以及各实验条件下的结果与缺失量。报告示例应让教师看得出哪些条目可执行、哪些反馈对学生说清了问题。单次 rubric 文本研究提供覆盖与评分一致性证据。实际评分准确性、时间节约和学生学习收益需要后续独立验证。
