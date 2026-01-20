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
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data, save_enriched_data
from utils.report_generator import generate_sales_report


def safe_float(text):
    try:
        return float(text)
    except Exception:
        return None


def get_user_filters(transactions):
    regions = sorted(
        list({t["Region"] for t in transactions if "Region" in t and t["Region"]}))
    amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]
    min_amt = min(amounts) if amounts else 0
    max_amt = max(amounts) if amounts else 0

    print("\nFilter Options Available:")
    print("Regions:", ", ".join(regions) if regions else "N/A")
    print(f"Transaction amount range: {min_amt:.2f} to {max_amt:.2f}")

    use_filter = input("\nDo you want to filter data? (y/n): ").strip().lower()
    if use_filter != "y":
        return None, None, None

    region = input("Enter region (or press Enter to skip): ").strip()
    if region == "":
        region = None

    min_amount = input("Enter min amount (or press Enter to skip): ").strip()
    min_amount = safe_float(min_amount) if min_amount else None

    max_amount = input("Enter max amount (or press Enter to skip): ").strip()
    max_amount = safe_float(max_amount) if max_amount else None

    return region, min_amount, max_amount


def main():
    try:
        print("==============================================")
        print("SALES ANALYTICS SYSTEM")
        print("==============================================\n")

        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        if not raw_lines:
            print("No sales data loaded. Exiting.")
            return
        print(f"Successfully read {len(raw_lines)} transactions\n")

        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"Parsed {len(transactions)} records\n")

        print("[3/10] Displaying filter options...")
        region, min_amount, max_amount = get_user_filters(transactions)

        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(
            transactions,
            region=region,
            min_amount=min_amount,
            max_amount=max_amount
        )
        print(
            f"Valid: {len(valid_transactions)} | Invalid removed: {invalid_count}")
        print("Summary:", summary, "\n")

        print("[5/10] Analyzing sales data...")
        total_revenue = calculate_total_revenue(valid_transactions)
        reg_stats = region_wise_sales(valid_transactions)
        top_products = top_selling_products(valid_transactions, n=5)
        top_customers = customer_analysis(valid_transactions)
        trend = daily_sales_trend(valid_transactions)
        peak_day = find_peak_sales_day(valid_transactions)
        low_perf = low_performing_products(valid_transactions, threshold=10)
        print("Analysis complete\n")

        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"Fetched {len(api_products)} products\n")

        product_map = create_product_mapping(api_products)

        print("[7/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(
            valid_transactions, product_map)
        enriched_count = sum(
            1 for t in enriched_transactions if t.get("API_Match") is True)
        success_rate = (enriched_count / len(enriched_transactions)
                        * 100) if enriched_transactions else 0
        print(
            f"Enriched {enriched_count}/{len(enriched_transactions)} transactions ({success_rate:.2f}%)\n")

        print("[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions,
                           filename="data/enriched_sales_data.txt")
        print("Saved to: data/enriched_sales_data.txt\n")

        print("[9/10] Generating report...")
        generate_sales_report(
            valid_transactions,
            enriched_transactions,
            output_file="output/sales_report.txt"
        )
        print("Report saved to: output/sales_report.txt\n")

        print("[10/10] Process Complete!")
        print("==============================================")

    except Exception as e:
        print("\nSomething went wrong but the program didn't crash.")
        print("Error:", e)


if __name__ == "__main__":
    main()
