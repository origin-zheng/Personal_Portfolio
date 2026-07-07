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

--多段逾期（30-59天、60-89天、90天以上里，至少有两种类型都发生过）
select customer_id,times_30_59_days_late,times_60_89_days_late,times_90_days_late
from credit_customers
where (case when times_30_59_days_late>0 then 1 else 0 end +
       case when times_60_89_days_late>0 then 1 else 0 end +
       case when times_90_days_late>0 then 1 else 0 end) >=2;

--缺失收入样本过滤(筛出 monthly_income 是缺失值（NULL）的客户群体)
select customer_id, age, debt_ratio, monthly_income, serious_dlq_2yrs
from credit_customers
where monthly_income is null;


--(统计monthly_income缺失组 vs 非缺失组的违约率对比)
select 
case when monthly_income is null then 'missing' else'not missing' end as income_status,
count(customer_id) as customer_count,
round(avg(serious_dlq_2yrs)*100,2) || '%' as default_rate
from credit_customers
group by income_status
order by income_status;

--信贷白名单/黑名单区分
select 
case 
when times_60_89_days_late>0 or times_90_days_late > 0 or monthly_income is null or debt_ratio > 0.8 then 'blacklist'
when times_30_59_days_late = 0 and times_60_89_days_late = 0 and times_90_days_late = 0 and debt_ratio < 0.3 then 'whitelist'
else 'greylist' end as credit_list_category,
count(customer_id) as customer_count,
round(avg(serious_dlq_2yrs)*100,2) || '%' as default_rate
from credit_customers
group by credit_list_category
order by credit_list_category;
