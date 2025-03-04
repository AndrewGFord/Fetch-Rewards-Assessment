## Exploration of users file

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

users_filename = 'USER_TAKEHOME.csv'
MAKE_NULL_PLOTS = False # set to true to make plots of null values

print('User file information')
users = pd.read_csv(users_filename)
users_first_10 = users.head(10)
print(users_first_10)

print('List of options for state: ',users['STATE'].unique())

print('List of options for language: ',users['LANGUAGE'].unique())

print('List of options for gender: ',users['GENDER'].unique())
count_users = users.shape[0]
print('Total number of users: ',count_users)

null_values = users.isnull().sum()
print('All null fields:\n',null_values)

# Make and display null plots
# Chose to manually resize and save plots myself instead of automatically saving
if MAKE_NULL_PLOTS:
	columns = list(users.columns)
	
	nullBarLin = plt.bar(columns,null_values)
	plt.title('Null values in USER_TAKEHOME columns (linear scale)')
	plt.ylabel('Total null values')
	plt.show()
	nullBarLog = plt.bar(columns,null_values,log=True)
	plt.title('Null values in USER_TAKEHOME columns (logarithmic scale)')
	plt.ylabel('Total null values')
	plt.show()
	nullBarPct = plt.bar(columns,null_values*100/count_users)
	plt.title('Null values in USER_TAKEHOME columns (percentage)')
	plt.ylabel('Percent of values which are null')
	plt.ylim([0,100])
	plt.show()
