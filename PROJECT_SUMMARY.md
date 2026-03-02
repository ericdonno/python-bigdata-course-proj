# 项目总结：五大联赛球员伤病分析与预测

## 一、项目概述

本项目是「Python 玩转大数据」课程下的**足球球员伤病数据**实战项目。以欧洲五大联赛（英超、西甲、德甲、意甲、法甲）球员为对象，从数据获取、结构化建模、分析可视化到**伤病预测建模**，搭建了一条完整的大数据处理与机器学习流水线。

**核心目标**：用五大联赛球员伤病史分析伤病规律，并预测球员在指定时间窗口内是否会受伤。

---

## 二、技术栈与数据来源

| 类别 | 说明 |
|------|------|
| **语言** | Python |
| **数据来源** | Transfermarkt（transfermarkt.com），遵守 robots.txt 规则 |
| **数据处理** | pandas、numpy、ast（解析伤病史序列） |
| **爬虫** | requests、BeautifulSoup、scraper_utils（重试与分页） |
| **可视化** | matplotlib、seaborn、Plotly（玫瑰图等） |
| **机器学习** | scikit-learn（LogisticRegression、RandomForest，可选 XGBoost） |
| **交付形式** | Jupyter Notebook（.ipynb）+ 自定义 Python 模块（.py）+ JSON/CSV 数据 |

---

## 三、项目结构概览

| 阶段 | 笔记本/模块 | 主要作用 |
|------|-------------|----------|
| **数据获取** | `PART1_datafetch.ipynb` | 爬取球队/球员/伤病页，得到 injury_dict、player_dict、feature_data_dict、injury_data_dict |
| **数据结构化** | `PART2_abstraction_and_data_structure.ipynb` | 球员与伤病史抽象，得到 obj_list / obj_dict |
| **加载测试** | `PART2_(extra)_loading_objects.ipynb` | 从 JSON 反序列化并加载球员对象 |
| **分析与可视化** | `PART3_analyzing_and_visualization.ipynb` | 伤病类型/天数统计、keyword_to_category 归类、图表与玫瑰图，产出 `players_filled.csv` |
| **预测模型** | `PART4_prediction_model.ipynb` | 二分类「未来是否会受伤」：标签构造、特征工程、按球员划分、训练与评估 |
| **自定义模块** | `player.py` | 球员类、Healthy/Injured、序列化/反序列化 |
| **爬虫工具** | `scraper_utils.py` | 带重试的请求、伤病表分页解析 |

---

## 四、数据流水线

### 4.1 数据获取（PART1）

- 从五大联赛首页获取**球队列表**及球队页 URL。
- 从各球队页获取**球员列表**及球员/伤病页 URL。
- 爬取**伤病明细表**（含分页）：伤情类型、起止日期、缺阵天数、缺阵场次等。
- 产出：injury_dict、player_dict、feature_data_dict、injury_data_dict 等。

### 4.2 数据结构设计（PART2）

- **球员**：姓名、位置、身高、国籍、出场数据（场次与分钟）、伤病史序列。
- **伤病史**：Healthy/Injured（namedtuple）交替表示健康天数与伤病记录，由 `generate_injury_history` 从原始表生成。
- 支持 JSON 序列化与反序列化（obj_list_from_json、obj_dict_from_json），产出 obj_list / obj_dict。

### 4.3 分析与可视化（PART3）

- 读取 injury_data_dict、obj_list 等，用 pandas 清洗与聚合。
- 伤病类型、缺阵天数统计与异常值处理；keyword_to_category 对伤情归类（含中英文）。
- matplotlib / seaborn / Plotly 可视化，产出 `saved/players_filled.csv`（含 height 填充、injury_history 等），供 PART4 使用。

### 4.4 预测模型（PART4，已完成）

- **任务**：二分类——给定球员与预测窗口（如 30/60/90 天），预测该窗口内是否发生至少一次伤病。
- **数据**：`./saved/players_filled.csv`（约 2591 名球员），解析 injury_history 为 injury_series（偶数位健康天数、奇数位伤病天数）。
- **标签构造**：从每条伤病史时间轴的「健康期起点」作为观察点，按 horizon_days 判断窗口内是否进入伤病段 → 1/0。
- **特征**：horizon_days、position（编码）、height、nationality、出场（总场次/总分钟/场均分钟）、到观察点的伤病史统计（伤病次数、总/均/最大缺阵天数、距上次伤病天数等）。
- **划分**：按球员划分训练/验证/测试集，避免同一球员跨集泄漏。
- **模型**：LogisticRegression、RandomForest（class_weight='balanced'），可选 XGBoost。
- **评估**：准确率约 0.64，AUC-ROC 约 0.68，F1 约 0.51；含混淆矩阵与分类报告。

---

## 五、核心模块说明

### 5.1 `player.py`

- **Healthy / Injured**：namedtuple，表示健康天数或一次伤病记录。
- **Player**：name、position、height、nationality、injury_history、apparence；add_healthy/add_injured、generate_injury_history、get_inj_series 等。
- **序列化**：player_to_dict；**反序列化**：obj_list_from_json、obj_dict_from_json。

### 5.2 `scraper_utils.py`

- get_page_source、get_page_source_r（带重试与延时）、get_all_injuries_r（伤病表含分页解析）。

---

## 六、数据文件说明

| 格式 | 文件名示例 | 作用 |
|------|------------|------|
| json | injury_dict, player_dict | 伤病页/球员页 URL 映射 |
| json | feature_data_dict, injury_data_dict | 球员特征与伤病原始数据 |
| json | obj_dict, obj_list | 序列化后的球员对象 |
| json | keyword_to_category / _cn | 伤情关键词到分类的映射 |
| csv | saved/players_filled.csv | PART3 产出，PART4 输入（含 injury_series 解析用列） |
| ipynb | PART1～PART4、PART2_extra | 各阶段笔记本 |
| py | player, scraper_utils | 球员模型与爬虫工具 |

---

## 七、项目特点与收获

1. **完整的数据与建模链路**：爬取 → 清洗与抽象 → 持久化 → 分析可视化 → **标签构造与特征工程 → 二分类预测与评估**，覆盖大数据与机器学习常见环节。
2. **清晰的数据建模**：namedtuple + Player 类对「球员」与「伤病时间线」建模，便于扩展与复用。
3. **工程化考虑**：爬虫重试与分页、异常值处理、按球员划分防止泄漏、类别不平衡（class_weight）。
4. **可复现性**：Notebook 分阶段、数据与代码分离（JSON/CSV + .py），便于复现与迭代。
5. **文档配套**：`INJURY_PREDICTION_SUGGESTIONS.md` 明确任务定义、标签构造、特征与评估方式，与 PART4 实现一致。

---

## 八、预测模型小结（PART4）

- **目标**：未来 H 天内是否受伤（二分类）。
- **数据规模**：约 2591 名球员，样本按健康段起点 × 预测窗口生成，按球员划分 train/val/test。
- **表现**：AUC ≈ 0.68，准确率 ≈ 0.64，F1 ≈ 0.51；可作为基线，后续可通过特征工程、采样或阈值优化提升。
- **扩展**：可接入伤病严重程度（回归/有序分类）、下次伤病类型（多分类）、复发风险等（参见 INJURY_PREDICTION_SUGGESTIONS.md）。

---

## 九、后续可拓展方向

- **模型与特征**：更多特征（如伤情类型编码、近期健康/伤病段统计）、超参调优、XGBoost/LightGBM 稳定接入；阈值与业务指标（漏报/误报）调优。
- **其他预测任务**：伤病严重程度、下次伤病类型、复发风险（见 INJURY_PREDICTION_SUGGESTIONS.md）。
- **爬虫与更新**：脚本化爬取、增量或定时更新新赛季数据。
- **可视化与报告**：按联赛、位置、伤情类别的多维图表与看板；模型可解释性（特征重要性、SHAP 等）。

---

*本总结基于当前仓库中的 Notebook、Python 模块与 INJURY_PREDICTION_SUGGESTIONS.md 整理，反映项目最新状态（含 PART4 预测模型完成情况）。*
