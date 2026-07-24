-- ============================================================
-- 脚本名称：case_feature.sql
-- 业务场景：通过CASE WHEN对负债率、逾期次数、收入三个维度分段,生成分层风险标签,用于信贷风险画像
-- 数据来源：Kaggle - Give Me Some Credit
--           https://www.kaggle.com/competitions/GiveMeSomeCredit/data
-- 编写日期：2026-07-24
-- ============================================================

--负债率分层
SELECT customer_id,
       debt_ratio,
       CASE
           WHEN debt_ratio < 0.2 THEN
               '低负债率'
           WHEN debt_ratio < 0.5 THEN
               '中负债率'
           ELSE
               '高负债率'
       END AS debt_risk_level
  FROM credit_customers;

--逾期分层
SELECT customer_id,
       times_30_59_days_late + times_60_89_days_late + times_90_days_late AS total_late_time
       ,
       CASE
           WHEN ( times_30_59_days_late + times_60_89_days_late + times_90_days_late ) = 0 THEN
               '无逾期'
           WHEN ( times_30_59_days_late + times_60_89_days_late + times_90_days_late ) < 4 THEN
               '轻度逾期风险'
           ELSE
               '重度逾期风险'
       END AS late_risk_level
  FROM credit_customers
 WHERE times_30_59_days_late NOT IN ( 96,
                                      98 )
   AND times_60_89_days_late NOT IN ( 96,
                                      98 )
   AND times_90_days_late NOT IN ( 96,
                                   98 );

--收入分层
SELECT customer_id,
       monthly_income,
       CASE
           WHEN monthly_income IS NULL THEN
               '收入未知'
           WHEN monthly_income < 2000 THEN
               '低收入'
           WHEN monthly_income < 5000 THEN
               '中等收入'
           ELSE
               '高收入'
       END AS income_risk_level
  FROM credit_customers;


--合并三个表格
SELECT customer_id,
       debt_ratio,
       CASE
           WHEN debt_ratio < 0.2 THEN
               '低负债率'
           WHEN debt_ratio < 0.5 THEN
               '中负债率'
           ELSE
               '高负债率'
       END AS debt_risk_level,
       times_30_59_days_late + times_60_89_days_late + times_90_days_late AS total_late_times
       ,
       CASE
           WHEN ( times_30_59_days_late + times_60_89_days_late + times_90_days_late ) = 0  THEN
               '无逾期'
           WHEN ( times_30_59_days_late + times_60_89_days_late + times_90_days_late ) < 4 THEN
               '轻度逾期风险'
           ELSE
               '重度逾期风险'
       END AS late_risk_level,
       monthly_income,
       CASE
           WHEN monthly_income IS NULL THEN
               '收入未知'
           WHEN monthly_income < 2000 THEN
               '低收入'
           WHEN monthly_income < 5000 THEN
               '中等收入'
           ELSE
               '高收入'
       END AS income_risk_level
  FROM credit_customers
 WHERE times_30_59_days_late NOT IN ( 96,
                                      98 )
   AND times_60_89_days_late NOT IN ( 96,
                                      98 )
   AND times_90_days_late NOT IN ( 96,
                                   98 );
