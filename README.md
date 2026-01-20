# Setup 

1) Open terminal in the project folder:
	cd sales-analytics-system

2) Create and activate virtual environment write the following:
	python -m venv env
	env\Scripts\activate

3) Install dependencies
	write "pip install -r requirements.txt"
 	and to confirm
 	write "pip list"

4) To run the program 
	Write "python main.py" in the cmd terminal

# Output
After running successfully, these files are created:
	1) Enriched transactions file:
	   data/enriched_sales_data.txt
	2) Final report:
	   output/sales_report.txt

API Enrichment Notes
API used:
https://dummyjson.com/products?limit=100
If API fails due to internet/server issues, the program will still complete and generate outputs, but enrichment will show:
Fetched 0 products
Enriched 0 transactions
Success rate 0%
This is acceptable and expected behavior when network/API is unavailable.
