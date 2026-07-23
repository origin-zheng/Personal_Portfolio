"""
脚本名称:data_pipeline.py
业务场景:信贷训练集清洗与特征工程流程封装 —— 整合缺失值处理、异常值截断、衍生特征构造,
          供后续建模相关脚本(如train_test_split.py)统一调用,避免重复代码
数据来源:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期:2027-07-23
"""
import pandas as pd

def load_clean_data():
    df = pd.read_csv('03_Dataset/raw/cs-training.csv',index_col=0)
    median_dependents = df['NumberOfDependents'].median()
    df['NumberOfDependents'] = df['NumberOfDependents'].fillna(median_dependents)
    df['monthly_income_missing_flag'] = df['MonthlyIncome'].isnull().astype(int)#新建一列，标记是否缺失,使用astype()，将bull转换为0,1
    median_monthly_income = df['MonthlyIncome'].median()
    df['MonthlyIncome'] = df['MonthlyIncome'].fillna(median_monthly_income)
    df['NumberOfTime30-59DaysPastDueNotWorse'] = df['NumberOfTime30-59DaysPastDueNotWorse'].replace([98,96],0)
    df['NumberOfTime60-89DaysPastDueNotWorse'] = df['NumberOfTime60-89DaysPastDueNotWorse'].replace([98,96],0)
    df['NumberOfTimes90DaysLate'] = df['NumberOfTimes90DaysLate'].replace([98,96],0)
    debt_ratio_upper = df['DebtRatio'].quantile(0.99)
    df['DebtRatio'] = df['DebtRatio'].clip(upper= debt_ratio_upper)
    monthly_income_upper = df['MonthlyIncome'].quantile(0.99)
    df['MonthlyIncome'] = df['MonthlyIncome'].clip(upper = monthly_income_upper)
    df['total_late_times'] = df['NumberOfTime30-59DaysPastDueNotWorse'] + df['NumberOfTime60-89DaysPastDueNotWorse'] + df['NumberOfTimes90DaysLate']
    revol_util_upper = df['RevolvingUtilizationOfUnsecuredLines'].quantile(0.99)
    df['RevolvingUtilizationOfUnsecuredLines'] = df['RevolvingUtilizationOfUnsecuredLines'].clip(upper=revol_util_upper)
    df['income_debt_pressure'] = df['RevolvingUtilizationOfUnsecuredLines'] / (df['MonthlyIncome'] + 1)
    return df