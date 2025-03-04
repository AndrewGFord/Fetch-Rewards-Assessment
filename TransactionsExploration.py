## Exploration of transactions file

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

MAKE_NULL_PLOTS = False # Set to true to make and display plots of null value counts
transaction_filename = 'TRANSACTION_TAKEHOME.csv'

# clean data has string 'zero' replaced with 0.0 and whitespace removed from numeric fields
# does not check for redundant receipt ID and barcode combos
clean_data_filename = 'TRANSACTION_CLEAN.csv' # pre-cleaned data
CLEAN_DATA_EXISTS = os.path.exists(clean_data_filename)
MAKE_RATIO_PLOT = False # only makes plot if CLEAN_DATA_EXISTS is also true
if CLEAN_DATA_EXISTS:
	print('Cleaned transaction data already exists')
else:
	print('Cleaned transaction data not found')

print('Transaction file information')
transactions = pd.read_csv(transaction_filename)
transaction_first_10 = transactions.head(10)
transaction_sorted = transactions.sort_values(by=['RECEIPT_ID'], ascending=True)
print(transaction_sorted)

count_transactions = transactions.shape[0]
print('Total number of transactions: ',count_transactions)

null_values = transactions.isnull().sum()
print('All null fields:\n',null_values)

# Plots of null values
# I chose to manually resize and save plots myself instead of automatically saving
if MAKE_NULL_PLOTS:
	columns = list(transactions.columns)
	nullBarLin = plt.bar(columns,null_values)
	plt.title('Null values in TRANSACTION_TAKEHOME columns (linear scale)')
	plt.ylabel('Total null values')
	plt.show()
	nullBarLog = plt.bar(columns,null_values,log=True)
	plt.title('Null values in TRANSACTION_TAKEHOME columns (logarithmic scale)')
	plt.ylabel('Total null values')
	plt.show()
	nullBarPct = plt.bar(columns,null_values*100/count_transactions)
	plt.title('Null values in TRANSACTION_TAKEHOME columns (percentage)')
	plt.ylabel('Percent of values which are null')
	plt.ylim([0,100])
	plt.show()

# Checks the original data file for the fields which are filtered out in the clean data file
blank_final_sale = (transactions['FINAL_SALE'].str.isspace()).sum()
print('Final sale field blank: ', blank_final_sale)

zero_final_quantity = (transactions['FINAL_QUANTITY'] == 'zero').sum()
print('Final quantity field is string zero: ',zero_final_quantity)

zero_and_blank =((transactions['FINAL_SALE'].str.isspace()) & (transactions['FINAL_QUANTITY'] == 'zero')).sum()
print('Quantity is zero and sale is blank: ',zero_and_blank)

zero_or_blank =((transactions['FINAL_SALE'].str.isspace()) | (transactions['FINAL_QUANTITY'] == 'zero')).sum()
print('Quantity is zero or sale is blank: ',zero_or_blank)

# checks how often each receipt ID appears and prints summary
receipt_id_counts = transactions['RECEIPT_ID'].value_counts()
print(receipt_id_counts.describe())

# gets information about how often each receipt ID/barcode combo exists and prints summary
# only called if the cleaned data file is present
if CLEAN_DATA_EXISTS:
	clean_transactions = pd.read_csv(clean_data_filename)
	clean_transactions = clean_transactions[clean_transactions['FINAL_SALE'].isna() == False]
	clean_transactions = clean_transactions[clean_transactions['FINAL_QUANTITY'] != 0.0]
	receipt_id_counts_clean = clean_transactions['RECEIPT_ID'].value_counts()
	print(receipt_id_counts_clean.describe())
	
	receipt_id_counts_ratio = pd.merge(receipt_id_counts,receipt_id_counts_clean,on='RECEIPT_ID')
	ratios = receipt_id_counts_ratio['count_x'].div(receipt_id_counts_ratio['count_y'])
	print(ratios.describe())
	
	# Ratio between how often each receipt ID/barcode pair appears in the full file and the filtered file
	# Example: If a pair appears 5 times in the full file and 2 in the filtered file, would register 2.5
	# The printed description above suggests every ratio is 2.0
	if MAKE_RATIO_PLOT:
		complete_records = plt.hist(ratios)
		plt.show()