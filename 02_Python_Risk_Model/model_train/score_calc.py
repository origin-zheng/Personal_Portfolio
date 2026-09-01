"""
脚本名称:score_calc.py
业务场景:将逻辑回归系数按标准评分卡公式(score = A - B*ln(odds))换算为信用分,
          并拆解为每个特征分箱对应的分值,供业务查表使用
数据来源:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期:2026-09-01
"""
import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

df_train = pd.read_csv("03_Dataset/processed/train_woe.csv")
target_col = 'SeriousDlqin2yrs'
feature_cols = [
    'RevolvingUtilizationOfUnsecuredLines_woe',
    'NumberOfTimes90DaysLate_woe',
    'NumberOfTime30-59DaysPastDueNotWorse_woe',
    'NumberOfTime60-89DaysPastDueNotWorse_woe',
    'age_woe',
    'DebtRatio_woe',
    'MonthlyIncome_woe'
]

X_train = df_train[feature_cols]
y_train = df_train[target_col]

model = LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', random_state=42)
model.fit(X_train, y_train)
coef_df = pd.DataFrame({
    'feature':feature_cols,
    'coefficient':model.coef_[0]
})

intercept = model.intercept_[0]
base_score = 600
base_odds = 1/20
pdo = 20
B = pdo/np.log(2)
A = base_score + B *np.log(base_odds)

base_points = A - B * intercept
coef_df['points_per_woe'] = -B * coef_df['coefficient']

print(f"A={A:.2f}, B={B:.2f}")
print("base_points:", base_points)
print(coef_df)

import pickle

with open("03_Dataset/processed/woe_bins.pkl", "rb") as f:
    bins = pickle.load(f)

scorecard_tables = []

for _, row in coef_df.iterrows():
    feature_woe_name = row['feature']             
    feature_raw_name = feature_woe_name.replace('_woe', '')  
    points_per_woe = row['points_per_woe']

    bin_table = bins[feature_raw_name].copy()
    bin_table['points'] = points_per_woe * bin_table['woe']
    bin_table['feature'] = feature_raw_name

    scorecard_tables.append(bin_table[['feature', 'bin', 'woe', 'points']])

scorecard_df = pd.concat(scorecard_tables, ignore_index=True)
print(scorecard_df)

scorecard_df.to_csv("03_Dataset/processed/scorecard_final.csv", index=False)
print("评分卡已保存至 scorecard_final.csv")