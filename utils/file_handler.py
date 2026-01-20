# Task 1.1: Read sales data with encoding handling
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)

    Expected Output Format:
    ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]

    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
    """

    encodings = ['utf-8', 'latin-1', 'cp1252']
    lines = []

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()

            raw_lines = []
            for line in lines:
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                # skip header
                if line.lower().startswith('transactionid'):
                    continue

                raw_lines.append(line)

            return raw_lines

        except UnicodeDecodeError:
            continue

        except FileNotFoundError:
            print(f"Error: File not found - {filename}")
            return []

    print("Error: Unable to read file due to encoding issues.")
    return []  # Return empty list if all encodings fail

# Task 1.2: Parse and Clean Data


def parse_transactions(raw_lines):

   # Parses raw lines into clean list of dictionaries

    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        # Must have exactly 8 fields
        if len(parts) != 8:
            continue

        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

        # Clean ProductName (replace commas with space)
        product_name = product_name.replace(',', ' ').strip()

        # Clean numbers: remove commas
        quantity = quantity.replace(',', '').strip()
        unit_price = unit_price.replace(',', '').strip()

        # Convert types
        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            continue

        transactions.append({
            'TransactionID': transaction_id.strip(),
            'Date': date.strip(),
            'ProductID': product_id.strip(),
            'ProductName': product_name,
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'CustomerID': customer_id.strip(),
            'Region': region.strip()
        })

    return transactions

# Task 1.3: Data Validation and Filtering


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates and filters transactions based on criteria

    Parameters:
    - transactions: list of transaction dictionaries
    - region: filter by region (string)
    - min_quantity: filter by minimum quantity (int)

    Returns: filtered list of transactions
    """

    required_keys = [
        'TransactionID', 'Date', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'CustomerID', 'Region'
    ]

    total_input = len(transactions)
    invalid_count = 0
    valid_transactions = []

    # validation

    for t in transactions:
        # required fields exist
        if not all(key in t for key in required_keys):
            invalid_count += 1
            continue

        # valid prefixes
        if not str(t["TransactionID"]).startswith('T'):
            invalid_count += 1
            continue
        if not str(t["ProductID"]).startswith('P'):
            invalid_count += 1
            continue
        if not str(t["CustomerID"]).startswith('C'):
            invalid_count += 1
            continue

        # valid values
        if t["Quantity"] <= 0:
            invalid_count += 1
            continue
        if t["UnitPrice"] <= 0:
            invalid_count += 1
            continue

        # if all checks passed
        valid_transactions.append(t)

    # filtering

    filtered = valid_transactions

    filtered_by_region = 0
    filtered_by_amount = 0

    # filter by region
    if region:
        before = len(filtered)
        filtered = [t for t in filtered if t['Region'].lower() ==
                    region.lower()]
        filtered_by_region += before - len(filtered)

    # filter by amount range
    if min_amount is not None:
        before = len(filtered)
        filtered = [t for t in filtered if t['Quantity']
                    * t['UnitPrice'] >= min_amount]
        filtered_by_amount += before - len(filtered)

    if max_amount is not None:
        before = len(filtered)
        filtered = [t for t in filtered if t['Quantity']
                    * t['UnitPrice'] <= max_amount]
        filtered_by_amount += before - len(filtered)

    filter_summary = {
        'total_input': total_input,
        'invalid_count': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'total_output': len(filtered)
    }

    return filtered, invalid_count, filter_summary
