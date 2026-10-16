-- Retail Sales & Profitability Analysis
-- Adapt table and column names to your SQL database.
-- Assumed table name: superstore

-- 1. Overall KPIs
SELECT
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit,
    SUM(Quantity) AS total_quantity,
    COUNT(DISTINCT `Order ID`) AS total_orders
FROM superstore;

-- 2. Sales and profit by category
SELECT
    Category,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit,
    SUM(Quantity) AS total_quantity
FROM superstore
GROUP BY Category
ORDER BY total_sales DESC;

-- 3. Regional performance
SELECT
    Region,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit
FROM superstore
GROUP BY Region
ORDER BY total_profit DESC;

-- 4. Sub-categories with losses
SELECT
    `Sub-Category`,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit
FROM superstore
GROUP BY `Sub-Category`
HAVING SUM(Profit) < 0
ORDER BY total_profit ASC;

-- 5. Discount bands (syntax may vary by SQL database)
SELECT
    CASE
        WHEN Discount < 0.10 THEN '0-9%'
        WHEN Discount < 0.20 THEN '10-19%'
        WHEN Discount < 0.30 THEN '20-29%'
        ELSE '30%+'
    END AS discount_band,
    COUNT(*) AS transaction_rows,
    AVG(Profit) AS average_profit,
    SUM(Sales) AS total_sales
FROM superstore
GROUP BY
    CASE
        WHEN Discount < 0.10 THEN '0-9%'
        WHEN Discount < 0.20 THEN '10-19%'
        WHEN Discount < 0.30 THEN '20-29%'
        ELSE '30%+'
    END
ORDER BY discount_band;

-- 6. Segment performance
SELECT
    Segment,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit
FROM superstore
GROUP BY Segment
ORDER BY total_sales DESC;
