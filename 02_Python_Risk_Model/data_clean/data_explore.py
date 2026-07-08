"""
脚本名称:data_explore.py
业务场景:信贷训练集数据探索性分析(EDA) —— 缺失值/样本分布/极值/异常值识别
数据来:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期:2026-07-08
"""

import pandas as pd
df = pd.read_csv("03_Dataset/raw/cs-training.csv", index_col=0)