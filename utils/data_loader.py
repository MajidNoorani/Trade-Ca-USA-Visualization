import pandas as pd
import os
from termcolor import colored

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))  # get directory path of file
PARENT_DIR = os.path.dirname(CURRENT_DIR)  # get parent directory path

df1 = pd.read_csv(os.path.join(PARENT_DIR, 'Processed', 'Canadian domestic exports.csv'))
df1.drop('Unnamed: 0', inplace=True, axis=1)
if not os.path.exists(os.path.join('Processed', 'Canadian domestic exports_unpivot.csv')):
    print(colored(f'Creating Canadian domestic exports_unpivot.csv data. This may take a while.', 'yellow'))
    year_month = df1.columns.drop(['origin','data_type', 'destination', 'industry', 'code_Naics'])
    id_vars = ['origin', 'data_type', 'destination', 'industry', 'code_Naics']
    df = pd.melt(df1, id_vars=id_vars)
    df[['Year', 'Month']] = df["variable"].apply(lambda x: pd.Series(str(x).split(" ")))
    df.rename({'variable':'date'}, inplace=True, axis=1)
    df.fillna(0, inplace=True)
    df.to_csv(os.path.join('Processed', 'Canadian domestic exports_unpivot.csv'))
    print(colored(f'Created the file.', 'green'))

# Data Loading and Pre processing
empty_df = pd.DataFrame({'Total all countries': [], 'Canada': []})
df = pd.read_csv(os.path.join(PARENT_DIR, 'Processed' , 'Canadian domestic exports_unpivot.csv'))

dates = df1.columns.drop(['origin', 'data_type', 'destination', 'industry', 'code_Naics'])
dates = dates.insert(0, dates[-1])
dates = dates.delete(-1)

totals = df1[df1['origin'].str.lower().str.contains('(total|others)', regex=True)]
totals.drop(['data_type'],axis=1, inplace=True)
totals.fillna(0, inplace=True)
df = df[~df['origin'].str.lower().str.contains('(total|others)', regex=True)]
df2 = df1[~df1['origin'].str.lower().str.contains('(total|others)', regex=True)]
# df = df[df['value']>=0]
df['value'] = df['value'].apply(lambda x: 0 if x<0 else x)




months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
years =  ['2021', '2022', '2023']