from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "outputs"
DEFAULT_CSV_PATH = Path(r"C:\Users\Asus\Downloads\archive (7)\Sample - Superstore.csv")

ALIASES = {
    "order date": "Order Date",
    "order_date": "Order Date",
    "sales": "Sales",
    "profit": "Profit",
    "quantity": "Quantity",
    "discount": "Discount",
    "category": "Category",
    "sub-category": "Sub-Category",
    "sub_category": "Sub-Category",
    "region": "Region",
    "segment": "Segment",
    "order id": "Order ID",
    "order_id": "Order ID",
    "product name": "Product Name",
    "product_name": "Product Name",
}

def find_csv():
    candidates = []

    if DEFAULT_CSV_PATH.exists():
        candidates.append(DEFAULT_CSV_PATH)

    if DATA_DIR.exists():
        candidates.extend(DATA_DIR.glob("*.csv"))

    unique_candidates = []
    seen = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved not in seen:
            unique_candidates.append(candidate)
            seen.add(resolved)

    if not unique_candidates:
        print("No CSV found in the configured locations.")
        print("Expected file:", DEFAULT_CSV_PATH)
        print("Or place the CSV in:", DATA_DIR)
        sys.exit(1)

    return unique_candidates[0]

def load_data(path):
    # Try common encodings; many Superstore files use latin1.
    for encoding in ("utf-8", "latin1", "cp1252"):
        try:
            df = pd.read_csv(path, encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
    df.columns = [str(c).strip() for c in df.columns]
    rename = {}
    for col in df.columns:
        key = col.strip().lower().replace("  ", " ")
        if key in ALIASES:
            rename[col] = ALIASES[key]
    df = df.rename(columns=rename)

    required = ["Sales", "Profit", "Category"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns: {missing}. Found columns: {df.columns.tolist()}"
        )

    for col in ("Sales", "Profit", "Quantity", "Discount"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

    # Preserve the raw file; only remove exact duplicate rows in the analysis copy.
    before = len(df)
    df = df.drop_duplicates().copy()
    print(f"Rows loaded: {before:,}")
    print(f"Exact duplicate rows removed: {before - len(df):,}")
    print(f"Rows after deduplication: {len(df):,}")
    print("\nMissing values by column:\n", df.isna().sum().to_string())
    return df

def save_chart(series, title, xlabel, ylabel, filename, kind="bar"):
    if series.empty:
        return

    plot_kwargs = {"figsize": (9, 5)}
    if kind == "line":
        plot_kwargs["marker"] = "o"

    ax = series.plot(kind=kind, **plot_kwargs)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    OUT_DIR.mkdir(exist_ok=True)
    plt.savefig(OUT_DIR / filename, dpi=150)
    plt.close()
    print(f"Saved chart: outputs/{filename}")

def main():
    OUT_DIR.mkdir(exist_ok=True)
    path = find_csv()
    print("Reading:", path.name)
    df = load_data(path)

    print("\n=== Dataset preview ===")
    print(df.head().to_string(index=False))
    print("\nShape:", df.shape)
    print("\n=== Overall KPIs ===")
    print(f"Total sales:  {df['Sales'].sum():,.2f}")
    print(f"Total profit: {df['Profit'].sum():,.2f}")
    if "Quantity" in df.columns:
        print(f"Total quantity: {df['Quantity'].sum():,.0f}")
    if "Order ID" in df.columns:
        print(f"Unique orders: {df['Order ID'].nunique():,}")
    if df["Sales"].sum() != 0:
        print(f"Profit margin: {df['Profit'].sum() / df['Sales'].sum():.2%}")

    category_cols = {"Category", "Sales", "Profit"}
    if category_cols.issubset(df.columns):
        category = df.groupby("Category", dropna=False).agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
        ).sort_values("Total_Sales", ascending=False)
        category.to_csv(OUT_DIR / "category_summary.csv")
        print("\n=== Category summary ===\n", category.to_string())
        save_chart(category["Total_Sales"], "Total Sales by Category",
                   "Category", "Sales", "category_sales.png")

    if "Region" in df.columns:
        region = df.groupby("Region", dropna=False).agg(
            Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum")
        ).sort_values("Total_Profit", ascending=False)
        region.to_csv(OUT_DIR / "region_summary.csv")
        print("\n=== Region summary ===\n", region.to_string())
        save_chart(region["Total_Profit"], "Total Profit by Region",
                   "Region", "Profit", "region_profit.png")

    if "Order Date" in df.columns:
        dated = df.dropna(subset=["Order Date"]).copy()
        if not dated.empty:
            dated["Month"] = dated["Order Date"].dt.to_period("M").astype(str)
            monthly = dated.groupby("Month").agg(
                Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum")
            ).sort_index()
            monthly.to_csv(OUT_DIR / "monthly_summary.csv")
            save_chart(monthly["Total_Sales"], "Monthly Sales Trend",
                       "Month", "Sales", "monthly_sales.png", kind="line")

    # Save cleaned dataset for importing into Power BI.
    df.to_csv(OUT_DIR / "cleaned_data.csv", index=False)
    print("\nSaved cleaned data and summaries in the outputs/ folder.")
    print("Next: import outputs/cleaned_data.csv into Power BI and create KPI cards, charts, and slicers.")

if __name__ == "__main__":
    main()
