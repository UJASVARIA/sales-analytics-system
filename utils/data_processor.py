# Task 2.1: Sales summery calculator

# (a): Calculate Total Revenue
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)

    Expected Output: Single number representing sum of (Quantity * UnitPrice)
    Example: 1545000.50
    """

    total = 0.0
    for t in transactions:
        total += t['Quantity'] * t['UnitPrice']
    return round(total, 2)

# (b): Region-wise Sales Analysis


def region_wise_sales(transactions):

    # Total revenue of all transactions
    total_revenue = calculate_total_revenue(transactions)
    region_stats = {}

    for t in transactions:
        region = t['Region']
        revenue = t['Quantity'] * t['UnitPrice']

        if region not in region_stats:
            region_stats[region] = {
                'total_sales': 0.0,
                'transaction_count': 0,
                'percentage': 0.0
            }

        region_stats[region]['total_sales'] += revenue
        region_stats[region]['transaction_count'] += 1

    # Calculate percentage and round values
    for region, stats in region_stats.items():
        stats['total_sales'] = round(stats['total_sales'], 2)
        stats['percentage'] = round(
            (stats['total_sales'] / total_revenue) * 100, 2) if total_revenue > 0 else 0.0

    # Sort by total_sales in descending order
    sorted_region_stats = dict(
        sorted(region_stats.items(),
               key=lambda item: item[1]['total_sales'],
               reverse=True)
    )

    return sorted_region_stats

# (c): Top Selling Products


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples
    [
        ('Laptop', 45, 2250000.0),
        ('Mouse', 38, 19000.0),
        ...
    ]
    """

    product_stats = {}

    # Aggregate quantity and revenue by product
    for t in transactions:
        product = t['ProductName']
        quantity = t['Quantity']
        revenue = t['Quantity'] * t['UnitPrice']

        if product not in product_stats:
            product_stats[product] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }

        product_stats[product]['total_quantity'] += quantity
        product_stats[product]['total_revenue'] += revenue

    # Convert to list of tuples
    result = []
    for product_name, stats in product_stats.items():
        result.append((
            product_name,
            stats['total_quantity'],
            round(stats['total_revenue'], 2)
        ))

    # Sort by quantity (descending)
    result.sort(key=lambda x: x[1], reverse=True)

    # Return top n
    return result[:n]

# (d): Customer Purchase Analysis


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns.

    Returns: dictionary of customer statistics
    Sorted by total_spent in descending order
    """

    customer_stats = {}

    # Step 1: Aggregate spending + purchase count + unique products
    for t in transactions:
        customer = t["CustomerID"]
        product = t["ProductName"]
        amount = t["Quantity"] * t["UnitPrice"]

        if customer not in customer_stats:
            customer_stats[customer] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()   # set ensures uniqueness
            }

        customer_stats[customer]["total_spent"] += amount
        customer_stats[customer]["purchase_count"] += 1
        customer_stats[customer]["products_bought"].add(product)

    # Step 2: Calculate average order value and clean output types
    for customer, stats in customer_stats.items():
        spent = stats["total_spent"]
        count = stats["purchase_count"]

        if count > 0:
            avg = spent / count
        else:
            avg = 0.0

        stats["total_spent"] = round(spent, 2)
        stats["avg_order_value"] = round(avg, 2)

        # convert set -> sorted list
        stats["products_bought"] = sorted(list(stats["products_bought"]))

    # Step 3: Sort by total_spent descending
    sorted_customers = dict(
        sorted(customer_stats.items(),
               key=lambda item: item[1]["total_spent"],
               reverse=True)
    )

    return sorted_customers

# Task 2.2: Date-based Analysis

# (a): Daily Sales Trend


def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns: dictionary sorted by date

    Expected Output Format:
    {
        '2024-12-01': {
            'revenue': 125000.0,
            'transaction_count': 8,
            'unique_customers': 6
        },
        '2024-12-02': {...},
        ...
    }

    Requirements:
    - Group by date
    - Calculate daily revenue
    - Count daily transactions
    - Count unique customers per day
    - Sort chronologically
    """

    date_stats = {}

    for t in transactions:
        date = t['Date']
        revenue = t['Quantity'] * t['UnitPrice']
        customer = t['CustomerID']

        if date not in date_stats:
            date_stats[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()
            }

        date_stats[date]['revenue'] += revenue
        date_stats[date]['transaction_count'] += 1
        date_stats[date]['unique_customers'].add(customer)

    # Finalize unique customer counts and round revenue
    for date, stats in date_stats.items():
        stats['revenue'] = round(stats['revenue'], 2)
        stats['unique_customers'] = len(stats['unique_customers'])

    # Sort by date
    sorted_date_stats = dict(
        sorted(date_stats.items(),
               key=lambda item: item[0])
    )

    return sorted_date_stats

# (b): Find Peak Sales Day


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns: tuple (date, revenue, transaction_count)

    Expected Output Format:
    ('2024-12-15', 185000.0, 12)
    """

    daily_stats = daily_sales_trend(transactions)

    peak_date = None
    peak_revenue = 0.0
    peak_transactions = 0

    for date, stats in daily_stats.items():
        if stats['revenue'] > peak_revenue:
            peak_revenue = stats['revenue']
            peak_date = date
            peak_transactions = stats['transaction_count']

    return (peak_date, peak_revenue, peak_transactions)

# Task 2.3: Product Performance

# Low Performing Products


def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns: list of tuples

    Expected Output Format:
    [
        ('Webcam', 4, 12000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Headphones', 7, 10500.0),
        ...
    ]

    Requirements:
    - Find products with total quantity < threshold
    - Include total quantity and revenue
    - Sort by TotalQuantity ascending
    """
    product_stats = {}

    # Aggregate quantity and revenue by product
    for t in transactions:
        product = t['ProductName']
        quantity = t['Quantity']
        revenue = t['Quantity'] * t['UnitPrice']

        if product not in product_stats:
            product_stats[product] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }

        product_stats[product]['total_quantity'] += quantity
        product_stats[product]['total_revenue'] += revenue

    # Filter low performing products
    low_performers = []
    for product_name, stats in product_stats.items():
        if stats['total_quantity'] < threshold:
            low_performers.append((
                product_name,
                stats['total_quantity'],
                round(stats['total_revenue'], 2)
            ))

    # Sort by total_quantity ascending
    low_performers.sort(key=lambda x: x[1])

    return low_performers
