# Analysis-of-Bonus-Allocation
## Project Description:
### Business Problem:
The company is facing insufficiencies in it's bonus allocation process, leading to sub-optimal use of resources and customer dissatisfaction. The current method does not adequately align bonus distribution with key performance indicators (KPIs) and business goals, resulting in higher costs and lower customer motivation. There is a need for an efficient system to allocate bonuses that maximizes customer performance and satisfaction while staying within budget constraints.
### Business Objective: 
Maximize customer satisfaction, minimize variance in bonus distribution.
### Business Constraint: 
Maximize fairness in bonus distribution.
### Business Success Criteria: 
Achieving a 10% increase in profit margins through optimized bonus allocation.
### Economic Success Criteria: 
Generating a 20% increase in revenue from the solution within the first year of implementation.

## Data Understanding:
Data Dimension = 5000 records, 19 attributes.
Data Dictionary:
![image](https://github.com/user-attachments/assets/f7adeae9-59b8-4344-bde2-c0d9db98b382)

## Exploratory Data Analysis(EDA) & Data Preprocessing:

<details>
  <summary>EDA using MySQL</summary>
	
  ```SQL
create database if not exists bonus_optimization_db;
use bonus_optimization_db;
drop table bonus_alloc;
create table if not exists bonus_alloc (
cust_id INT not null,
f_n VARCHAR(20) NOT NULL,
l_n VARCHAR(20) NOT NULL,
country TEXT NOT NULL,
age INT NOT NULL,
gender VARCHAR(10) NOT NULL,
income_level BIGINT NOT NULL,
win_pert INT NOT NULL,
days_since_last_bet INT NOT NULL,
active_days INT NOT NULL,
total_no_of_bets INT NOT NULL,
total_amt_wagered BIGINT NOT NULL,
avg_bet_amt INT NOT NULL,
no_of_bonus_rcvd INT NOT NULL,
amt_of_bonus_rcvd INT NOT NULL,
rev_from_bonus INT NOT NULL,
incr_bets_after_bonus INT NOT NULL,
incr_wager_after_bonus BIGINT NOT NULL,
should_rcv_bonus INT NOT NULL
);

select * from bonus_alloc;

											# EDA #
# Customer Age statistics:
SELECT 
    AVG(age) AS avg_age,
    MIN(age) AS min_age,
    MAX(age) AS max_age,
    STDDEV(age) AS stddev_age
FROM 
    bonus_alloc;
    
# Income level statistics:    
SELECT 
    AVG(income_level) AS avg_income,
    MIN(income_level) AS min_income,
    MAX(income_level) AS max_income,
    STDDEV(income_level) AS stddev_income
FROM 
    bonus_alloc;
    
# Betting behavior statistics:
SELECT 
    AVG(win_pert) AS avg_winning_percentage,
    MIN(win_pert) AS min_winning_percentage,
    MAX(win_pert) AS max_winning_percentage,
    STDDEV(win_pert) AS stddev_winning_percentage
FROM 
    bonus_alloc;
    
# Total number of bets:
SELECT 
    AVG(total_no_of_bets) AS avg_total_bets,
    MIN(total_no_of_bets) AS min_total_bets,
    MAX(total_no_of_bets) AS max_total_bets,
    STDDEV(total_no_of_bets) AS stddev_total_bets
FROM 
    bonus_alloc;
                                       
# Total Amount wagered:
SELECT 
    AVG(total_amt_wagered) AS avg_total_wagered,
    MIN(total_amt_wagered) AS min_total_wagered,
    MAX(total_amt_wagered) AS max_total_wagered,
    STDDEV(total_amt_wagered) AS stddev_total_wagered
FROM 
    bonus_alloc;
    
# Average bet amount:
SELECT 
    AVG(avg_bet_amt) AS avg_bet_amount,
    MIN(avg_bet_amt) AS min_bet_amount,
    MAX(avg_bet_amt) AS max_bet_amount,
    STDDEV(avg_bet_amt) AS stddev_bet_amount
FROM 
    bonus_alloc;
    
# No of bonuses received:
SELECT 
    AVG(no_of_bonus_rcvd) AS avg_bonuses_received,
    MIN(no_of_bonus_rcvd) AS min_bonuses_received,
    MAX(no_of_bonus_rcvd) AS max_bonuses_received,
    STDDEV(no_of_bonus_rcvd) AS stddev_bonuses_received
FROM 
    bonus_alloc;
    
# Amount of bonuses received:
SELECT 
    AVG(amt_of_bonus_rcvd) AS avg_bonus_amount,
    MIN(amt_of_bonus_rcvd) AS min_bonus_amount,
    MAX(amt_of_bonus_rcvd) AS max_bonus_amount,
    STDDEV(amt_of_bonus_rcvd) AS stddev_bonus_amount
FROM 
    bonus_alloc;

# Revenue from bonuses:
SELECT 
    AVG(rev_from_bonus) AS avg_revenue_from_bonuses,
    MIN(rev_from_bonus) AS min_revenue_from_bonuses,
    MAX(rev_from_bonus) AS max_revenue_from_bonuses,
    STDDEV(rev_from_bonus) AS stddev_revenue_from_bonuses
FROM 
    bonus_alloc;

# Increase in bets after bonus:
SELECT 
    AVG(incr_bets_after_bonus) AS avg_increase_in_bets,
    MIN(incr_bets_after_bonus) AS min_increase_in_bets,
    MAX(incr_bets_after_bonus) AS max_increase_in_bets,
    STDDEV(incr_bets_after_bonus) AS stddev_increase_in_bets
FROM 
    bonus_alloc;

# Increase in wagering after bonus:
SELECT 
    AVG(incr_wager_after_bonus) AS avg_increase_in_wagering,
    MIN(incr_wager_after_bonus) AS min_increase_in_wagering,
    MAX(incr_wager_after_bonus) AS max_increase_in_wagering,
    STDDEV(incr_wager_after_bonus) AS stddev_increase_in_wagering
FROM 
    bonus_alloc;
    
# Unique values in categorical columns
SELECT gender, COUNT(*) AS count
FROM bonus_alloc
GROUP BY gender
ORDER BY count DESC;

SELECT country, COUNT(*) AS count
FROM bonus_alloc
GROUP BY country
ORDER BY count DESC;

# Distribution of numerical columns
SELECT
    FLOOR(age / 10) * 10 AS age_range_start,
    FLOOR(age / 10) * 10 + 9 AS age_range_end,
    COUNT(*) AS frequency
FROM bonus_alloc
GROUP BY age_range_start, age_range_end
ORDER BY age_range_start;

			## Data Preprocessing ##
# combining first name and last name into customer name
set sql_safe_updates = 0;
ALTER TABLE bonus_alloc
ADD COLUMN cust_name VARCHAR(255);
UPDATE bonus_alloc
SET cust_name = CONCAT(f_n, ' ', l_n);

ALTER TABLE bonus_alloc
DROP COLUMN f_n,
DROP COLUMN l_n;

# Outlier analysis:
-- Step 1: Calculate Q1 and Q3 using subqueries

-- This subquery calculates Q1 and Q3 for win_pert
WITH quartiles AS (
    SELECT 
        MIN(CASE WHEN cumulative_percentile >= 25 THEN win_pert END) AS Q1,
        MIN(CASE WHEN cumulative_percentile >= 75 THEN win_pert END) AS Q3
    FROM (
        SELECT 
            win_pert,
            100 * (ROW_NUMBER() OVER (ORDER BY win_pert) - 0.5) / COUNT(*) OVER () AS cumulative_percentile
        FROM bonus_alloc
    ) AS percentiles
)

-- Step 2: Update outliers in win_pert
UPDATE bonus_alloc
SET win_pert = CASE
    -- Replace values less than Q1 range with the minimum value within Q1 range
    WHEN win_pert < (
        SELECT Q1 - 1.5 * (Q3 - Q1)
        FROM quartiles
    ) THEN (
        SELECT MIN(win_pert)
        FROM bonus_alloc
        WHERE win_pert >= (SELECT Q1 FROM quartiles) AND win_pert <= (SELECT Q3 FROM quartiles)
    )
    -- Replace values greater than Q3 range with the maximum value within Q3 range
    WHEN win_pert > (
        SELECT Q3 + 1.5 * (Q3 - Q1)
        FROM quartiles
    ) THEN (
        SELECT MAX(win_pert)
        FROM bonus_alloc
        WHERE win_pert >= (SELECT Q1 FROM quartiles) AND win_pert <= (SELECT Q3 FROM quartiles)
    )
    ELSE win_pert
END;


# importing the clean dataset:
create table if not exists clean_data (
cust_id INT not null,
cust_name VARCHAR(30) NOT NULL,
country TEXT NOT NULL,
age INT NOT NULL,
gender VARCHAR(10) NOT NULL,
income_level BIGINT NOT NULL,
win_pert INT NOT NULL,
days_since_last_bet INT NOT NULL,
active_days INT NOT NULL,
total_no_of_bets INT NOT NULL,
total_amt_wagered BIGINT NOT NULL,
avg_bet_amt INT NOT NULL,
no_of_bonus_rcvd INT NOT NULL,
amt_of_bonus_rcvd INT NOT NULL,
rev_from_bonus INT NOT NULL,
incr_bets_after_bonus INT NOT NULL,
incr_wager_after_bonus BIGINT NOT NULL,
should_rcv_bonus INT NOT NULL
);

# querying insights from the dataset:
select * from clean_data;

#--customer statistics --
select count(distinct(cust_name)) from clean_data;   # 622 unique customers
select count(distinct(country)) from clean_data;     # 223 countries

select count(distinct(income_level)) from clean_data;
select max(income_level) from clean_data;            #149892
select min(income_level) from clean_data;			# 20021
# grouping customers based upon their age and income_level
ALTER TABLE clean_data
ADD COLUMN age_group VARCHAR(20),
ADD COLUMN income_group VARCHAR(20);
set sql_safe_updates = 0;
# --age grouping--
UPDATE clean_data
SET age_group = CASE
    WHEN age BETWEEN 18 AND 25 THEN '18-25'
    WHEN age BETWEEN 26 AND 35 THEN '26-35'
    WHEN age BETWEEN 36 AND 45 THEN '36-45'
    WHEN age BETWEEN 46 AND 55 THEN '46-55'
    WHEN age BETWEEN 56 AND 65 THEN '56-65'
    WHEN age BETWEEN 66 AND 75 THEN '66-75'
    WHEN age > 75 THEN '75+'
    ELSE 'Unknown'
END;
# --income_level grouping --
UPDATE clean_data
SET income_group = CASE
    WHEN income_level BETWEEN 0 AND 30000 THEN '0-30K'
    WHEN income_level BETWEEN 30001 AND 60000 THEN '30K-60K'
    WHEN income_level BETWEEN 60001 AND 90000 THEN '60K-90K'
    WHEN income_level BETWEEN 90001 AND 120000 THEN '90K-120K'
    WHEN income_level BETWEEN 120001 AND 150000 THEN '120K-150K'
    WHEN income_level > 150000 THEN '150K+'
    ELSE 'Unknown'
END;
select * from clean_data;
#-- age group recieving the highest bonus
SELECT age_group, SUM(amt_of_bonus_rcvd) AS total_bonus
FROM clean_data
GROUP BY age_group
ORDER BY total_bonus DESC LIMIT 1;
#-- customer activity in 46-55 age group
select max(income_group) from clean_data
WHERE age_group = '46-55';        #90 -120K

# highest revenue generator age-group:
select age_group, sum(rev_from_bonus) as total_revenue
from clean_data
group by age_group order by total_revenue DESC LIMIT 1;


select avg(total_amt_wagered) from clean_data WHERE age_group = '46-55' AND income_group = '90K-120K';
select max(total_amt_wagered) from clean_data WHERE age_group = '46-55' AND income_group = '90K-120K';

select count(distinct(cust_id)) from clean_data WHERE age_group = '46-55';
select count(distinct(country)) from clean_data WHERE age_group = '46-55';

SELECT AVG(win_pert) AS avg_winning_percentage FROM clean_data
WHERE age_group = '46-55';          #43%
SELECT avg(avg_bet_amt) FROM clean_data WHERE age_group = '46-55';    # 990
select count(distinct(total_no_of_bets)) from clean_data WHERE age_group = '46-55';
```
</details>

<details>
 <summary>EDA using Python</summary>
	
 ```python
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

```
</details>

## Data Visualization:
### Dashboard 1
![alt text](https://github.com/Subham1702/Analysis-of-Bonus-Allocation/blob/main/Screenshot%20(376).png)

### Dashboard 2
![alt text](https://github.com/Subham1702/Analysis-of-Bonus-Allocation/blob/main/Screenshot%20(377).png)

## Insights from the data analysis:
### Statistical Insights: -
1) Distribution of Winning Percentage.
 ``` Python
plt.figure(figsize=(8, 6))
plt.hist(data['Winning_percentage'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Winning Percentage')
plt.xlabel('Winning Percentage')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
```
![alt text](https://github.com/Subham1702/Analysis-of-Bonus-Allocation/blob/main/output%20(1).png)
Average Winning Percentage: 42.22% — This indicates that, on average, customers are winning about 42% of the time.

2) Correlation Between Active Days and Total Number of Bets.
 ``` Python
plt.figure(figsize=(8, 6))
plt.scatter(data['Active_Days'], data['Total_Number_of_Bets'], color='green')
plt.title('Correlation Between Active Days and Total Number of Bets')
plt.xlabel('Active Days')
plt.ylabel('Total Number of Bets')
plt.grid(True)
plt.show()
```
![alt text](https://github.com/Subham1702/Analysis-of-Bonus-Allocation/blob/main/output%20(2).png)
The correlation value is 0.21 — There is a weak positive correlation, suggesting that while more active customers tend to place more bets, the relationship is not particularly strong.

3) Bonus Allocation (Yes/No).
 ``` Python
plt.figure(figsize=(6, 6))
bonus_allocation_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightcoral'])
plt.title('Bonus Allocation (Yes/No)')
plt.ylabel('')
plt.show()
```
![alt text](https://github.com/Subham1702/Analysis-of-Bonus-Allocation/blob/main/output%20(3).png)
3593 customers should receive a bonus, while 1407 should not. This highlights a relatively balanced but slightly more frequent allocation towards receiving bonuses.

4) Average Revenue from Bonuses: 4991.88 — The revenue generated per customer from bonuses is approximately 5000, indicating the business value of offering bonuses.   


### Business Insights: -
1) Bonus Impact on Customer Behavior: The data shows a significant increase in the number of bets and the amount wagered after bonuses are given, implying that bonuses effectively drive engagement and potentially customer satisfaction.
2) Fairness in Bonus Allocation: The allocation of bonuses is mostly balanced, with a slightly higher proportion of customers receiving bonuses. This can be further optimized by considering key performance indicators to ensure alignment with business goals.
3) Revenue Generation from Bonuses: The average bonus revenue is high, indicating that the current bonus system contributes positively to the business. Further optimization of the bonus allocation process could lead to a more efficient system, reducing costs and enhancing profitability.

## Recommendations:
• Segment the customer base using data-driven insights, analyzing factors like winning percentage, active days, and increase in bets after bonuses to target high-engagement customers for bonus allocation.
• Align bonuses with KPIs, such as increased bets and wagering amounts, by analyzing the impact of bonuses on customer behavior to ensure that bonuses drive the desired outcomes.
• Evaluate fairness in bonus distribution by conducting statistical analyses on performance metrics and customer activity to ensure bonuses are allocated equitably.
• Implement dynamic bonus allocation models using real-time data analytics to adjust bonus amounts based on customers' evolving betting patterns.
• Monitor the impact of bonuses through continuous analysis of customer engagement post-bonus, using metrics like the increase in bets and revenue, and adjust strategies accordingly.
• Optimize bonus budgeting by performing cost-benefit analyses on bonus recipients, ensuring bonuses are allocated efficiently to maximize return on investment (ROI).
• Leverage A/B testing and other experimental methods to test different bonus strategies and identify the most effective bonus structures for various customer segments based on data insights.

