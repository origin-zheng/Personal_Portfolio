"""
脚本名称:feature_create.py
业务场景:基于清洗后的信贷特征字段,构造建模用衍生变量 —— 负债收入比、逾期总次数复合特征等,
          承接outlier_process.py的缺失值处理与异常值截断结果
数据来源:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期:2026-07-22
"""

import pandas as pd

#清洗数据
df = pd.read_csv('03_Dataset/raw/cs-training.csv',index_col = 0)
median_dependents = df['NumberOfDependents'].median()
df['NumberOfDependents'] = df['NumberOfDependents'].fillna(median_dependents)
print("填充后缺失量：",df['NumberOfDependents'].isnull().sum())

df['monthly_income_missing_flag'] = df['MonthlyIncome'].isnull().astype(int)#新建一列，标记是否缺失,使用astype()，将bull转换为0,1
print('收入缺失标记为1的数量:',df['monthly_income_missing_flag'].sum())
median_monthly_income = df['MonthlyIncome'].median()
df['MonthlyIncome'] = df['MonthlyIncome'].fillna(median_monthly_income)
print("填充后缺失量：",df['MonthlyIncome'].isnull().sum())

df['NumberOfTime30-59DaysPastDueNotWorse'] = df['NumberOfTime30-59DaysPastDueNotWorse'].replace([98,96],0)
df['NumberOfTime60-89DaysPastDueNotWorse'] = df['NumberOfTime60-89DaysPastDueNotWorse'].replace([98,96],0)
df['NumberOfTimes90DaysLate'] = df['NumberOfTimes90DaysLate'].replace([98,96],0)
print('30-59逾期字段中=98的数量:',(df['NumberOfTime30-59DaysPastDueNotWorse']==98).sum())
print('60-89逾期字段中=98的数量:',(df['NumberOfTime60-89DaysPastDueNotWorse']==98).sum())
print('超过90逾期字段中=98的数量:',(df['NumberOfTimes90DaysLate']==98).sum())

debt_ratio_upper = df['DebtRatio'].quantile(0.99)
print("DebtRatio 99%分位数:",debt_ratio_upper)
df['DebtRatio'] = df['DebtRatio'].clip(upper= debt_ratio_upper)
print("截断后DebtRatio最大值:",df['DebtRatio'].max())

monthly_income_upper = df['MonthlyIncome'].quantile(0.99)
print('MonthlyIncome 99%分位数',monthly_income_upper)
df['MonthlyIncome'] = df['MonthlyIncome'].clip(upper = monthly_income_upper)
print("截断后MonthlyIncome最大值:",df['MonthlyIncome'].max())


#衍生特征1：逾期总次数
df['total_late_times'] = df['NumberOfTime30-59DaysPastDueNotWorse'] + df['NumberOfTime60-89DaysPastDueNotWorse'] + df['NumberOfTimes90DaysLate']
print("逾期总次数示例:", df['total_late_times'].describe())
print(df[df['total_late_times'] > 50][['NumberOfTime30-59DaysPastDueNotWorse', 'NumberOfTime60-89DaysPastDueNotWorse', 'NumberOfTimes90DaysLate', 'total_late_times']])
print("30-59逾期=96的数量:", (df['NumberOfTime30-59DaysPastDueNotWorse'] == 96).sum())
print("60-89逾期=96的数量:", (df['NumberOfTime60-89DaysPastDueNotWorse'] == 96).sum())
print("90天以上逾期=96的数量:", (df['NumberOfTimes90DaysLate'] == 96).sum())

#RevolvingUtilizationOfUnsecuredLines 异常值截断
revol_util_upper = df['RevolvingUtilizationOfUnsecuredLines'].quantile(0.99)
print("额度使用率99%分位数:", revol_util_upper)
df['RevolvingUtilizationOfUnsecuredLines'] = df['RevolvingUtilizationOfUnsecuredLines'].clip(upper=revol_util_upper)

#负债收入比
df['income_debt_pressure'] = df['RevolvingUtilizationOfUnsecuredLines'] / (df['MonthlyIncome'] + 1)
print("负债收入压力比示例:", df['income_debt_pressure'].describe())