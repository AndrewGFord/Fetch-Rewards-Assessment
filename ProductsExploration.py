## Exploration of products file

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

products_filename = 'PRODUCTS_TAKEHOME.csv'
MAKE_NULL_PLOTS = False # set to true to make plots of null values

print('Products file information')
products = pd.read_csv(products_filename)
prods_first_10 = products.head(10)
print(prods_first_10)

count_products = products.shape[0]
print('Total number of products: ',count_products)

# Counts of null values for each field (no cross-referencing)
null_values = products.isnull().sum()
print('All null fields:\n',null_values)

# Counts of null values for all combinations of brand and manufacturer
missing_brand = (products['BRAND'].isnull()).sum()
missing_manufacturer = (products['MANUFACTURER'].isnull()).sum()
missing_both = (products['BRAND'].isnull()*products['MANUFACTURER'].isnull()).sum()
missing_only_brand = (products['BRAND'].isnull() > products['MANUFACTURER'].isnull()).sum()
missing_only_manufacturer = (products['MANUFACTURER'].isnull() > products['BRAND'].isnull()).sum()
print('Missing brand: ',missing_brand)
print('Missing only brand: ',missing_only_brand)
print('Missing manufacturer: ',missing_manufacturer)
print('Missing only manufacturer: ',missing_only_manufacturer)
print('Missing both: ',missing_both)


# Plots of null values
# Chose to manually resize and save plots myself instead of automatically saving
if MAKE_NULL_PLOTS:
	columns = list(products.columns)
	
	nullBarLin = plt.bar(columns,null_values)
	plt.title('Null values in PRODUCTS_TAKEHOME columns (linear scale)')
	plt.ylabel('Total null values')
	plt.show()
	nullBarLog = plt.bar(columns,null_values,log=True)
	plt.title('Null values in PRODUCTS_TAKEHOME columns (logarithmic scale)')
	plt.ylabel('Total null values')
	plt.show()
	nullBarPct = plt.bar(columns,null_values*100/count_products)
	plt.title('Null values in PRODUCTS_TAKEHOME columns (percentage)')
	plt.ylabel('Percent of values which are null')
	plt.ylim([0,100])
	plt.show()

# Tests the hypothesis that the category fields represent a tree of categories and subcategories
# If the tree exists without errors, this should print 0
category_errors12 = (products['CATEGORY_1'].isnull() > products['CATEGORY_2'].isnull()).sum()
category_errors13 = (products['CATEGORY_1'].isnull() > products['CATEGORY_3'].isnull()).sum()
category_errors14 = (products['CATEGORY_1'].isnull() > products['CATEGORY_4'].isnull()).sum()
category_errors23 = (products['CATEGORY_2'].isnull() > products['CATEGORY_3'].isnull()).sum()
category_errors24 = (products['CATEGORY_2'].isnull() > products['CATEGORY_4'].isnull()).sum()
category_errors34 = (products['CATEGORY_3'].isnull() > products['CATEGORY_4'].isnull()).sum()
print('Total errors in category structure: ',category_errors12 + category_errors13 + category_errors14 + category_errors23 + category_errors24 + category_errors34)

# Other information on categories
category_1_values = products['CATEGORY_1'].unique()
print('CATEGORY_1 values: ',category_1_values)
print('Total unique values for CATEGORY_1: ',category_1_values.shape[0])
print('Total unique values for CATEGORY_2: ',products['CATEGORY_2'].unique().shape[0])
print('Total unique values for CATEGORY_3: ',products['CATEGORY_3'].unique().shape[0])
print('Total unique values for CATEGORY_4: ',products['CATEGORY_4'].unique().shape[0])