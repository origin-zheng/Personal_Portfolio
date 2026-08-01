"""
脚本名称:discrete_woe.py
业务场景:批量对候选特征做scorecardpy分箱,汇总输出各分箱的违约率/WOE/IV对照表,存档为Markdown文档,便于查阅与建模参考
数据来源:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期: 2026-08-01
"""

import pandas as pd
import scorecardpy as sc
import sys
sys.path.append("02_Python_Risk_Model/data_clean")
from data_pipeline import load_clean_data

df = load_clean_data()
target_col = 'SeriousDlqin2yrs'
feature_cols = [col for col in df.columns if col != target_col]
print(f"候选特征列表: {list(feature_cols)}")

bins = sc.woebin(df, y = target_col, x  = feature_cols)
with open("02_Python_Risk_Model/feature_woe/discrete_woe.md", 'w',encoding = "utf-8") as f:
    f.write("# 各特征WOE分箱对照表\n\n")
    for feature, table in bins.items():
        f.write(f"## {feature}\n\n")
        f.write(table.to_markdown(index=False))
        f.write("\n\n")

print("已生成discrete_woe_summary.md")