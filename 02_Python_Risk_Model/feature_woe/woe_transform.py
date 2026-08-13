"""
脚本名称: woe_transform.py
业务场景:基于scorecardpy分箱结果,将原始特征值全部替换为对应的WOE值,生成可直接用于评分卡建模的数据集
数据来源:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期: 2026-08-03
修改日期: 2026-08-13
"""

import pandas as pd
import scorecardpy as sc
import pickle

df_train = pd.read_csv("03_Dataset/processed/train_clean.csv")
df_test = pd.read_csv("03_Dataset/processed/test_clean.csv")

with open("03_Dataset/processed/woe_bins.pkl", "rb") as f:
    bins = pickle.load(f)

train_woe = sc.woebin_ply(df_train,bins)
test_woe = sc.woebin_ply(df_test, bins)

print("训练集WOE转换结果:", train_woe.shape)
print("测试集WOE转换结果:", test_woe.shape)

train_woe.to_csv("03_Dataset/processed/train_woe.csv", index=False)
test_woe.to_csv("03_Dataset/processed/test_woe.csv", index=False)
print("训练集与测试集WOE转换结果已保存")