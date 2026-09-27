# 信贷风险分析作品集

## 项目结构
- `01_SQL_Risk_Script/` — SQL风险指标计算脚本
- `02_Python_Risk_Model/` — Python评分卡建模代码
- `03_Dataset/` — 数据集说明文档（原始数据未上传，见下方下载方式）
- `04_Project_Report/` — 项目分析报告
- `05_CheatSheet/` — FRM知识点速查

## 数据集获取
本项目使用 Kaggle 公开数据集 [Give Me Some Credit](https://www.kaggle.com/c/GiveMeSomeCredit/data)。
原始CSV文件较大，未上传本仓库，详细字段说明见 `03_Dataset/data_intro.md`，
需要复现代码请自行前往 Kaggle 下载后放入 `03_Dataset/raw/` 目录。

## 技术栈
- DuckDB SQL（风险指标计算）
- Python（pandas / numpy / scikit-learn / scorecardpy，数据清洗与建模）
- FRM Level 1 信用风险理论（PD/LGD/EAD/EL、评分卡开发流程）

## 作者
张元正 Yuanzheng Zhang — Monash University 数据科学研一在读硕士，FRM Level 1 备考中
