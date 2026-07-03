import duckdb

with open("01_SQL_Risk_Script/basic_sql/00_create_view.sql", encoding="utf-8") as f:
    duckdb.sql(f.read())

with open("01_SQL_Risk_Script/basic_sql/base_risk_select.sql", encoding="utf-8") as f:
    result = duckdb.sql(f.read())
    result.show()