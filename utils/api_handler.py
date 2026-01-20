# Task 3.1 Fetch Product Details

# (a) Fetch All Products
def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries

    Expected Output Format:
    [
        {
            'id': 1,
            'title': 'iPhone 9',
            'category': 'smartphones',
            'brand': 'Apple',
            'price': 549,
            'rating': 4.69
        },
        ...
    ]

    Requirements:
    - Fetch all available products (use limit=100)
    - Handle connection errors with try-except
    - Return empty list if API fails
    - Print status message (success/failure)
    """

    import requests

    url = "https://dummyjson.com/products?limit=100"
    products = []

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad responses

        data = response.json()
        products = data.get('products', [])

        print(f"Successfully fetched {len(products)} products.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching products: {e}")
        products = []

    return products


# (b) Create Product Mapping
def create_product_mapping(api_products):
    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")
        if product_id is None:
            continue

        product_mapping[product_id] = {
            "title": product.get("title", None),
            "category": product.get("category", None),
            "brand": product.get("brand", None),   # ✅ FIX HERE
            "rating": product.get("rating", None)
        }

    return product_mapping

# Task 3.2 Enrich Sales Data


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information

    Parameters:
    - transactions: list of transaction dictionaries
    - product_mapping: dictionary from create_product_mapping()

    Returns: list of enriched transaction dictionaries

    Expected Output Format (each transaction):
    {
        'TransactionID': 'T001',
        'Date': '2024-12-01',
        'ProductID': 'P101',
        'ProductName': 'Laptop',
        'Quantity': 2,
        'UnitPrice': 45000.0,
        'CustomerID': 'C001',
        'Region': 'North',
        # NEW FIELDS ADDED FROM API:
        'API_Category': 'laptops',
        'API_Brand': 'Apple',
        'API_Rating': 4.7,
        'API_Match': True  # True if enrichment successful, False otherwise
    }

    Enrichment Logic:
    - Extract numeric ID from ProductID (P101 → 101, P5 → 5)
    - If ID exists in product_mapping, add API fields
    - If ID doesn't exist, set API_Match to False and other fields to None
    - Handle all errors gracefully

    File Output:
    - Save enriched data to 'data/enriched_sales_data.txt'
    - Use same pipe-delimited format
    - Include new columns in header
    """

    enriched_transactions = []

    for t in transactions:
        enriched_t = t.copy()  # Start with original transaction data

        # Extract numeric product ID
        product_id_str = t['ProductID']
        try:
            numeric_id = int(''.join(filter(str.isdigit, product_id_str)))
        except ValueError:
            numeric_id = None

        # Enrich with API data if available
        if numeric_id and numeric_id in product_mapping:
            product_info = product_mapping[numeric_id]
            enriched_t['API_Category'] = product_info['category']
            enriched_t['API_Brand'] = product_info['brand']
            enriched_t['API_Rating'] = product_info['rating']
            enriched_t['API_Match'] = True
        else:
            enriched_t['API_Category'] = None
            enriched_t['API_Brand'] = None
            enriched_t['API_Rating'] = None
            enriched_t['API_Match'] = False

        enriched_transactions.append(enriched_t)

    return enriched_transactions

# helper function


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file

    Expected File Format:
    TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
    T001|2024-12-01|P101|Laptop|2|45000.0|C001|North|laptops|Apple|4.7|True
    ...

    Requirements:
    - Create output file with all original + new fields
    - Use pipe delimiter
    - Handle None values appropriately
    """

    with open(filename, 'w', encoding='utf-8') as file:
        # Write header
        header = [
            "TransactionID", "Date", "ProductID", "ProductName",
            "Quantity", "UnitPrice", "CustomerID", "Region",
            "API_Category", "API_Brand", "API_Rating", "API_Match"
        ]
        file.write("|".join(header) + "\n")

        for t in enriched_transactions:
            line = [
                t["TransactionID"],
                t["Date"],
                t["ProductID"],
                t["ProductName"],
                str(t["Quantity"]),
                str(t["UnitPrice"]),
                t["CustomerID"],
                t["Region"],
                t.get("API_Category") if t.get(
                    "API_Category") is not None else "",
                t.get("API_Brand") if t.get("API_Brand") is not None else "",
                str(t.get("API_Rating")) if t.get(
                    "API_Rating") is not None else "",
                str(t.get("API_Match"))
            ]
            file.write("|".join(line) + "\n")
