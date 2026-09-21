-- ============================================================
-- 脚本名称：top_risk_customers.sql
-- 业务场景：整合SQL阶段全部语法,排除96/98数据异常客户后,按总逾期次数对客户进行风险排名,输出TOP风险客户名单,供银行月度信贷监控看板中"催收清单"使用
-- 数据来源：Kaggle - Give Me Some Credit
--           https://www.kaggle.com/competitions/GiveMeSomeCredit/data
-- 编写日期：2026-09-21
-- ============================================================
WITH classified AS (
    SELECT
        customer_id,
        times_30_59_days_late,
        times_60_89_days_late,
        times_90_days_late,
        CASE
            WHEN times_30_59_days_late IN (96, 98)
              OR times_60_89_days_late IN (96, 98)
              OR times_90_days_late IN (96, 98)
                THEN '数据异常'
            ELSE '正常'
        END AS data_flag
    FROM credit_customers
),
ranked AS (
    SELECT
        customer_id,
        times_30_59_days_late,
        times_60_89_days_late,
        times_90_days_late,
        (times_30_59_days_late + times_60_89_days_late + times_90_days_late) AS total_late_times,
        RANK() OVER (ORDER BY (times_30_59_days_late + times_60_89_days_late + times_90_days_late) DESC) AS risk_rank
    FROM classified
    WHERE data_flag = '正常'
)
SELECT *
FROM ranked
WHERE risk_rank <= 20
ORDER BY risk_rank;