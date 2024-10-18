# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 13:22:47 2024

@author: mital
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

raw_data = pd.read_csv(r"C:\Users\mital\Documents\Project-4 (Analysis of Bonus Allocation)\Bonus Allocation Data - Master Data.csv.csv")
raw_data.describe
raw_data.info
# missing values #
raw_data.isna().sum()


from scipy import stats

# Age statistics
age_stats = {
    'Average Age': raw_data['age'].mean(),
    'Median Age': raw_data['age'].median(),
    'Mode Age': raw_data['age'].mode()[0],
    'Minimum Age': raw_data['age'].min(),
    'Maximum Age': raw_data['age'].max(),
    'Range of Age': raw_data['age'].max() - raw_data['age'].min(),
    'Age Variance': raw_data['age'].var(),
    'Age Standard Deviation': raw_data['age'].std(),
    'Age Skewness': raw_data['age'].skew(),
    'Age Kurtosis': raw_data['age'].kurt()
}
age_stats


# Income Level statistics
income_stats = {
    'Average Income': raw_data['income_level'].mean(),
    'Median Income': raw_data['income_level'].median(),
    'Mode Income': raw_data['income_level'].mode()[0],
    'Minimum Income': raw_data['income_level'].min(),
    'Maximum Income': raw_data['income_level'].max(),
    'Range of Income': raw_data['income_level'].max() - raw_data['income_level'].min(),
    'Income Variance': raw_data['income_level'].var(),
    'Income Standard Deviation': raw_data['income_level'].std(),
    'Income Skewness': raw_data['income_level'].skew(),
    'Income Kurtosis': raw_data['income_level'].kurt()
}
income_stats



# Winning Percentage statistics
winning_percentage_stats = {
    'Average Winning Percentage': raw_data['Winning_percentage'].mean(),
    'Median Winning Percentage': raw_data['Winning_percentage'].median(),
    'Mode Winning Percentage': raw_data['Winning_percentage'].mode()[0],
    'Minimum Winning Percentage': raw_data['Winning_percentage'].min(),
    'Maximum Winning Percentage': raw_data['Winning_percentage'].max(),
    'Range of Winning Percentage': raw_data['Winning_percentage'].max() - raw_data['Winning_percentage'].min(),
    'Winning Percentage Variance': raw_data['Winning_percentage'].var(),
    'Winning Percentage Standard Deviation': raw_data['Winning_percentage'].std(),
    'Winning Percentage Skewness': raw_data['Winning_percentage'].skew(),
    'Winning Percentage Kurtosis': raw_data['Winning_percentage'].kurt()
}
winning_percentage_stats



# Total Number of Bets statistics
total_bets_stats = {
    'Average Total Number of Bets': raw_data['Total_Number_of_Bets'].mean(),
    'Median Total Number of Bets': raw_data['Total_Number_of_Bets'].median(),
    'Mode Total Number of Bets': raw_data['Total_Number_of_Bets'].mode()[0],
    'Minimum Total Number of Bets': raw_data['Total_Number_of_Bets'].min(),
    'Maximum Total Number of Bets': raw_data['Total_Number_of_Bets'].max(),
    'Range of Total Number of Bets': raw_data['Total_Number_of_Bets'].max() - raw_data['Total_Number_of_Bets'].min(),
    'Total Number of Bets Variance': raw_data['Total_Number_of_Bets'].var(),
    'Total Number of Bets Standard Deviation': raw_data['Total_Number_of_Bets'].std(),
    'Total Number of Bets Skewness': raw_data['Total_Number_of_Bets'].skew(),
    'Total Number of Bets Kurtosis': raw_data['Total_Number_of_Bets'].kurt()
}
total_bets_stats


# Amount of Bonuses Received statistics
bonus_amount_stats = {
    'Average Amount of Bonuses Received': raw_data['Amount_of_Bonuses_Received'].mean(),
    'Median Amount of Bonuses Received': raw_data['Amount_of_Bonuses_Received'].median(),
    'Mode Amount of Bonuses Received': raw_data['Amount_of_Bonuses_Received'].mode()[0],
    'Minimum Amount of Bonuses Received': raw_data['Amount_of_Bonuses_Received'].min(),
    'Maximum Amount of Bonuses Received': raw_data['Amount_of_Bonuses_Received'].max(),
    'Range of Amount of Bonuses Received': raw_data['Amount_of_Bonuses_Received'].max() - raw_data['Amount_of_Bonuses_Received'].min(),
    'Amount of Bonuses Received Variance': raw_data['Amount_of_Bonuses_Received'].var(),
    'Amount of Bonuses Received Standard Deviation': raw_data['Amount_of_Bonuses_Received'].std(),
    'Amount of Bonuses Received Skewness': raw_data['Amount_of_Bonuses_Received'].skew(),
    'Amount of Bonuses Received Kurtosis': raw_data['Amount_of_Bonuses_Received'].kurt()
}
bonus_amount_stats





import matplotlib.pyplot as plt
import seaborn as sns

# Univariate Analysis - Distribution of Age
plt.figure(figsize=(10, 6))
sns.histplot(raw_data['age'], kde=True, bins=30)
plt.title('Distribution of Customer Age')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()


# Bivariate Analysis - Age vs. Winning Percentage
plt.figure(figsize=(10, 6))
sns.scatterplot(x='age', y='Winning_percentage', data=raw_data)
plt.title('Age vs. Winning Percentage')
plt.xlabel('Age')
plt.ylabel('Winning Percentage')
plt.show()


# Multivariate Analysis - Pair Plot
plt.figure(figsize=(15, 10))
sns.pairplot(raw_data[['age', 'Winning_percentage', 'Total_Number_of_Bets', 'Total_Amount_Wagered']])
plt.suptitle('Pair Plot of Selected Features', y=1.02)
plt.show()


                 ### PREPROCESSING OF DATA ###
                                                
sns.boxplot(raw_data.age)                                                               
sns.boxplot(raw_data.income_level)                        
sns.boxplot(raw_data.Winning_percentage)            
sns.boxplot(raw_data.Days_Since_Last_Bet)
sns.boxplot(raw_data.Active_Days)                         
sns.boxplot(raw_data.Total_Number_of_Bets)    #            
sns.boxplot(raw_data.Total_Amount_Wagered)    #            
sns.boxplot(raw_data.Average_Bet_Amount)      #              
sns.boxplot(raw_data.Number_of_Bonuses_Received)       
sns.boxplot(raw_data.Amount_of_Bonuses_Received)         
sns.boxplot(raw_data.Revenue_from_Bonuses)              
sns.boxplot(raw_data.Increase_in_Bets_After_Bonus)         
sns.boxplot(raw_data.Increase_in_wagering_after_Bonus)    
                                 


# Function to identify outliers using the IQR method
def count_outliers(column):
    Q1 = column.quantile(0.25)
    Q3 = column.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = ((column < lower_bound) | (column > upper_bound)).sum()
    return outliers

# Apply the outlier counting function to each numerical column
numerical_columns = raw_data.select_dtypes(include=[np.number]).columns
outliers_count = raw_data[numerical_columns].apply(count_outliers)

# Print the number of outliers in each numerical attribute
print("Number of outliers in each numerical attribute:")
print(outliers_count)



IQR = raw_data['Total_Number_of_Bets'].quantile(0.75) - raw_data['Total_Number_of_Bets'].quantile(0.25)
lower_limit = raw_data['Total_Number_of_Bets'].quantile(0.25) - 1.5*IQR
upper_limit = raw_data['Total_Number_of_Bets'].quantile(0.75) + 1.5*IQR
# Replacing the outlier values with the upper and lower limits #
raw_data['Total_Number_of_Bets'] = pd.DataFrame(np.where(raw_data['Total_Number_of_Bets'] > upper_limit, upper_limit, np.where(raw_data['Total_Number_of_Bets'] < lower_limit, lower_limit, raw_data['Total_Number_of_Bets'])))
sns.boxplot(raw_data.Total_Number_of_Bets)


IQR = raw_data['Total_Amount_Wagered'].quantile(0.75) - raw_data['Total_Amount_Wagered'].quantile(0.25)
lower_limit = raw_data['Total_Amount_Wagered'].quantile(0.25) - 1.5*IQR
upper_limit = raw_data['Total_Amount_Wagered'].quantile(0.75) + 1.5*IQR
# Replacing the outlier values with the upper and lower limits #
raw_data['Total_Amount_Wagered'] = pd.DataFrame(np.where(raw_data['Total_Amount_Wagered'] > upper_limit, upper_limit, np.where(raw_data['Total_Amount_Wagered'] < lower_limit, lower_limit, raw_data['Total_Amount_Wagered'])))
sns.boxplot(raw_data.Total_Amount_Wagered)


IQR = raw_data['Average_Bet_Amount'].quantile(0.75) - raw_data['Average_Bet_Amount'].quantile(0.25)
lower_limit = raw_data['Average_Bet_Amount'].quantile(0.25) - 1.5*IQR
upper_limit = raw_data['Average_Bet_Amount'].quantile(0.75) + 1.5*IQR
# Replacing the outlier values with the upper and lower limits #
raw_data['Average_Bet_Amount'] = pd.DataFrame(np.where(raw_data['Average_Bet_Amount'] > upper_limit, upper_limit, np.where(raw_data['Average_Bet_Amount'] < lower_limit, lower_limit, raw_data['Average_Bet_Amount'])))
sns.boxplot(raw_data.Average_Bet_Amount)


# Combine 'first name' and 'last name' into a new column 'cust_name'
raw_data['cust_name'] = raw_data['first_name'] + ' ' + raw_data['last_name']

# Remove the original 'first name' and 'last name' columns
raw_data = raw_data.drop(columns=['first_name', 'last_name'])

# Reorder columns to have 'cust_name' at the first position
columns_order = ['cust_name'] + [col for col in raw_data.columns if col != 'cust_name']
raw_data = raw_data[columns_order]

# Set 'cust_name' as the index of the DataFrame
raw_data.set_index('cust_name', inplace=True)

import mysql.connector
# Database connection details
host = 'localhost'
user = 'root'
password = 'password'
database = 'bonus_optimization_db'

# Establishing the connection
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
# Creating a cursor object
cursor = conn.cursor()
# pushing the cleaned data to MySQL db
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:password@Localhost/bonus_optimization_db')
raw_data.to_sql('bonus_info', con=engine, if_exists='replace', index=True)


from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


# Encoding of categorical variables
categorical_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)

# Standardization of numerical features
scaler = StandardScaler()
numerical_cols = ['age','income_level','Winning_percentage',
                  'Days_Since_Last_Bet','Active_Days',
                  'Total_Number_of_Bets','Total_Amount_Wagered',
                  'Average_Bet_Amount','Number_of_Bonuses_Received',
                  'Amount_of_Bonuses_Received','Revenue_from_Bonuses',
                  'Increase_in_Bets_After_Bonus',
                  'Increase_in_wagering_after_Bonus']
                  
categorical_cols = raw_data.select_dtypes(include=['object']).columns
                  
                  

preprocessor = ColumnTransformer(
    transformers=[
        ('num', scaler, numerical_cols),            # Only scaling for numerical columns
        ('cat', categorical_encoder, categorical_cols)  # Only encoding for categorical columns
    ])


# Applying the preprocessing pipeline to the raw data
preprocessed_data = preprocessor.fit_transform(raw_data)

# Converting the preprocessed data back into a DataFrame
preprocessed_data = pd.DataFrame(preprocessed_data, columns=(
    numerical_cols + 
    list(preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_cols))
))

preprocessed_data.shape


#converting dataframe to csv file
raw_data.to_csv('clean_data.csv', index=False)




