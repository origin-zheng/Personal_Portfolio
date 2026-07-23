"""
脚本名称:train_test_split.py
业务场景：将清洗后的信贷数据集,按分层抽样方式拆分为训练集与测试集,
          保证违约样本比例在两个数据集中保持一致,用于后续模型训练与评估
数据来源:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期:2026—07-23
"""

import pandas as pd
from data_pipeline import load_clean_data

df = load_clean_data()

from sklearn.model_selection import train_test_split
train_df,test_df = train_test_split(
    df,
    test_size = 0.2,
    stratify = df['SeriousDlqin2yrs'], #按照元数据同比例分层
    random_state = 42)#固定抽取的样本每次都一样

print("训练集违约比例:", train_df['SeriousDlqin2yrs'].mean())
print("测试集违约比例:", test_df['SeriousDlqin2yrs'].mean())
print("原始数据违约比例:", df['SeriousDlqin2yrs'].mean())

train_df.to_csv("03_Dataset/processed/train_clean.csv", index=False)
test_df.to_csv("03_Dataset/processed/test_clean.csv", index=False)
print("训练集与测试集已保存")