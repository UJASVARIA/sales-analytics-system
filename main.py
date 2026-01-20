# main.py
# Part 5: Main Application - Task 5.1

from datetime import datetime

from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)


def write_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):

    def money(x):
        return f"{x:,.2f}"

    total_transactions = len(transactions)
    total_revenue = calculate_total_revenue(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    # date range
    dates = [t["Date"] for t in transactions]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    # region performance
    region_stats = region_wise_sales(transactions)

    # top products
    top_products = top_selling_products(transactions, n=5)

    # top customers
    customers = customer_analysis(transactions)
    top_customers = list(customers.items())[:5]

    # daily trend
    trend = daily_sales_trend(transactions)

    # peak sales
    peak_day = find_peak_sales_day(transactions)

    # low performing
    low_perf = low_performing_products(transactions, threshold=10)

    # API enrichment summary
    enriched_count = sum(
        1 for t in enriched_transactions if t.get("API_Match") is True)
    total_enriched = len(enriched_transactions)
    success_rate = (enriched_count / total_enriched *
                    100) if total_enriched else 0

    failed_products = sorted(set(
        t["ProductName"] for t in enriched_transactions if not t.get("API_Match")
    ))

    with open(output_file, "w", encoding="utf-8") as f:
        # 1) HEADER
        f.write("=" * 50 + "\n")
        f.write("              SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {len(transactions)}\n")
        f.write("=" * 50 + "\n\n")

        # 2) OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Revenue:        {money(total_revenue)}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  {money(avg_order_value)}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        # 3) REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 50 + "\n")
        f.write(
            f"{'Region':<10}{'Sales':<15}{'% of Total':<12}{'Transactions':<12}\n")
        for region, stats in region_stats.items():
            f.write(
                f"{region:<10}{money(stats['total_sales']):<15}"
                f"{stats['percentage']:<12}{stats['transaction_count']:<12}\n"
            )
        f.write("\n")

        # 4) TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Rank':<6}{'Product':<20}{'Qty Sold':<10}{'Revenue':<15}\n")
        for i, (pname, qty, rev) in enumerate(top_products, start=1):
            f.write(f"{i:<6}{pname:<20}{qty:<10}{money(rev):<15}\n")
        f.write("\n")

        # 5) TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Rank':<6}{'Customer':<12}{'Total Spent':<15}{'Orders':<10}\n")
        for i, (cid, info) in enumerate(top_customers, start=1):
            f.write(
                f"{i:<6}{cid:<12}{money(info['total_spent']):<15}{info['purchase_count']:<10}\n"
            )
        f.write("\n")

        # 6) DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Date':<12}{'Revenue':<15}{'Txns':<8}{'UniqueCust':<10}\n")
        for date, info in trend.items():
            f.write(
                f"{date:<12}{money(info['revenue']):<15}{info['transaction_count']:<8}{info['unique_customers']:<10}\n"
            )
        f.write("\n")

        # 7) PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 50 + "\n")
        f.write(
            f"Best selling day: {peak_day[0]} | Revenue: {money(peak_day[1])} | Transactions: {peak_day[2]}\n\n")

        f.write("Low performing products (qty < 10):\n")
        if low_perf:
            for item in low_perf:
                f.write(
                    f" - {item[0]} | Qty: {item[1]} | Revenue: {money(item[2])}\n")
        else:
            f.write(" - None\n")
        f.write("\n")

        # Avg transaction value per region
        f.write("Average transaction value per region:\n")
        for region, stats in region_stats.items():
            avg_val = stats["total_sales"] / \
                stats["transaction_count"] if stats["transaction_count"] else 0
            f.write(f" - {region}: {money(avg_val)}\n")
        f.write("\n")

        # 8) API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(
            f"Total products enriched: {enriched_count}/{total_enriched}\n")
        f.write(f"Success rate: {success_rate:.2f}%\n\n")

        f.write("Products that couldn't be enriched:\n")
        if failed_products:
            for p in failed_products:
                f.write(f" - {p}\n")
        else:
            f.write(" - None\n")


def main():
    print("=" * 40)
    print("      SALES ANALYTICS SYSTEM")
    print("=" * 40)

    try:
        # [1/10] Reading sales data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # [2/10] Parsing and cleaning data
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        # [3/10] Filter options
        print("\n[3/10] Filter Options Available:")
        regions = sorted(set(t["Region"] for t in transactions))
        print("Regions:", ", ".join(regions))

        amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]
        min_amount_range = min(amounts) if amounts else 0
        max_amount_range = max(amounts) if amounts else 0
        print(
            f"Amount Range: ₹{min_amount_range:.2f} - ₹{max_amount_range:.2f}")

        choice = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region_filter = None
        min_amount = None
        max_amount = None

        if choice == "y":
            region_filter = input(
                "Enter region (or press Enter to skip): ").strip()
            if region_filter == "":
                region_filter = None

            min_amount_in = input(
                "Enter min amount (or press Enter to skip): ").strip()
            if min_amount_in != "":
                min_amount = float(min_amount_in)

            max_amount_in = input(
                "Enter max amount (or press Enter to skip): ").strip()
            if max_amount_in != "":
                max_amount = float(max_amount_in)

        # [4/10] Validate
        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(
            transactions,
            region=region_filter,
            min_amount=min_amount,
            max_amount=max_amount
        )
        print(
            f" Valid: {len(valid_transactions)} | Invalid removed: {invalid_count}")
        print("Summary:", summary)

        # [5/10] Analyze (Part 2 functions already tested)
        print("\n[5/10] Analyzing sales data...")
        _ = calculate_total_revenue(valid_transactions)
        _ = region_wise_sales(valid_transactions)
        _ = top_selling_products(valid_transactions, n=5)
        _ = customer_analysis(valid_transactions)
        _ = daily_sales_trend(valid_transactions)
        _ = find_peak_sales_day(valid_transactions)
        _ = low_performing_products(valid_transactions, threshold=10)
        print("✓ Analysis complete")

        # [6/10] API fetch
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # [7/10] Enrich
        print("\n[7/10] Enriching sales data...")
        product_map = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(
            valid_transactions, product_map)

        enriched_count = sum(
            1 for t in enriched_transactions if t.get("API_Match") is True)
        success_rate = (enriched_count / len(enriched_transactions)
                        * 100) if enriched_transactions else 0
        print(
            f"✓ Enriched {enriched_count}/{len(enriched_transactions)} transactions ({success_rate:.2f}%)")

        # [8/10] Save enriched data
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions,
                           filename="data/enriched_sales_data.txt")
        print("✓ Saved to: data/enriched_sales_data.txt")

        # [9/10] Generate report DIRECTLY IN output/
        print("\n[9/10] Generating report...")
        write_sales_report(valid_transactions, enriched_transactions,
                           output_file="output/sales_report.txt")
        print("✓ Report saved to: output/sales_report.txt")

        # [10/10] Complete
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n Something went wrong but the program didn’t crash.")
        print("Error:", e)


if __name__ == "__main__":
    main()
