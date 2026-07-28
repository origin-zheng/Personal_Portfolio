# 数据清洗规则说明（Clean Summary）

## 说明

本文档记录信贷训练集清洗过程中采用的所有处理规则及其业务依据，对应代码文件见 `02_Python_Risk_Model/data_clean/` 目录。详细的数据探索发现（缺失比例、异常值分布、分组统计规律等）见 `data_intro.md`，本文档不重复展开，仅聚焦"做了什么处理、为什么这么做"。

数据来源：Kaggle - Give Me Some Credit
https://www.kaggle.com/competitions/GiveMeSomeCredit/data

---

## 1. 缺失值处理规则

对应代码：`missing_handle.py`

### 1.1 判断标准：随机缺失 vs 业务缺失

处理缺失值前，先判断该字段缺失是否与其他风险指标存在系统性关联：
- 若存在关联（如缺失比例与违约率、其他异常值存在统计相关性），判定为**业务缺失**，缺失本身承载风险信号，需保留标记后再填补；
- 若无证据显示与风险相关，且缺失比例较小，判定为**随机缺失**，直接用统计量填补即可，不需额外保留标记。

### 1.2 具体规则

| 字段 | 缺失比例 | 判定 | 处理规则 | 依据 |
|---|---|---|---|---|
| MonthlyIncome | 19.82% | 业务缺失 | 新增`monthly_income_missing_flag`标记列(1=原缺失)，再用中位数填补 | 已验证：负债率异常值中79%伴随收入缺失，收入缺失组与非缺失组违约率存在明显差异，缺失本身具有预测价值，不应直接丢弃该信号 |
| NumberOfDependents | 2.62% | 随机缺失 | 直接用中位数填补 | 缺失比例小，且未发现与风险指标的系统性关联，属于中性人口统计字段 |

---

## 2. 异常编码值处理规则

对应代码：`missing_handle.py`（后续在`outlier_process.py`、`feature_create.py`中同步修复遗漏）

### 2.1 规则

三个逾期次数字段（`NumberOfTime30-59DaysPastDueNotWorse`、`NumberOfTime60-89DaysPastDueNotWorse`、`NumberOfTimes90DaysLate`）中，取值为 **98** 或 **96** 的记录，统一替换为 **0**。

### 2.2 业务依据

- 三个字段中取值恰为98的记录数完全一致(均264条)，且与"取值大于10"的记录数高度接近，不符合真实业务数据应有的连续分布特征，判定为系统特殊编码值，而非真实逾期次数；
- 后续在构造`total_late_times`衍生特征时，进一步发现96也是同类异常编码(各5条)，采用相同规则一并处理；
- 选择填充为0而非中位数：因无法确认这批客户的真实逾期情况，用0是保守、不夸大风险的处理方式，避免凭空为客户"发明"逾期记录。

### 2.3 遗漏修复记录

该规则最初仅覆盖98，在`feature_create.py`阶段构造衍生特征时发现遗漏96，已回溯修复`missing_handle.py`、`outlier_process.py`、`feature_create.py`三个文件，保持清洗逻辑一致。SQL视图（`00_create_view.sql`）与Python清洗流程相互独立，未自动同步该规则，已在`case_feature.sql`中单独通过WHERE条件补充排除。

---

## 3. 异常值截断规则

对应代码：`outlier_process.py`（`RevolvingUtilizationOfUnsecuredLines`截断在`feature_create.py`阶段发现遗漏后补充）

### 3.1 规则

采用 **99%分位数截断（Winsorization）**：字段中超过99%分位数的极端值，统一压缩至该分位数边界，不做删除处理。

### 3.2 具体字段

| 字段 | 99%分位数 | 截断前最大值 |
|---|---|---|
| DebtRatio | 4979.04 | 329664.0 |
| MonthlyIncome | 23000.0 | 3008750.0 |
| RevolvingUtilizationOfUnsecuredLines | 1.093 | 50708.0 |

### 3.3 业务依据

评分卡建模（WOE分箱等技术）对极端值敏感，个别离谱极端值会扭曲分箱与打分逻辑；采用截断而非删除，是为了保留样本量与其他字段信息，仅收敛数值范围。

### 3.4 遗漏修复记录

`RevolvingUtilizationOfUnsecuredLines`最初未纳入截断范围，在构造`income_debt_pressure`衍生特征时发现该字段极端值导致新特征严重失真（标准差从15.30压缩后降至0.05），回溯补充截断规则至`outlier_process.py`。

---

## 4. 衍生特征构造规则

对应代码：`feature_create.py`

| 衍生特征 | 构造方式 | 业务依据 | IV值验证结果 |
|---|---|---|---|
| total_late_times | 三个逾期次数字段求和 | 综合反映客户整体逾期严重程度，避免单一字段判断片面 | 0.566（区分力极强，效果显著） |
| income_debt_pressure | 额度使用率 ÷ (月收入+1) | 尝试衡量额度使用压力相对收入水平的比例，分母+1避免除0 | 0.001（几乎无区分力，效果不佳） |

**结论**：衍生特征并非天然有效，需用IV值等客观指标验证，不能仅凭业务直觉判断特征组合是否有价值。

---

## 5. 特征筛选规则

对应代码：`calc_iv.py`

### 5.1 规则

对所有候选特征计算IV值，按以下标准判断取舍：

| IV值范围 | 区分力评价 | 处理建议 |
|---|---|---|
| < 0.02 | 几乎无预测力 | 建议剔除 |
| 0.02 ~ 0.1 | 较弱 | 谨慎保留 |
| 0.1 ~ 0.3 | 中等 | 保留 |
| 0.3 ~ 0.5 | 较强 | 保留 |
| > 0.5 | 极强 | 保留，但需排查是否存在数据泄漏 |

### 5.2 建议剔除清单

`monthly_income_missing_flag`、`NumberRealEstateLoansOrLines`、`NumberOfDependents`、`income_debt_pressure`、`NumberOfOpenCreditLinesAndLoans`（IV值均低于0.02）。

### 5.3 需重点核实

`RevolvingUtilizationOfUnsecuredLines`（IV=1.08）区分力远超常规极强阈值，建模前需单独核实该字段计算逻辑，排除数据泄漏可能。

---

## 6. 数据集拆分规则

对应代码：`train_test_split.py`

采用分层抽样（`stratify`），按8:2拆分训练集/测试集，确保两者违约样本比例（约6.68%）与原始数据保持一致，避免随机拆分导致的样本分布偏移。拆分结果仅保存生成代码，数据文件不入库（见`.gitignore`）。

---

## 7. 代码结构说明

| 文件 | 职责 |
|---|---|
| `data_explore.py` | 探索性分析（缺失值/样本分布/极值/异常值/分组统计） |
| `missing_handle.py` | 缺失值与异常编码值处理 |
| `outlier_process.py` | 承接缺失值处理结果，做异常值截断 |
| `feature_create.py` | 承接截断结果，构造衍生特征 |
| `data_pipeline.py` | 将上述清洗与特征工程流程封装为`load_clean_data()`函数，供后续脚本统一调用，避免重复代码 |
| `train_test_split.py` | 调用`data_pipeline`，做分层抽样拆分 |
| `calc_iv.py`（位于`feature_woe/`） | 调用`data_pipeline`，批量计算特征IV值 |