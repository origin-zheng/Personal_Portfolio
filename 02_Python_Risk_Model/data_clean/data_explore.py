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

#正负样本分布
target_distribution = df['SeriousDlqin2yrs'].value_counts()
target_distribution_pct = round((target_distribution/len(df))*100,2)
target_distribution_df = pd.DataFrame({
    '样本数量':target_distribution,
    '样本占比(%)':target_distribution_pct}).reset_index(names='逾期标签')
print(target_distribution_df)

#字段极值
extremes_df = pd.DataFrame({
    '最小值':df.min(),
    '最大值':df.max()
})
print(extremes_df)

#异常值识别
print('信用额度使用率 > 1的记录数 ',(df['RevolvingUtilizationOfUnsecuredLines'] > 1).sum())
print('age = 0 的记录数',(df['age'] == 0).sum())
print("30-59天逾期次数=98的记录数:", (df['NumberOfTime30-59DaysPastDueNotWorse'] == 98).sum())
print("30-59天逾期次数>10的记录数:", (df['NumberOfTime30-59DaysPastDueNotWorse'] > 10).sum())
print("负债率>1的记录数:", (df['DebtRatio'] > 1).sum())
print("负债率>1且收入缺失的记录数:", ((df['DebtRatio'] > 1) & (df['MonthlyIncome'].isnull())).sum())
print("60-89天逾期次数=98的记录数:", (df['NumberOfTime60-89DaysPastDueNotWorse'] == 98).sum())
print("60-89天逾期次数>10的记录数:", (df['NumberOfTime60-89DaysPastDueNotWorse'] > 10).sum())
print("超过90天逾期次数=98的记录数:", (df['NumberOfTimes90DaysLate'] == 98).sum())
print("超过90天逾期次数>10的记录数:", (df['NumberOfTimes90DaysLate'] > 10).sum())
print("三个逾期字段同时=98的记录数:", (
    (df['NumberOfTime30-59DaysPastDueNotWorse'] == 98) &
    (df['NumberOfTime60-89DaysPastDueNotWorse'] == 98) &
    (df['NumberOfTimes90DaysLate'] == 98)
).sum())
