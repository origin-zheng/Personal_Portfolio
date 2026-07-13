"""
脚本名称:data_explore.py
业务场景:信贷训练集数据探索性分析(EDA) —— 缺失值/样本分布/极值/异常值识别
数据来:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期:2026-07-13
"""
#读取训练集
import pandas as pd
df = pd.read_csv("03_Dataset/raw/cs-training.csv", index_col=0)

#缺失值统计
missing_count = df.isnull().sum()
missing_pct = round((missing_count/len(df))*100,2)
missing_df = pd.DataFrame({
    '缺失数量':missing_count,
    '缺失百分数(%)':missing_pct
})
print(missing_df)