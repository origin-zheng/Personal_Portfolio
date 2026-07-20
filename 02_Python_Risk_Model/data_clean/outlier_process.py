"""
脚本名称:outlier_process.py
业务场景:信贷训练集异常值截断处理 —— 承接missing_handle.py的缺失值处理结果,
          对MonthlyIncome、DebtRatio两个存在极端异常值的字段做分位数截断,
          使数据分布适配评分卡建模(WOE分箱等)对极端值敏感的规范要求
数据来源:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期:2026-07-20
"""
import pandas as pd

#用随机缺失处理NumberOfDependents
df = pd.read_csv('03_Dataset/raw/cs-training.csv',index_col = 0)
median_dependents = df['NumberOfDependents'].median()
df['NumberOfDependents'] = df['NumberOfDependents'].fillna(median_dependents)
print("填充后缺失量：",df['NumberOfDependents'].isnull().sum())

#用业务缺失处理MonthlyIncome
df['monthly_income_missing_flag'] = df['MonthlyIncome'].isnull().astype(int)#新建一列，标记是否缺失,使用astype()，将bull转换为0,1
print('收入缺失标记为1的数量:',df['monthly_income_missing_flag'].sum())
median_monthly_income = df['MonthlyIncome'].median()
df['MonthlyIncome'] = df['MonthlyIncome'].fillna(median_monthly_income)
print("填充后缺失量：",df['MonthlyIncome'].isnull().sum())

#逾期特征的0填充
df['NumberOfTime30-59DaysPastDueNotWorse'] = df['NumberOfTime30-59DaysPastDueNotWorse'].replace(98,0)
df['NumberOfTime60-89DaysPastDueNotWorse'] = df['NumberOfTime60-89DaysPastDueNotWorse'].replace(98,0)
df['NumberOfTimes90DaysLate'] = df['NumberOfTimes90DaysLate'].replace(98,0)
print('30-59逾期字段中=98的数量:',(df['NumberOfTime30-59DaysPastDueNotWorse']==98).sum())
print('60-89逾期字段中=98的数量:',(df['NumberOfTime60-89DaysPastDueNotWorse']==98).sum())
print('超过90逾期字段中=98的数量:',(df['NumberOfTimes90DaysLate']==98).sum())

debt_ratio_upper = df['DebtRatio'].quantile(0.99)
print("DebtRatio 99%分位数:",debt_ratio_upper)
df['DebtRatio'] = df['DebtRatio'].clip(upper= debt_ratio_upper)
print("截断后DebtRatio最大值:",df['DebtRatio'].max())