-- ============================================================
-- 脚本名称：month_risk_dashboard.sql
-- 业务场景：整合SQL阶段全部语法,基于客户逾期次数字段构建逾期严重程度分层(M0/M1/M2/M3),输出银行月度信贷监控指标看板的分层统计基础数据
-- 数据来源：Kaggle - Give Me Some Credit
--           https://www.kaggle.com/competitions/GiveMeSomeCredit/data
-- 编写日期：2026-09-21
-- ============================================================
SELECT
    risk_level,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / SUM(COUNT(customer_id)) OVER (), 2) AS percentage
FROM (
    SELECT
        customer_id,
        CASE
            WHEN times_30_59_days_late IN (96, 98)
              OR times_60_89_days_late IN (96, 98)
              OR times_90_days_late IN (96, 98)
                THEN '数据异常'
            WHEN times_90_days_late > 0 THEN 'M3'
            WHEN times_60_89_days_late > 0 THEN 'M2'
            WHEN times_30_59_days_late > 0 THEN 'M1'
            ELSE 'M0'
        END AS risk_level
    FROM credit_customers
) AS classified
GROUP BY risk_level
ORDER BY risk_level;

