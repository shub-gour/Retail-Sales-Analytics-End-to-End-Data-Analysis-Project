#Creating database
CREATE DATABASE IF NOT EXISTS retail_analyze;

#Use the database
USE retail_analyze;

#Creating table retail_cleaned
CREATE TABLE retail_cleaned (
    date DATE,
    transaction_id VARCHAR(20),
    customer_id VARCHAR(20),
    customer_phone_no VARCHAR(20),
    customer_age INT,
    customer_gender VARCHAR(10),
    transaction_method VARCHAR(10),
    product_category VARCHAR(50),
    brand_name VARCHAR(20),
    branch_id VARCHAR(10),
    sales_rep VARCHAR(20),
    city VARCHAR(20),
    state VARCHAR(20),
    quantity INT,
    cost DECIMAL(15,2),
    unit_price DECIMAL(15,2),
    total_price DECIMAL(15,2),
    profit DECIMAL(15,2),
    review_after_2_months INT
);

-- Update the file path according to your local MySQL upload directory
#Uploading Retail sales data - Cleaned.csv into retail_cleaned table
LOAD DATA INFILE 
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Retail sales data - Cleaned.csv'
INTO TABLE retail_cleaned
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

#Retrieving all data from the retail_cleaned
SELECT * FROM retail_cleaned;

#Creating view for overall data KPI
CREATE VIEW kpi_retail AS
SELECT SUM(total_price) AS Total_sales,
       SUM(profit) AS Total_profit,
       AVG(total_price) AS Avg_sales,
       SUM(quantity) AS Prod_sold,
       COUNT(DISTINCT customer_id) AS Total_cust
FROM retail_cleaned;

SELECT * FROM kpi_retail;

#Creating view for yearly KPI
CREATE VIEW kpi_per_year AS
SELECT YEAR(date) AS Year,
       SUM(total_price) AS Total_sales,
       SUM(profit) AS Total_profit,
       AVG(total_price) AS Avg_sales,
       SUM(quantity) AS Prod_sold,
       COUNT(DISTINCT customer_id) AS Total_cust
FROM retail_cleaned
GROUP BY YEAR(date);

SELECT * FROM kpi_per_year;

#Creating view for sales, profit, quantity by year
CREATE VIEW year_sales AS
SELECT YEAR(date) AS Year,
	   SUM(total_price) AS Sales,
       SUM(profit) AS Profit,
       SUM(quantity) AS prod_sold
FROM retail_cleaned
GROUP BY YEAR(date)
ORDER BY YEAR(date);

SELECT * FROM year_sales;

#Creating view for sales, profit, quantity by monthly for each year
CREATE VIEW month_sales AS
SELECT YEAR(date) AS Year,
       MONTHNAME(date) AS Month,
	   SUM(total_price) AS Sales,
       SUM(profit) AS Profit,
       SUM(quantity) AS prod_sold
FROM retail_cleaned
GROUP BY YEAR(date), MONTH(date), MONTHNAME(date)
ORDER BY YEAR(date), MONTH(date);

SELECT * FROM month_sales;

#Creating view for sales, profit, quantity by quarterly for each year
CREATE VIEW qtr_sales AS
SELECT YEAR(date) AS Year,
       QUARTER(date) AS Quarter,
	   SUM(total_price) AS Sales,
       SUM(profit) AS Profit,
       SUM(quantity) AS prod_sold
FROM retail_cleaned
GROUP BY YEAR(date), QUARTER(date)
ORDER BY YEAR(date), QUARTER(date);

SELECT * FROM qtr_sales;

#Creating view for sales, profit, quantity, profit margin by products
CREATE VIEW cat_sales AS
SELECT product_category,
	   SUM(total_price) AS Sales,
       SUM(profit) AS Profit,
       SUM(quantity) AS prod_sold,
       ROUND((SUM(profit)/SUM(total_price))*100, 1) AS prof_marg
FROM retail_cleaned
GROUP BY product_category
ORDER BY product_category;

SELECT * FROM cat_sales;

#Creating view for sales, profit, quantity, profit margin by brand
CREATE VIEW brand_sales AS
SELECT brand_name,
	   SUM(total_price) AS Sales,
       SUM(profit) AS Profit,
       SUM(quantity) AS prod_sold,
       ROUND((SUM(profit)/SUM(total_price))*100, 1) AS prof_marg
FROM retail_cleaned
GROUP BY brand_name
ORDER BY brand_name;

SELECT * FROM brand_sales;

#Creating view for sales, profit, quantity, profit margin by category and brand
CREATE VIEW cat_brand_sales AS
SELECT product_category,
       brand_name,
	   SUM(total_price) AS Sales,
       SUM(profit) AS Profit,
       SUM(quantity) AS prod_sold,
       ROUND((SUM(profit)/SUM(total_price))*100, 1) AS prof_marg
FROM retail_cleaned
GROUP BY product_category,brand_name
ORDER BY product_category,brand_name;

SELECT * FROM cat_brand_sales;

#Creating view for sales, profit, quantity by state
CREATE VIEW state_sales AS
SELECT state,
	   SUM(total_price) AS Sales,
       SUM(profit) AS Profit,
       SUM(quantity) AS prod_sold
FROM retail_cleaned
GROUP BY state
ORDER BY state;

SELECT * FROM state_sales;

#Creating view for sales, profit, quantity by city 
CREATE VIEW city_sales AS
SELECT city,
	   SUM(total_price) AS Sales,
       SUM(profit) AS Profit,
       SUM(quantity) AS prod_sold
FROM retail_cleaned
GROUP BY city
ORDER BY city;

SELECT * FROM city_sales;

#Creating view for sales, profit, quantity by state and city
CREATE VIEW state_city_sales AS
SELECT state,
       city,
	   SUM(total_price) AS Sales,
       SUM(profit) AS Profit,
       SUM(quantity) AS prod_sold
FROM retail_cleaned
GROUP BY state, city
ORDER BY state, city;

SELECT * FROM state_city_sales;

#Creating view for customers handled by sales rep
CREATE VIEW salrep_cust AS
SELECT sales_rep,
	   COUNT(DISTINCT customer_id) AS cust_handled
FROM retail_cleaned
GROUP BY sales_rep
ORDER BY cust_handled DESC;

SELECT * FROM salrep_cust;

#Creating view for sales, profit, quantity by sales rep
CREATE VIEW salrep_sales AS
SELECT sales_rep,
	   SUM(total_price) AS Sales,
       SUM(profit) AS Profit,
       SUM(quantity) AS prod_sold
FROM retail_cleaned
GROUP BY sales_rep
ORDER BY sales_rep;

SELECT * FROM salrep_sales;

#Creating view for sales, profit, quantity by gender
CREATE VIEW gender_sales AS
SELECT customer_gender,
	   SUM(total_price) AS Sales,
       SUM(profit) AS Profit,
       SUM(quantity) AS prod_sold
FROM retail_cleaned
GROUP BY customer_gender
ORDER BY customer_gender;

SELECT * FROM gender_sales;

#Creating view for sales, profit, quantity by age group
CREATE VIEW age_sales AS
SELECT 
    CASE 
        WHEN customer_age BETWEEN 15 AND 25 THEN '15-25'
        WHEN customer_age BETWEEN 26 AND 35 THEN '26-35'
        WHEN customer_age BETWEEN 36 AND 45 THEN '36-45'
        WHEN customer_age BETWEEN 46 AND 60 THEN '46-60'
        WHEN customer_age > 60 THEN '60+'
        ELSE 'Unknown'
    END AS age_group,
    SUM(total_price) AS Total_sales,
    SUM(profit) AS Profit,
    SUM(quantity) AS Prod_sold
FROM retail_cleaned
GROUP BY age_group
ORDER BY age_group;

SELECT * FROM age_sales;

#Creating view for transaction method counts
CREATE VIEW trans_mthd AS
SELECT transaction_method,
       COUNT(transaction_method) AS Transaction
FROM retail_cleaned
GROUP BY transaction_method
ORDER BY Transaction DESC;

SELECT * FROM trans_mthd;

#Creating view for Customer Lifetime Value
CREATE VIEW CLV AS
SELECT customer_id,
       SUM(total_price) AS Total_sales
FROM retail_cleaned
GROUP BY customer_id
HAVING customer_id <> 'unknown'
ORDER BY Total_sales DESC;

SELECT * FROM CLV;

#Creating view for Repeated customers
CREATE VIEW revisit_cust AS
SELECT customer_id,
       COUNT(customer_id) AS revisit_cnt
FROM retail_cleaned
GROUP BY customer_id
HAVING COUNT(customer_id) > 1 AND customer_id <> 'unknown'
ORDER BY revisit_cnt DESC;

SELECT * FROM revisit_cust;

#Creating view for rating by brand
CREATE VIEW brand_rating AS
SELECT brand_name,
       ROUND(AVG(review_after_2_months),1) AS Rate
FROM retail_cleaned
WHERE review_after_2_months <> 0
GROUP BY brand_name
ORDER BY Rate DESC;

SELECT * FROM brand_rating;

#Creating view for rating by products
CREATE VIEW cat_rating AS
SELECT product_category,
       ROUND(AVG(review_after_2_months),1) AS Rate
FROM retail_cleaned
WHERE review_after_2_months <> 0
GROUP BY product_category
ORDER BY Rate DESC;

SELECT * FROM cat_rating;

#Creating view for rating by products and brand
CREATE VIEW cat_brand_rating AS
SELECT product_category,
	   brand_name,
       ROUND(AVG(review_after_2_months),1) AS Rate
FROM retail_cleaned
WHERE review_after_2_months <> 0
GROUP BY product_category,brand_name
ORDER BY product_category, Rate DESC;

SELECT * FROM cat_brand_rating;

#Creating Procedure for Top 5 by sales
DELIMITER $$
CREATE PROCEDURE top5(IN col_name VARCHAR(100))
BEGIN
    SET @sql = CONCAT('
        SELECT ', col_name, ',
               SUM(total_price) AS Total_sales,
               SUM(profit) AS Profit,
               SUM(quantity) AS Prod_sold
        FROM retail_cleaned
        WHERE ', col_name, ' <> ''unknown''
        GROUP BY ', col_name, '
        ORDER BY Total_sales DESC
        LIMIT 5;
    ');
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END $$
DELIMITER ;

#Calling the Procedure top5
CALL top5('customer_id');
CALL top5('sales_rep');
CALL top5('branch_id');
CALL top5('product_category');
CALL top5('brand_name');

#Creating Procedure for Bottom 5 by sales
DELIMITER $$
CREATE PROCEDURE bottom5(IN col_name VARCHAR(100))
BEGIN
    SET @sql = CONCAT('
        SELECT ', col_name, ',
               SUM(total_price) AS Total_sales,
               SUM(profit) AS Profit,
               SUM(quantity) AS Prod_sold
        FROM retail_cleaned
        WHERE ', col_name, ' <> ''unknown''
        GROUP BY ', col_name, '
        ORDER BY Total_sales
        LIMIT 5;
    ');
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END $$
DELIMITER ;

#Calling the procedure bottom5
CALL bottom5('sales_rep');
CALL bottom5('branch_id');
CALL bottom5('product_category');
CALL bottom5('brand_name');

#Creating function for Average Order Value
DELIMITER $$
CREATE FUNCTION AOV(total_sales DECIMAL(15,2), orders INT)
RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
    RETURN total_sales / orders;
END $$
DELIMITER ;

#Creating function for Profit Margin
DELIMITER $$
CREATE FUNCTION PROMAR(profit DECIMAL(15,2), total_sales DECIMAL(15,2) )
RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
    RETURN (profit/total_sales)*100;
END $$
DELIMITER ;

#Creating view for calculated KPI(AOV, Profit Margin, Count of Repeated customers)
CREATE VIEW cal_kpi AS
SELECT AOV(SUM(total_price),COUNT(DISTINCT transaction_id)) AS AOV,
       PROMAR(SUM(profit),SUM(total_price)) AS Profit_margin,
       (SELECT COUNT(customer_id) FROM revisit_cust) AS repeated_cust
FROM retail_cleaned;

SELECT * FROM cal_kpi;