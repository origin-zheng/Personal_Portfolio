-- ============================================================
-- 脚本名称：multi_condition.sql
-- 业务场景：多条件组合风险筛选与信贷名单划分
-- 数据来源：Kaggle - Give Me Some Credit
--           https://www.kaggle.com/competitions/GiveMeSomeCredit/data
-- 编写日期：2026-07-07
-- ============================================================

--高负债客户（负债率大于0.8且年龄在30岁以上的客户）
select customer_id,age,debt_ratio,monthly_income
from credit_customers
where debt_ratio>0.8 and age>30 and monthly_income is not null;

