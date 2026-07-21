-- ============================================================
-- 脚本名称：risk_top_list.sql
-- 业务场景：提取TOP高负债、TOP多次逾期客户名单,生成风控预警清单,支持分页输出便于人工审核
-- 数据来源：Kaggle - Give Me Some Credit
--           https://www.kaggle.com/competitions/GiveMeSomeCredit/data
-- 编写日期：2026-07-21
-- ============================================================

--DebtRatio的TOP高负债客户分页1
select customer_id, age, debt_ratio, serious_dlq_2yrs
from credit_customers
order by debt_ratio desc
fetch  next 20 rows only;

--DebtRatio的TOP高负债客户分页2
select customer_id, age, debt_ratio, serious_dlq_2yrs
from credit_customers
order by debt_ratio desc
offset 20 rows fetch next 20 rows only;

-- TOP多次逾期客户分页1
select customer_id, age, times_90_days_late, serious_dlq_2yrs
from credit_customers
where times_90_days_late <> 98
order by times_90_days_late desc
fetch next 20 rows only;

---- TOP多次逾期客户分页2
select customer_id, age, times_90_days_late, serious_dlq_2yrs
from credit_customers
where times_90_days_late <> 98
order by times_90_days_late desc
offset 20 rows fetch next 20 rows only;
