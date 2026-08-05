"""
脚本名称: woe_transform.py
业务场景:基于scorecardpy分箱结果,将原始特征值全部替换为对应的WOE值,生成可直接用于评分卡建模的数据集
数据来源:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期: 2026-08-03
"""

import pandas as pd
import scorecardpy as sc
import sys
sys.path.append("02_Python_Risk_Model/data_clean")
from data_pipeline import load_clean_data

df = load_clean_data()
target_col = 'SeriousDlqin2yrs'
feature_cols = [col for col in df.columns if col != target_col]

breaks_list = {
    'NumberOfTime60-89DaysPastDueNotWorse': [1, 2]
}

bins = sc.woebin(df, y = target_col, x = feature_cols, breaks_list=breaks_list,
    count_distr_limit=0.001 )
df_woe = sc.woebin_ply(df,bins)
print(df_woe.head())
print(df_woe.shape)
df_woe.to_csv("03_Dataset/processed/woe_transformed.csv", index=False)
print("saved")
print(bins['NumberOfTime60-89DaysPastDueNotWorse'])
df_woe = pd.read_csv('03_Dataset/processed/woe_transformed.csv')
print(df_woe['NumberOfTime60-89DaysPastDueNotWorse_woe'].value_counts())