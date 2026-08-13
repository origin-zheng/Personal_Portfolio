"""
脚本名称:woe_bin.py
业务场景:使用scorecardpy对收入(MonthlyIncome)、负债率(DebtRatio)做自动分箱,
          结合人工业务约束调整分箱边界,用于评分卡建模的WOE转换
数据来源:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期:2026-07-30
修改日期:2026-08-13
"""

import pandas as pd
import scorecardpy as sc
import pickle

df_train = pd.read_csv("03_Dataset/processed/train_clean.csv")

target_col = "SeriousDlqin2yrs"
feature_cols = [col for col in df_train.columns if col != target_col]

breaks_list = {
    'DebtRatio': [0.4, 0.55, 0.7, 2, 5],
    'NumberOfTime60-89DaysPastDueNotWorse': [1, 2]
}

bins = sc.woebin(df_train,y = target_col, x = feature_cols, breaks_list = breaks_list, count_distr_limit = 0.001)

print(bins['NumberOfTime60-89DaysPastDueNotWorse'])
print(bins['DebtRatio'])


with open("03_Dataset/processed/woe_bins.pkl", "wb") as f:
    pickle.dump(bins, f)

print("分箱规则已保存至 woe_bins.pkl")



