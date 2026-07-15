-- ============================================================
-- 脚本名称：group_risk_stat.sql
-- 业务场景：按家庭受抚养人数、90天以上逾期次数分组统计违约率与平均负债率
-- 数据来源：Kaggle - Give Me Some Credit
--           https://www.kaggle.com/competitions/GiveMeSomeCredit/data
-- 编写日期：2026-07-15
-- 备注：本分析已在Python阶段(02_Python_Risk_Model/data_clean/data_explore.py)
--       用pandas groupby实现过一次，此处用SQL重新实现相同逻辑，用于对比两种工具的写法
-- ============================================================

--按家庭人数分组统计违约率与平均负债率
select 
num_dependents,
count(num_dependents) as customer_count,
round(avg(serious_dlq_2yrs)*100,2) || '%' as default_rate,
round(avg(debt_ratio)*100,2) || '%' as avg_debt_ratio
from credit_customers
group by num_dependents
order by num_dependents;

--按逾期次数分组
SELECT
times_90_days_late,
count(times_90_days_late) as  customer_count,
round(avg(serious_dlq_2yrs)*100,2) || '%' as default_rate,
round(avg(debt_ratio)*100,2) || '%' as avg_debt_ratio
from credit_customers
group by times_90_days_late
order by times_90_days_late;


