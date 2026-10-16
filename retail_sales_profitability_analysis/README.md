# Retail Sales & Profitability Analysis

Beginner-friendly end-to-end Data Analyst portfolio project using Python, Pandas, SQL, Matplotlib/Seaborn, and Power BI.

## Project objective
Analyze retail transactions to understand sales, profit, product categories, regional performance, monthly trends, and discount impact. Turn the analysis into business recommendations.

## Project structure
```text
retail_sales_profitability_analysis/
├── data/
│   └── README.md
├── notebooks/
│   └── retail_sales_analysis.py
├── sql/
│   └── analysis_queries.sql
├── outputs/
│   └── .gitkeep
├── requirements.txt
├── run_analysis.py
└── README.md
```

## Dataset
This project does not redistribute a third-party dataset. Download the Sample Superstore dataset from:
https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

Extract the CSV into `data/`. The script searches for a CSV in `data/` automatically. The expected columns include fields such as `Sales`, `Profit`, `Quantity`, `Discount`, `Category`, `Sub-Category`, `Region`, `Order Date`, and `Segment`. Column capitalization is normalized where possible.

If the downloaded file uses a different column naming convention, review `run_analysis.py` and update the column mappings.

## Run with Google Colab
1. Open https://colab.research.google.com/
2. Upload `run_analysis.py` or paste its contents into a notebook cell.
3. Upload the dataset CSV when prompted, or upload it to the `data/` folder if working locally.
4. Run the script.

## Run locally
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python run_analysis.py
```

## Outputs
The script creates:
- `outputs/category_sales.png`
- `outputs/monthly_sales.png`
- `outputs/region_profit.png`
- `outputs/category_summary.csv`
- `outputs/monthly_summary.csv`
- `outputs/region_summary.csv`
- `outputs/cleaned_data.csv`

## Suggested Power BI dashboard
Import `cleaned_data.csv` and build:
- KPI cards: Total Sales, Total Profit, Total Orders, Profit Margin
- Line chart: Sales by month
- Bar chart: Sales by category
- Bar chart: Profit by region
- Table: Sub-category sales and profit
- Slicers: Order Date, Region, Category, Segment

## Example questions to answer
1. Which category has the highest sales?
2. Which category has the highest profit?
3. Which region contributes the most profit?
4. How do sales change month by month?
5. Which sub-categories lose money?
6. Are higher discounts associated with lower profit?

## Portfolio guidance
Do not claim results until you run the analysis on the dataset. In your README or report, include your actual findings, charts, and specific recommendations.
