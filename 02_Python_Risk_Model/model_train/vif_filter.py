"""
脚本名称:vif_filter.py
业务场景:对WOE转换后的建模数据集计算VIF(方差膨胀因子),检测并剔除存在多重共线性问题的特征
数据来源:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期:2026-08-04
"""

import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor

df_woe = pd.read_csv('03_Dataset/processed/woe_transformed.csv')
print(df_woe.shape)

target_col = 'SeriousDlqin2yrs'
exclude_cols = [
    target_col,
    'total_late_times_woe',              # 与三个逾期分项字段共线,VIF=9.6
    'income_debt_pressure_woe',          # IV=0.001,几乎无区分力
    'NumberRealEstateLoansOrLines_woe',  # IV<0.02
    'NumberOfDependents_woe',            # IV<0.02
    'NumberOfOpenCreditLinesAndLoans_woe', # IV<0.02
    'monthly_income_missing_flag_woe',   # IV<0.02
]
feature_cols = [col for col in df_woe.columns if col not in exclude_cols]
x = df_woe[feature_cols]

vif_data = pd.DataFrame()
vif_data['feature'] = x.columns
vif_data['VIF'] = [variance_inflation_factor(x.values, i) for i in range(x.shape[1])]

vif_data = vif_data.sort_values('VIF', ascending=False)
print(vif_data)