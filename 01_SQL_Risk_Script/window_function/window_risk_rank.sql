--同家庭客户⻛险排序
SELECT customer_id,
       num_dependents,
       ( times_30_59_days_late + times_60_89_days_late + times_90_days_late ) AS total_late_time
       ,
       RANK()
       OVER(PARTITION BY num_dependents
            ORDER BY(times_30_59_days_late + times_60_89_days_late + times_90_days_late
            ) DESC
       ) AS risk_rank_in_family
  FROM credit_customers
 WHERE times_30_59_days_late NOT IN ( 96,
                                      98 )
   AND times_60_89_days_late NOT IN ( 96,
                                      98 )
   AND times_90_days_late NOT IN ( 96,
                                   98 );

--各收⼊区间违约排名

SELECT income_group,
       default_rate,
       RANK()
       OVER(
            ORDER BY default_rate DESC
       ) AS default_rate_rank
  FROM (
    SELECT AVG(serious_dlq_2yrs) AS default_rate,
           CASE
               WHEN monthly_income IS NULL THEN
                   '无收入'
               WHEN monthly_income < 2000 THEN
                   '低收入'
               WHEN monthly_income < 5000 THEN
                   '中等收入'
               ELSE
                   '高收入'
           END AS income_group
      FROM credit_customers
     WHERE monthly_income IS NULL
        OR monthly_income <= 23000
     GROUP BY income_group
);