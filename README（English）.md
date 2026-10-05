# Credit Risk Analysis Portfolio


## Project Structure

* `01_SQL_Risk_Script/` — SQL scripts for risk metric calculation
* `02_Python_Risk_Model/` — Python code for scorecard modelling
* `03_Dataset/` — Dataset documentation (raw data is not uploaded; see download instructions below)
* `04_Project_Report/` — Project analysis report
* `05_CheatSheet/` — FRM key-point cheat sheet

## Dataset

This project uses the public Kaggle dataset [Give Me Some Credit](https://www.kaggle.com/c/GiveMeSomeCredit/data). The raw CSV files are large and are not included in this repository. Field descriptions are in `03_Dataset/data_intro.md`. To reproduce the code, download the data from Kaggle and place it in the `03_Dataset/raw/` directory.

## Results

* **Model performance** — Logistic regression scorecard; test-set AUC 0.857, KS 0.562
* **Model features** — Selected by Information Value (IV) screening and VIF checks; 7 features retained (VIF 1.07–1.39)
* **Scorecard scaling** — Base score 600, base odds 1:20, PDO (points to double the odds) 20
* **Data leakage fix** — WOE binning was originally fitted on the full dataset. It is now fitted on the training set only, saved as `woe_bins.pkl`, and then applied separately to the training and test sets
* **Ranking ability** — The highest-risk 10% of customers have a default rate of 35.4% and capture 52.5% of all bad customers in the test set; the lowest-risk 10% have a default rate of only 0.49%

## Tech Stack

* DuckDB SQL (risk metric calculation)
* Python (pandas / numpy / scikit-learn / scorecardpy for data cleaning and modelling)
* FRM Level 1 credit risk theory (PD / LGD / EAD / EL, scorecard development workflow)

## Author

Yuanzheng Zhang — First-year Master of Data Science student at Monash University, preparing for FRM Level 1