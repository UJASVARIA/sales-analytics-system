
""""""
# Data File Handler & Pre-processing (File I/O and Error Handling)

from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter

raw_lines = read_sales_data('data/sales_data.txt')
print("Task 1.1 -> Raw Lines:", len(raw_lines))
print("First raw line:", raw_lines[0] if raw_lines else "No data")

transactions = parse_transactions(raw_lines)
print("\nTask 1.2 -> Parsed Transactions:", len(transactions))
print("First parsed transaction:",
      transactions[0] if transactions else "No data")

valid, invalid_count, summary = validate_and_filter(transactions)
print("\nTask 1.3 -> Valid Transactions:", len(valid))
print("Invalid removed:", invalid_count)
print("Summary:", summary)


# Data Processing (Lists, Dictionaries & Functions)

# Task 2.1(a): Total Revenue
total_revenue = calculate_total_revenue(valid)
print("\nTask 2.1(a) -> Total Revenue:", total_revenue)

# Task 2.1(b): Region-wise Sales
region_stats = region_wise_sales(valid)
print("\nTask 2.1(b) -> Region-wise Sales (sorted by total_sales desc):")
for region, stats in region_stats.items():
    print(region, "->", stats)

# Task 2.1(c): Top Selling Products
top_products = top_selling_products(valid, n=5)
print("\nTask 2.1(c) -> Top 5 Selling Products (ProductName, TotalQty, TotalRevenue):")
for item in top_products:
    print(item)

# Task 2.1(d): Customer Analysis
customers = customer_analysis(valid)
print("\nTask 2.1(d) -> Customer Analysis (Top 5 customers):")
count = 0
for cid, stats in customers.items():
    print(cid, "->", stats)
    count += 1
    if count == 5:
        break

# Task 2.2(a): Daily Sales Trend
daily = daily_sales_trend(valid)
print("\nTask 2.2(a) -> Daily Sales Trend (first 5 days):")
count = 0
for date, stats in daily.items():
    print(date, "->", stats)
    count += 1
    if count == 5:
        break

# Task 2.2(b): Peak Sales Day
peak_day = find_peak_sales_day(valid)
print("\nTask 2.2(b) -> Peak Sales Day (date, revenue, transaction_count):")
print(peak_day)

# Task 2.3: Low Performing Products
low_products = low_performing_products(valid, threshold=10)
print("\nTask 2.3 -> Low Performing Products (qty < 10):")
for item in low_products:
    print(item)

# API Integration

# Task 3.1(a) Fetch Products
api_products = fetch_all_products()
print("API products fetched:", len(api_products))

# Task 3.1(b) Product Mapping
product_map = create_product_mapping(api_products)
print("Product mapping created:", len(product_map))

# Show first 2 API products
if api_products:
    print("\nSample API Product 1:", api_products[0])
    print("Sample API Product 2:", api_products[1])

# Task 3.2 Enrich Sales Data
enriched = enrich_sales_data(valid, product_map)
print("\nEnriched transaction sample:")
print(enriched[0])

# Save enriched file
save_enriched_data(enriched, filename="data/enriched_sales_data.txt")
print("\n Saved file: data/enriched_sales_data.txt")

if not api_products:
    print("API failed or no products returned — enrichment will continue with API_Match = False")
