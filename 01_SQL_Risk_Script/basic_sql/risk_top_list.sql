-- ============================================================
-- 脚本名称：risk_top_list.sql
-- 业务场景：提取TOP高负债、TOP多次逾期客户名单,生成风控预警清单,支持分页输出便于人工审核
-- 数据来源：Kaggle - Give Me Some Credit
--           https://www.kaggle.com/competitions/GiveMeSomeCredit/data
-- 编写日期：2026-07-21
-- ============================================================

--DebtRatio的TOP高负债客户分页1
SELECT customer_id,
       age,
       debt_ratio,
       serious_dlq_2yrs
  FROM credit_customers
 ORDER BY debt_ratio DESC
 FETCH NEXT 20 ROWS ONLY;

--DebtRatio的TOP高负债客户分页2
SELECT customer_id,
       age,
       debt_ratio,
       serious_dlq_2yrs
  FROM credit_customers
 ORDER BY debt_ratio DESC
OFFSET 20 ROWS FETCH NEXT 20 ROWS ONLY;

-- TOP多次逾期客户分页1
SELECT customer_id,
       age,
       times_90_days_late,
       serious_dlq_2yrs
  FROM credit_customers
 WHERE times_90_days_late <> 98
 ORDER BY times_90_days_late DESC
 FETCH NEXT 20 ROWS ONLY;

-- TOP多次逾期客户分页2
SELECT customer_id,
       age,
       times_90_days_late,
       serious_dlq_2yrs
  FROM credit_customers
 WHERE times_90_days_late <> 98
 ORDER BY times_90_days_late DESC
OFFSET 20 ROWS FETCH NEXT 20 ROWS ONLY;

--最终风险预警表
SELECT customer_id,
       age,
       times_30_59_days_late,
       times_60_89_days_late,
       times_90_days_late,
       ( times_30_59_days_late + times_60_89_days_late + times_90_days_late ) AS total_late_times
       ,
       serious_dlq_2yrs
  FROM credit_customers
 WHERE times_30_59_days_late <> 98
   AND times_60_89_days_late <> 98
   AND times_90_days_late <> 98
 ORDER BY total_late_times DESC
 FETCH NEXT 20 ROWS ONLY;
