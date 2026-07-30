"""
脚本名称:woe_bin.py
业务场景:使用scorecardpy对收入(MonthlyIncome)、负债率(DebtRatio)做自动分箱,
          结合人工业务约束调整分箱边界,用于评分卡建模的WOE转换
数据来源:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期:2026-07-30
"""

import pandas as pd
import scorecardpy as sc
import sys
sys.path.append("02_Python_Risk_Model/data_clean")
from data_pipeline  import load_clean_data

df = load_clean_data()


#自动分箱
bins = sc.woebin(df, y ='SeriousDlqin2yrs',x = ['MonthlyIncome', 'DebtRatio'])
print(bins)
