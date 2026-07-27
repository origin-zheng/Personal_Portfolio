"""
脚本名称:calc_iv.py
业务场景:批量计算所有候选特征的IV值(信息价值),用于评估特征区分力,剔除区分力弱(IV<0.02)的变量
数据来源:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期: 2026-07-27
"""

import pandas as pd
import numpy as np
import sys #sys.path.append 的标准很简单：先看两个文件是不是在同一个文件夹，同文件夹不用加，不同文件夹才需要加
sys.path.append("02_Python_Risk_Model/data_clean")
from data_pipeline import load_clean_data

df = load_clean_data()
def calc_iv(df, feature_col, target_col='SeriousDlqin2yrs', bins=5):
    df_temp = df[[feature_col, target_col]].copy()
    
    # 数值型分箱,非数值型(比如已经是分类的字段)直接用原始值分组
    if pd.api.types.is_numeric_dtype(df_temp[feature_col]):
        df_temp['bin'] = pd.cut(df_temp[feature_col], bins=bins, duplicates='drop')
    else:
        df_temp['bin'] = df_temp[feature_col]
    
    stat = df_temp.groupby('bin', observed=True)[target_col].agg(['count', 'sum'])
    stat['bad'] = stat['sum']
    stat['good'] = stat['count'] - stat['sum']
    
    total_bad = stat['bad'].sum()
    total_good = stat['good'].sum()
    
    stat['bad_rate'] = stat['bad'] / total_bad
    stat['good_rate'] = stat['good'] / total_good
    
    # 避免除0或log(0)报错,给0值加一个极小数
    stat['bad_rate'] = stat['bad_rate'].replace(0, 0.0001)
    stat['good_rate'] = stat['good_rate'].replace(0, 0.0001)
    
    stat['woe'] = np.log(stat['good_rate'] / stat['bad_rate'])
    stat['iv_component'] = (stat['good_rate'] - stat['bad_rate']) * stat['woe']
    
    return stat['iv_component'].sum()
print("age的IV值(函数版):", calc_iv(df, 'age'))

df['age_bin'] = pd.cut(df['age'],bins=5)
print(df['age_bin'].value_counts()) #.value_counts 了解分箱效果
information_value_table = df.groupby('age_bin')['SeriousDlqin2yrs'].agg(['count','sum'])
print(information_value_table)

information_value_table['bad'] =information_value_table['sum']
information_value_table['good'] = information_value_table['count'] - information_value_table['bad']
total_bad = information_value_table['bad'].sum()
total_good = information_value_table['good'].sum()
information_value_table['bad_rate'] = information_value_table['bad']/ total_bad
information_value_table['good_rate'] = information_value_table['good']/ total_good
print(information_value_table)

information_value_table['WOE'] = np.log(information_value_table['bad_rate']/information_value_table['good_rate'])      # WOE(weight of evidence) = ln((bad/bad_total)\(good/good_total))
information_value_table['IV_component'] = (information_value_table['bad_rate'] - information_value_table['good_rate']) * information_value_table['WOE']     # IV = Σ（bad_rate - good_rate) * WOE
print(information_value_table)
total_IV = information_value_table['IV_component'].sum()
print("age特征的总IV值:", total_IV)