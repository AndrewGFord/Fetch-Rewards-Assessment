## Clean transactions file for SQL import

import pandas as pd

# Problems for SQL load:
# Some values of FINAL_QUANTITY are saved as the string 'zero' instead of the number 0
# Some values of FINAL_SALE are whitespace characters, not just blank
# Possible third problem: at least 2 rows for each receipt_id (max 12, min 2, all even numbers)

INPUT_FILENAME = 'TRANSACTION_TAKEHOME.csv'
transactions = pd.read_csv(INPUT_FILENAME)
num_rows = transactions.shape[0]

def transform_row(r):
	if r['FINAL_QUANTITY'] == 'zero':
		r['FINAL_QUANTITY'] = 0.0
	if r['FINAL_SALE'].isspace():
		r['FINAL_SALE'] = ''
	return r

transactions_clean = transactions.apply(transform_row, axis=1)
# converts floats to string representation of integer while making NaN values blank
transactions_clean['BARCODE'] = transactions_clean['BARCODE'].fillna('')
transactions_clean['BARCODE'] = transactions_clean['BARCODE'].astype(str)
transactions_clean['BARCODE'] = transactions_clean['BARCODE'].str.split('.')
transactions_clean['BARCODE'] = transactions_clean['BARCODE'].str[0]

print(transactions_clean.sort_values(by=['RECEIPT_ID'], ascending=True))

OUTPUT_FILENAME = 'TRANSACTION_CLEAN.csv'
transactions_clean.to_csv(OUTPUT_FILENAME, index=False)