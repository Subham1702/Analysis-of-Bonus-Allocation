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

</details>
