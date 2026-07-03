CREATE OR REPLACE VIEW credit_customers AS
SELECT
    row_number() OVER (ORDER BY (SELECT NULL)) AS customer_id,
    "SeriousDlqin2yrs" AS serious_dlq_2yrs,
    "RevolvingUtilizationOfUnsecuredLines" AS revolving_utilization,
    "age" AS age,
    "NumberOfTime30-59DaysPastDueNotWorse" AS times_30_59_days_late,
    "DebtRatio" AS debt_ratio,
    TRY_CAST("MonthlyIncome" AS DOUBLE) AS monthly_income,
    "NumberOfOpenCreditLinesAndLoans" AS open_credit_lines,
    "NumberOfTimes90DaysLate" AS times_90_days_late,
    "NumberRealEstateLoansOrLines" AS real_estate_loans,
    "NumberOfTime60-89DaysPastDueNotWorse" AS times_60_89_days_late,
    TRY_CAST("NumberOfDependents" AS DOUBLE) AS num_dependents
FROM read_csv_auto('03_Dataset/raw/cs-training.csv');