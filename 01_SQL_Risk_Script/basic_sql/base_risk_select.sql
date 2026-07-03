-- ============================================================
-- 脚本名称：base_risk_select.sql
-- 业务场景：信贷客户风险分层与基础风险指标探查（Day 1）
-- 数据来源：Kaggle - Give Me Some Credit
--           https://www.kaggle.com/competitions/GiveMeSomeCredit/data
-- 编写日期：2026-07-03
-- 字段说明：
--   serious_dlq_2yrs      -- 目标变量，2年内是否发生严重逾期(90天+) 1=是 0=否
--   age                   -- 年龄
--   times_30_59_days_late -- 过去2年内30-59天逾期次数
--   times_90_days_late    -- 过去2年内90天以上逾期次数
--   debt_ratio            -- 负债率
--   monthly_income        -- 月收入
-- ============================================================
--客户分组及对应的逾期率
select 
case
when 18 <= age and age < 30 then '18-29'
when 30 <= age and age < 40 then '30-39'
when 40 <= age and age < 50 then '40-49'
when 50 <= age and age < 60 then '50-59'
when 60 <= age and age < 70 then '60-69'
when 70 <= age and age < 80 then '70-79'
when 80 <= age and age < 90 then '80-89'
else '90+'
end as age_group,
count(customer_id) as customer_count,
round(avg(serious_dlq_2yrs) * 100, 2) || '%' as serious_dlq_2yrs_rate
from credit_customers
group by age_group
order by age_group;

--轻度预期客户(有过30-59天的逾期记录，但从来没有出现过90天以上的严重逾期。)
select customer_id, age, times_30_59_days_late, times_90_days_late,'lightly_delinquent' as risk_level
from credit_customers
where times_30_59_days_late > 0 and  times_90_days_late = 0
union all
--严重预期客户(有过90天以上的严重逾期记录。)
select customer_id, age, times_30_59_days_late, times_90_days_late, 'seriously_delinquent' as risk_level
from credit_customers
where times_90_days_late > 0;