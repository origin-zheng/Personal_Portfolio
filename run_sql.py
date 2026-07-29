import duckdb

with open("01_SQL_Risk_Script/basic_sql/00_create_view.sql", encoding="utf-8") as f:
    duckdb.sql(f.read())

with open("01_SQL_Risk_Script/window_function/window_risk_rank.sql", encoding="utf-8") as f:
    result = duckdb.sql(f.read())
    result.show()