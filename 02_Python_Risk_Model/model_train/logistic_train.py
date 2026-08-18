"""
脚本名称:logistic_train.py
业务场景:基于WOE转换后的训练集,使用sklearn LogisticRegression拟合标准信用评分卡逻辑回归模型,
          固定随机种子保证结果可复现
数据来源:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期:2026-08-18
"""
import pandas as pd
from sklearn.linear_model import LogisticRegression

df_train = pd.read_csv("03_Dataset/processed/train_woe.csv")
target_col = 'SeriousDlqin2yrs'
feature_cols = ['RevolvingUtilizationOfUnsecuredLines_woe',
    'NumberOfTimes90DaysLate_woe',
    'NumberOfTime30-59DaysPastDueNotWorse_woe',
    'NumberOfTime60-89DaysPastDueNotWorse_woe',
    'age_woe',
    'DebtRatio_woe',
    'MonthlyIncome_woe']

X_train = df_train[feature_cols]
Y_train = df_train[target_col]

model = LogisticRegression(
    penalty='l2',
    C=1.0,
    solver = 'lbfgs',
    random_state = 42
)

model.fit(X_train,Y_train)
coef_df = pd.DataFrame({
    'feature': feature_cols,
    'coefficient': model.coef_[0]
})
print(coef_df)
print("截距 intercept:", model.intercept_[0])