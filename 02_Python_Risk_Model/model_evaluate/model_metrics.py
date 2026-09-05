"""
脚本名称:model_metrics.py
业务场景:对逻辑回归评分卡模型进行完整效果评估,输出AUC、KS值、十等分人群违约率曲线,
          并保存相关评估图表,用于验证模型在测试集上的区分能力与稳定性
数据来源:Kaggle - Give Me Some Credit
          https://www.kaggle.com/competitions/GiveMeSomeCredit/data
编写日期:2026-09-05
"""
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from sklearn.metrics import roc_auc_score, roc_curve


df_test = pd.read_csv("03_Dataset/processed/test_woe.csv")
target_col = 'SeriousDlqin2yrs' 
with open("03_Dataset/processed/logistic_model.pkl", "rb") as f:
    saved = pickle.load(f)

model = saved["model"]
feature_cols = saved["feature_cols"]
x_test = df_test[feature_cols]
y_test = df_test[target_col]
y_pred_proba = model.predict_proba(x_test)[:, 1]

auc = roc_auc_score(y_test, y_pred_proba)
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
ks = max(tpr-fpr)
print(f"AUC:{auc:.4f}, KS: {ks:.4f}")
eval_df = pd.DataFrame({
    'y_true': y_test.values,
    'y_pred_proba': y_pred_proba
})
eval_df['decile'] = pd.qcut(eval_df['y_pred_proba'],10,labels=False,duplicates = 'drop')
eval_df['decile'] = 9 - eval_df['decile']
decile_stat = eval_df.groupby('decile').agg(
    count = ('y_true', 'count'),
    bad_count = ('y_true', 'sum')   
)
decile_stat['bad_rate'] = decile_stat['bad_count'] / decile_stat['count']
decile_stat = decile_stat.sort_index()

print(decile_stat)

plt.figure(figsize=(8, 5))
plt.plot(decile_stat.index, decile_stat['bad_rate'], marker='o')
plt.xlabel('风险分组(0=风险最高的10%, 9=风险最低的10%)')
plt.ylabel('真实违约率')
plt.title('十等分人群违约率曲线')
plt.grid(True)
plt.savefig("02_Python_Risk_Model/visualization/decile_default_curve.png", dpi=150)
plt.show()