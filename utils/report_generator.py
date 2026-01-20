# utils/report_generator.py

import os
from datetime import datetime


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted text report

    Report Must Include (in this order):

    1. HEADER
    2. OVERALL SUMMARY
    3. REGION-WISE PERFORMANCE
    4. TOP 5 PRODUCTS
    5. TOP 5 CUSTOMERS
    6. DAILY SALES TREND
    7. PRODUCT PERFORMANCE ANALYSIS
    8. API ENRICHMENT SUMMARY
    """

    def safe_float(x):
        try:
            return float(x)
        except Exception:
            return 0.0

    def money(x):
        # Format like: 3,540,205.00
        return f"{safe_float(x):,.2f}"

    def amount(t):
        return safe_float(t.get("Quantity", 0)) * safe_float(t.get("UnitPrice", 0))

    # Make sure output folder exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    records = len(transactions)
    total_revenue = sum(amount(t) for t in transactions)
    total_transactions = records
    avg_order_value = (
        total_revenue / total_transactions) if total_transactions else 0.0

    # Date range
    dates = [t.get("Date") for t in transactions if t.get("Date")]
    date_min = min(dates) if dates else "N/A"
    date_max = max(dates) if dates else "N/A"

    # Region-wise performance
    region_stats = {}
    for t in transactions:
        r = t.get("Region", "").strip()
        rev = amount(t)
        if r not in region_stats:
            region_stats[r] = {"total_sales": 0.0, "transaction_count": 0}
        region_stats[r]["total_sales"] += rev
        region_stats[r]["transaction_count"] += 1

    # Add percentage + sort
    region_list = []
    for r, stats in region_stats.items():
        pct = (stats["total_sales"] / total_revenue *
               100) if total_revenue else 0.0
        region_list.append(
            (r, stats["total_sales"], pct, stats["transaction_count"]))
    region_list.sort(key=lambda x: x[1], reverse=True)

    # Top 5 products (by quantity sold)
    product_stats = {}
    for t in transactions:
        p = t.get("ProductName", "").strip()
        q = int(safe_float(t.get("Quantity", 0)))
        rev = amount(t)
        if p not in product_stats:
            product_stats[p] = {"qty": 0, "rev": 0.0}
        product_stats[p]["qty"] += q
        product_stats[p]["rev"] += rev

    top_products = sorted(
        [(p, v["qty"], v["rev"]) for p, v in product_stats.items()],
        key=lambda x: x[1],
        reverse=True
    )[:5]

    # Top 5 customers (by total spent)
    customer_stats = {}
    for t in transactions:
        c = t.get("CustomerID", "").strip()
        rev = amount(t)
        if c not in customer_stats:
            customer_stats[c] = {"spent": 0.0, "orders": 0}
        customer_stats[c]["spent"] += rev
        customer_stats[c]["orders"] += 1

    top_customers = sorted(
        [(c, v["spent"], v["orders"]) for c, v in customer_stats.items()],
        key=lambda x: x[1],
        reverse=True
    )[:5]

    # Daily sales trend
    daily = {}
    for t in transactions:
        d = t.get("Date", "").strip()
        if not d:
            continue
        if d not in daily:
            daily[d] = {"revenue": 0.0, "txns": 0, "customers": set()}
        daily[d]["revenue"] += amount(t)
        daily[d]["txns"] += 1
        daily[d]["customers"].add(t.get("CustomerID", ""))

    daily_list = []
    for d, info in daily.items():
        daily_list.append(
            (d, info["revenue"], info["txns"], len(info["customers"])))
    daily_list.sort(key=lambda x: x[0])

    # Best selling day
    peak_day = ("N/A", 0.0, 0)
    if daily_list:
        peak_day = max(daily_list, key=lambda x: x[1])
        peak_day = (peak_day[0], peak_day[1], peak_day[2])

    # Low performing products (qty < 10)
    low_perf = sorted(
        [(p, v["qty"], v["rev"])
         for p, v in product_stats.items() if v["qty"] < 10],
        key=lambda x: x[1]
    )

    # Avg transaction value per region
    avg_region = []
    for r, sales, pct, txns in region_list:
        avg_val = (sales / txns) if txns else 0.0
        avg_region.append((r, avg_val))

    # API enrichment summary
    enriched_count = 0
    failed_products = set()

    for t in enriched_transactions:
        if t.get("API_Match") is True:
            enriched_count += 1
        else:
            pname = t.get("ProductName")
            if pname:
                failed_products.add(pname.strip())

    success_rate = (enriched_count / len(enriched_transactions)
                    * 100) if enriched_transactions else 0.0

    # Write report
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(
            "== == == == == == == == == == == == == == == == == == == == == == == == ==\n")
        f.write("              SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {records}\n")
        f.write(
            "== == == == == == == == == == == == == == == == == == == == == == == == ==\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("--------------------------------------------------\n")
        f.write(f"Total Revenue:        {money(total_revenue)}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  {money(avg_order_value)}\n")
        f.write(f"Date Range:           {date_min} to {date_max}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("--------------------------------------------------\n")
        f.write(f"{'Region':<10}{'Sales':<15}{'% of Total':<12}{'Transactions'}\n")
        for r, sales, pct, txns in region_list:
            f.write(f"{r:<10}{money(sales):<15}{pct:>8.2f}{'':<4}{txns}\n")
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("--------------------------------------------------\n")
        f.write(f"{'Rank':<6}{'Product':<20}{'Qty Sold':<10}{'Revenue'}\n")
        for i, (p, qty, rev) in enumerate(top_products, start=1):
            f.write(f"{i:<6}{p:<20}{qty:<10}{money(rev)}\n")
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("--------------------------------------------------\n")
        f.write(f"{'Rank':<6}{'Customer':<12}{'Total Spent':<15}{'Orders'}\n")
        for i, (c, spent, orders) in enumerate(top_customers, start=1):
            f.write(
                f"{i:<6}{c:<12}{money(spent(spent) if False else money(spent)):<15}{orders}\n")
        f.write("\n")

        f.write("DAILY SALES TREND\n")
        f.write("--------------------------------------------------\n")
        f.write(f"{'Date':<12}{'Revenue':<15}{'Txns':<8}{'UniqueCust'}\n")
        for d, rev, txns, uniq in daily_list:
            f.write(f"{d:<12}{money(rev):<15}{txns:<8}{uniq}\n")
        f.write("\n")

        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("--------------------------------------------------\n")
        f.write(
            f"Best selling day: {peak_day[0]} | Revenue: {money(peak_day[1])} | Transactions: {peak_day[2]}\n\n")

        f.write("Low performing products(qty < 10):\n")
        if low_perf:
            for p, qty, rev in low_perf:
                f.write(f" - {p} | Qty: {qty} | Revenue: {money(rev)}\n")
        else:
            f.write(" - None\n")
        f.write("\n")

        f.write("Average transaction value per region:\n")
        for r, avg_val in avg_region:
            f.write(f" - {r}: {money(avg_val)}\n")
        f.write("\n")

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("--------------------------------------------------\n")
        f.write(
            f"Total products enriched: {enriched_count}/{len(enriched_transactions)}\n")
        f.write(f"Success rate: {success_rate:.2f}%\n\n")

        f.write("Products that couldn't be enriched:\n")
        if failed_products:
            for p in sorted(failed_products):
                f.write(f" - {p}\n")
        else:
            f.write(" - None\n")
