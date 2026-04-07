# Commit Plan

下面按你现在仓库里的实现来拆，尽量保持每个 commit 的边界清晰、可讲述、也方便后面继续扩展成 hourly job。

## 1. `refactor ingestion into a reusable command`

**目标**  
把当前“一次性脚本”重构成一个可复用的 ingestion 入口，后续不管是手动跑、定时跑、还是监控包装，都会基于同一个 `run_ingestion()`。

**对文件的修改**
- 新建 `ingestion.py`：新增 `run_ingestion(...)`，把“建表 + 调 scraper + 汇总结果”放到这里。
- [main.py](/Users/zuotianhao/Desktop/sa intern/sa-intern/main.py)：去掉具体抓取逻辑，只负责传参并调用 `run_ingestion(...)`。
- [scraper.py](/Users/zuotianhao/Desktop/sa intern/sa-intern/scraper.py)：保留底层抓取逻辑，但改成返回结构化结果，而不是只 `print`；顺手修掉文件末尾错误的 `print_filtered_comments(...)` 调用。
- [scraper.py](/Users/zuotianhao/Desktop/sa intern/sa-intern/scraper.py)：把 `app_id`、`lang`、`country`、`max_reviews`、`sleep_seconds` 这些参数都通过函数参数传入，不依赖硬编码常量。
- [README.md](/Users/zuotianhao/Desktop/sa intern/sa-intern/README.md)：补一段“如何手动运行一次 ingestion”的说明。

**完成标准**
- `python main.py` 仍然能跑通。
- 其他模块也可以直接 import `run_ingestion()` 来重复调用。
- `main.py` 不再直接承担业务细节。

---

## 2. `persist ingestion run metadata`

**目标**  
让每次 ingestion 都有一条 run-level 记录，系统开始具备“可追踪的运行历史”。

**对文件的修改**
- [create_db.py](/Users/zuotianhao/Desktop/sa intern/sa-intern/create_db.py)：新增 `ingestion_runs` 表。
- [create_db.py](/Users/zuotianhao/Desktop/sa intern/sa-intern/create_db.py)：新增类似 `start_ingestion_run(...)` 和 `finish_ingestion_run(...)` 的 helper，用来写入 `run_id`、`started_at`、`ended_at`、`status`、`records_fetched`、`records_inserted`、`error_message`。
- `ingestion.py`：在 `run_ingestion(...)` 开始时创建 run record，结束时更新 run record。
- [main.py](/Users/zuotianhao/Desktop/sa intern/sa-intern/main.py)：只负责展示最终 run summary，不直接关心数据库细节。

**完成标准**
- 每执行一次 ingestion，数据库里都会新增一条 run 记录。
- 即使这一轮没有插入任何新评论，也会留下 run 记录。
- 后续监控和报表已经有基础数据来源。

---

## 3. `track insert vs duplicate outcomes explicitly`

**目标**  
把“成功新增”和“重复已存在”明确区分开，解决现在 `INSERT OR REPLACE` 把 duplicate 情况吞掉的问题。

**对文件的修改**
- [create_db.py](/Users/zuotianhao/Desktop/sa intern/sa-intern/create_db.py)：把评论写入逻辑从 `INSERT OR REPLACE` 改成更适合监控的方式，比如 `INSERT OR IGNORE`。
- [create_db.py](/Users/zuotianhao/Desktop/sa intern/sa-intern/create_db.py)：让 `add_comment(...)` 这类函数返回写入结果，比如“inserted”或“duplicate”。
- [scraper.py](/Users/zuotianhao/Desktop/sa intern/sa-intern/scraper.py)：每处理一条 review，都更新 `records_fetched`、`inserted_count`、`duplicate_count`。
- [create_db.py](/Users/zuotianhao/Desktop/sa intern/sa-intern/create_db.py)：给 `ingestion_runs` 表补充 `duplicate_count` 字段。
- `ingestion.py`：在 run 完成时，把 `inserted_count` 和 `duplicate_count` 写回 run metadata。

**完成标准**
- 你可以明确回答“一次 run 抓到了多少条、真正新增了多少条、重复了多少条”。
- duplicate 至少按 `review_id` 统计。
- 主评论表不会因为重复抓取而被无意义覆盖。

---

## 4. `add basic data quality checks per run`

**目标**  
让每次 run 除了有数量统计，还能有最基础的数据质量统计，形成最小可用的 monitoring layer。

**对文件的修改**
- 新建 `quality_checks.py`：集中放数据质量检查函数，避免 [scraper.py](/Users/zuotianhao/Desktop/sa intern/sa-intern/scraper.py) 越堆越乱。
- `quality_checks.py`：实现这些检查项的计数逻辑：空 `content`、缺失 `review_id`、缺失 `date`、非法 `score`、无效 UTF-8、过短评论数。
- [scraper.py](/Users/zuotianhao/Desktop/sa intern/sa-intern/scraper.py)：在处理每条 review 时调用质量检查，并累计 metrics。
- [create_db.py](/Users/zuotianhao/Desktop/sa intern/sa-intern/create_db.py)：给 `ingestion_runs` 增加对应的质量指标字段，或者新增一张 `ingestion_run_quality` 表专门存这些 metrics。
- `ingestion.py`：将本轮质量检查结果和 run 绑定起来落库。
- [README.md](/Users/zuotianhao/Desktop/sa intern/sa-intern/README.md)：补充这些指标的定义，避免后面汇报时口径不一致。

**完成标准**
- 每次 run 结束后，都能查到一组固定的数据质量指标。
- 检查逻辑和抓取逻辑分离，后面扩展规则时不会继续污染 scraper。
- 对于哪些记录“只统计不丢弃”、哪些记录“直接跳过”，代码里要有一致规则。

---

## 5. `record failures and add a simple monitoring report`

**目标**  
把异常运行显式记录下来，并提供一个简单报表入口，方便快速看最近几次 ingestion 的健康状态。

**对文件的修改**
- `ingestion.py`：在 `run_ingestion(...)` 外层加 `try / except / finally`。
- `ingestion.py`：出现异常时，把本轮 run 标记为 `FAILED`，并记录 `error_message`。
- [create_db.py](/Users/zuotianhao/Desktop/sa intern/sa-intern/create_db.py)：新增查询最近几次 run 的 helper，比如 `get_recent_ingestion_runs(limit=10)`。
- 新建 `monitoring_report.py`：读取最近 N 次 run，打印 `started_at`、`status`、`records_fetched`、`records_inserted`、`duplicate_count`、质量指标、`error_message`。
- [README.md](/Users/zuotianhao/Desktop/sa intern/sa-intern/README.md)：新增“如何查看 monitoring report”的命令说明。
- [database_peaker.py](/Users/zuotianhao/Desktop/sa intern/sa-intern/database_peaker.py)：可选，保留为低层 debug 工具，不建议把业务报表直接塞进这个文件。

**完成标准**
- ingestion 失败时，数据库里能看到失败 run，而不是静默结束。
- 你可以通过一个简单命令查看最近几次 run 的核心监控信息。
- 后面接 scheduler 时，不需要再重构监控逻辑，只要定时触发 `run_ingestion()` 即可。

---

# 你可以这样向 manager 解释这 5 个 commit 的逻辑

1. 先把脚本改成可复用 command，解决“只能手动跑一次”的问题。  
2. 再给每次运行加 metadata，解决“跑过了但没有运行历史”的问题。  
3. 然后区分 inserted 和 duplicate，解决“无法衡量真实增量”的问题。  
4. 接着补数据质量 checks，解决“只知道跑了，不知道数据好不好”的问题。  
5. 最后加 failure logging 和 monitoring report，解决“系统出问题时不可见”的问题。  

如果你愿意，我下一步可以直接把这 5 个 commit 再改写成更像真正 Git commit 的格式：`commit message + changed files + code-level tasks + expected demo result`。