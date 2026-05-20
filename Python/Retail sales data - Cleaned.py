#Retail sales Data - Cleaned

#importing libraries
import os
import pandas as pd
import numpy as np
import re
from rapidfuzz import process, fuzz
from word2number import w2n

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "..", "Data", "Retail sales data - Uncleaned.csv")

#df = pd.read_csv(file_path)

#To show full data
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_seq_items', None)

#Uploading data
df = pd.read_csv(file_path)

#Data info before cleaning

df.drop_duplicates(inplace=True)

#Cleaning date column

def clean_date(x):

    x = str(x).strip()

    # 1. Unix timestamp
    if x.isdigit() and len(x) in (10, 13):
        try:
            ts = int(x)
            if len(x) == 13:  # milliseconds
                ts = ts / 1000
            return pd.to_datetime(ts, unit='s')
        except:
            pass

    # 2. yyyy-mm-dd  → safe format (no warning)
    if re.match(r'^\d{4}-\d{2}-\d{2}$', x):
        return pd.to_datetime(x, format="%Y-%m-%d")

    # 3. dd/mm/yy or dd-mm-yyyy → use dayfirst=True
    if re.match(r'^\d{1,2}[/-]\d{1,2}[/-]\d{2,4}$', x):
        return pd.to_datetime(x, dayfirst=True)

    # 4. Month DD, YYYY  → January 17, 2021
    try:
        return pd.to_datetime(x, format="%B %d, %Y")
    except:
        pass

    # 5. DD Mon YYYY  → 13 Nov 2022
    try:
        return pd.to_datetime(x, format="%d %b %Y")
    except:
        pass

    # 6. If nothing works
    try:
        return pd.to_datetime(x, errors="coerce")
    except:
        return pd.NaT

df["date"] = df["date"].apply(clean_date)



#Cleaning transaction_id column

def clean_transaction_id(x):

    # 1. txn000123456 → TXN000123456
    x=str(x).strip().upper()

    # 2. 000123456 → TXN000123456
    if x.isdigit() and len(x) == 9:
        return "TXN"+x
    
    # 3. If nothing works
    return x

df["transaction_id"] = df["transaction_id"].apply(clean_transaction_id)
df["transaction_id"] = df["transaction_id"].replace("NAN", np.nan).astype("string")



#Cleaning customer_id column

def clean_customer_id(x):

    # 1. cust123456 → CUST123456
    x=str(x).strip().upper()
    return x

df["customer_id"] = df["customer_id"].apply(clean_customer_id)
df["customer_id"] = df["customer_id"].replace("NAN", np.nan).astype("string")



#Cleaning customer_phone_no column

def clean_phone(x):
    
    x = str(x).strip()
    
    # 1. Remove everything except digits
    digits = re.sub(r'\D', '', x)
    
    # 2. If number starts with India's country code 91
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]
    
    # 3. If number starts with 0 → remove it
    if digits.startswith("0") and len(digits) == 11:
        digits = digits[1:]
    
    # 4. Final check
    if len(digits) == 10:
        return digits
    
    return np.nan

df["customer_phone_no"] = df["customer_phone_no"].apply(clean_phone)

df["customer_phone_no"] = df["customer_phone_no"].astype('string')



#Cleaning customer_age column

def clean_age(x):
    
    x = str(x).strip()
    
    # 1. Remove everything except digits
    digits = re.sub(r'\D', '', x)

    # 2. If no digits
    if digits == '':
        return np.nan
    
    return digits

df["customer_age"] = df["customer_age"].apply(clean_age)

df["customer_age"] = pd.to_numeric(df["customer_age"], errors='coerce').round(0).astype("Int64")



#Cleaning customer_gender column

# 1. Capitalize the strings
df["customer_gender"] = df["customer_gender"].astype(str).str.strip().str.capitalize()

# 2. Replace M,F,O → Male, Female,  Other
df["customer_gender"] = df["customer_gender"].replace({'F':'Female','M':'Male','O':'Other','Nan':np.nan}).astype("string")



#Cleaning transaction_method column

# 1. Capitalize the strings
df["transaction_method"] = df["transaction_method"].astype(str).str.strip().str.capitalize()

# 2. Replace M,F,O → Male, Female,  Other
df["transaction_method"] = df["transaction_method"].replace({'Upi':'UPI','Emi':'EMI','Nan':np.nan}).astype("string")
  




#Cleaning product_category column

# 1. Basic cleaning(extract letters only)
df["product_category"] = (
    df["product_category"]
    .astype(str)
    .str.lower()
    .str.strip()
    .str.replace(r'[^a-z ]', '', regex=True)
    .str.replace(r'\s+', ' ', regex=True)
)

# 2. Product dictionary
correct_products = [
    "laptop", "laptop bag", "mobile", "tablet", "earphones", "charger",
    "keyboard", "mouse", "monitor", "pendrive", "memory card",
    "computer", "bluetooth speaker", "phone case", "cables"
]

# 3. Matching correct products
# def correct_product(x):
#     best_match = process.extractOne(x, correct_products, scorer=fuzz.WRatio)
#     if best_match[1] >= 70:
#         return best_match[0]
#     return x
def correct_product(x):

    # Handle null/empty values
    if pd.isna(x) or str(x).strip() == "":
        return np.nan

    best_match = process.extractOne(
        str(x),
        correct_products,
        scorer=fuzz.WRatio
    )

    # If no match found
    if best_match is None:
        return x

    # Confidence threshold
    if best_match[1] >= 70:
        return best_match[0]

    return x

df["product_category"] = df["product_category"].apply(correct_product)

df["product_category"] = df["product_category"].astype(str).str.title().replace('Nan',np.nan).astype("string")




#Cleaning brand_name column

# 1. Basic cleaning
df["brand_name"] = (
    df["brand_name"]
    .astype(str)
    .str.strip()
    .str.lower()
)
df["brand_name"] = df["brand_name"].replace("nan", np.nan)

# 2. Correct brands
correct_brands = [
    "samsung", "lg", "wildcraft", "aoc", "ambrane", "otterbox", "msi",
    "logitech", "lenovo", "xiaomi", "spigen", "generic", "bose", "asus",
    "sony", "casemate", "amazonbasics", "dell", "hp", "boat", "acer",
    "oppo", "skybags", "zebronics", "apple", "jio", "realme", "oneplus",
    "sandisk", "anker", "jbl", "sennheiser", "benq", "redragon",
    "kingston", "transcend", "vivo", "mi"
]

# 3. Matching correct brands
# def correct_brand(x):
#     if pd.isna(x):
#         return np.nan
#     match = process.extractOne(x, correct_brands, scorer=fuzz.WRatio)
#     if match and match[1] >= 80:
#         return match[0]
#     return x

def correct_brand(x):
    if pd.isna(x):
        return np.nan

    match = process.extractOne(
        str(x),
        correct_brands,
        scorer=fuzz.WRatio
    )

    if match is None:
        return x

    if match[1] >= 80:
        return match[0]

    return x

df["brand_name"] = df["brand_name"].apply(correct_brand)

df["brand_name"] = df["brand_name"].str.title()

df["brand_name"] = df["brand_name"].replace("Mi","Xiaomi")

df["brand_name"] = df["brand_name"].apply(lambda x: str(x).upper() if str(x) in ['Lg','Aoc','Msi','Hp','Jbl'] else x).astype("string")




#Cleaning city column

#1. Basic cleaning
df["city"] = (
    df["city"]
    .astype(str)
    .str.strip()
    .str.lower()
)
df["city"] = df["city"].replace("nan", np.nan)

# 2. Correct city names
correct_cities = [
    "hosur", "chennai", "madurai", "thiruvananthapuram", "puducherry",
    "mangalore", "coimbatore", "erode", "tirunelveli", "thanjavur",
    "vellore", "mysore", "salem", "bengaluru", "kochi", "tiruchirappalli"
]

# 3. Matching correct cities
# def correct_city(x):
#     if pd.isna(x):
#         return np.nan
#     match = process.extractOne(x, correct_cities, scorer=fuzz.WRatio)
#     if match and match[1] >= 80:
#         return match[0]
#     return x

def correct_city(x):
    if pd.isna(x):
        return np.nan

    match = process.extractOne(
        str(x),
        correct_cities,
        scorer=fuzz.WRatio
    )

    if match is None:
        return x

    if match[1] >= 80:
        return match[0]

    return x

df["city"] = df["city"].apply(correct_city)

df["city"] = df["city"].str.title().astype("string")




#Cleaning state column

state_mapping = df.dropna(subset=["state"]).set_index("city")["state"].to_dict()

df["state"] = df["state"].fillna(df["city"].map(state_mapping)).astype("string")

city_mapping = {"Puducherry" : "Puducherry"}

df["city"] = df["city"].fillna(df["state"].map(city_mapping)).astype("string")




#Cleaning unit_price column

def clean_amount(x):
    
    x = str(x).strip()

    temp = x.lower().replace("rs.", "").replace("rs", "").strip()
    temp = re.sub(r"[^a-z\s]", " ", temp)  # keep only letters for word check

    # 1. If written in words
    try:
        if re.fullmatch(r"[a-z\s]+", temp):     # words only
            return int(w2n.word_to_num(temp))
    except:
        pass

    # 2. Remove unnecessary charecters except digits
    x = re.sub(r"[^\d.]", "", x)

    if x.startswith('.'):
        return x[1:]

    # 3. Fill empties
    if x=="":
        return np.nan
    
    return float(x)

    
    
df["unit_price"] = df["unit_price"].apply(clean_amount)

df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")



#Cleaing cost column

def clean_cost(x):
    
    x = str(x).strip()

    # 1. If written in words
    try:
        if re.fullmatch(r"[a-z\s]+", x):     # words only
            return int(w2n.word_to_num(x))
    except:
        pass

    # 2. Remove unnecessary charecters except digits
    x = re.sub(r"[^\d.]", "", x)

    # 3. Fill empties
    if x=="":
        return np.nan
    
    return float(x)

df["cost"] = df["cost"].apply(clean_cost)

df["cost"] = pd.to_numeric(df["cost"], errors="coerce")




#Cleaning quantity column

df["quantity"] = df["quantity"].apply(lambda x : 1 if x == "one" else x)

df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").round(0).astype("Int64")



#Cleaning review_after_2_months column

def clean_digits(x):
    
    x = str(x).strip()

    # 1. If written in words
    try:
        if re.fullmatch(r"[a-z\s]+", x):     # words only
            return int(w2n.word_to_num(x))
    except:
        pass

    # 2. Remove unnecessary charecters except digits
    x = re.sub(r"[^\d.]", "", x)

    # 3. Fill empties
    if x=="":
        return np.nan
    
    return float(x)

df["review_after_2_months"] = df["review_after_2_months"].apply(clean_digits)

df["review_after_2_months"] = pd.to_numeric(df["review_after_2_months"], errors="coerce").round(0).astype("Int64")




#Creating sales_rep column

sales_rep_mapping = {
    "Chennai": "Aravindhan",
    "Coimbatore": "Suresh",
    "Tiruchirappalli": "Meena",
    "Bengaluru": "Praveenkumar",
    "Thiruvananthapuram": "Lekha",
    "Puducherry": "Mohana",
    "Mangalore": "Akash",
    "Tirunelveli": "Priya",
    "Thanjavur": "Anita",
    "Hosur": "Nivetha",
    "Mysore": "Deepa",
    "Kochi": "Vijay",
    "Vellore": "Rohit",
    "Madurai": "Ravikumar",
    "Erode": "Harish",
    "Salem": "Sanjay"
}

df["sales_rep"] = df["city"].map(sales_rep_mapping).astype("string")



#creating branch_id column

branch_id_mapping = {
    "hosur": "HOS4932",
    "chennai": "CHE7285",
    "madurai": "MAD6149",
    "thiruvananthapuram": "THI8507",
    "puducherry": "PUD9371",
    "mangalore": "MAN5824",
    "coimbatore": "COI7613",
    "erode": "ERO4598",
    "tirunelveli": "TIR3446",
    "thanjavur": "THA9052",
    "vellore": "VEL1287",
    "mysore": "MYS6730",
    "salem": "SAL8419",
    "bengaluru": "BEN5904",
    "kochi": "KOC2175",
    "tiruchirappalli": "TRI4681"
}

df["branch_id"] = df["city"].str.lower().map(branch_id_mapping).astype("string")


#Removing wrong allocated brand rows
category_brand_map = {
    "laptop": ["dell","hp","asus","acer","lenovo","msi","apple"],
    "laptop bag": ["wildcraft","skybags"],
    "mobile": ["samsung","xiaomi","realme","apple","vivo","oppo","oneplus","jio"],
    "tablet": ["samsung","apple","lenovo","xiaomi"],
    "earphones": ["boat","sony","jbl","realme","oneplus","sennheiser"],
    "charger": ["samsung","apple","xiaomi","anker","ambrane","boat","oneplus"],
    "keyboard": ["logitech","redragon","zebronics","hp","dell"],
    "mouse": ["logitech","redragon","zebronics","hp","dell"],
    "monitor": ["lg","samsung","benq","asus","aoc","dell","hp"],
    "pendrive": ["sandisk","kingston","transcend"],
    "memory card": ["sandisk","kingston","transcend"],
    "computer": ["dell","hp","lenovo","asus","acer","msi"],
    "bluetooth speaker": ["boat","jbl","sony","bose"],
    "phone case": ["spigen","casemate","otterbox","generic"],
    "cables": ["amazonbasics","boat","anker","zebronics"]
}

def valid_brand(row):
    category = str(row["product_category"]).strip().lower()
    brand = str(row["brand_name"]).strip().lower()

    valid_brands = category_brand_map.get(category, [])

    # If brand not in allowed list → mark row as invalid
    return brand in valid_brands

df = df[df.apply(valid_brand, axis=1)]

df = df.reset_index(drop=True)




#Replace outliers with nan (using IQR method)
cols = ["unit_price", "cost"]

def replace_outliers(group, col):
    Q1 = group[col].quantile(0.25)
    Q3 = group[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    return group[col].apply(lambda x: np.nan if x < lower or x > upper else x)

for c in cols:
    df[c] = df.groupby("brand_name")[c].transform(
        lambda x: replace_outliers(df.loc[x.index], c)
    )


#Replace outliers with nan (using ranges)
ranges = {
    "Bluetooth Speaker": (500, 30000),
    "Cables": (50, 2000),
    "Charger": (200, 10000),
    "Computer": (20000, 250000),
    "Earphones": (150, 25000),
    "Keyboard": (200, 15000),
    "Laptop": (20000, 350000),
    "Laptop Bag": (300, 10000),
    "Memory Card": (200, 10000),
    "Mobile": (5000, 180000),
    "Monitor": (4000, 60000),
    "Mouse": (100, 8000),
    "Pendrive": (200, 10000),
    "Phone Case": (50, 2000),
    "Tablet": (6000, 130000)
}

def remove_outlier(row, column_name):
    cat = row["product_category"]
    value = row[column_name]
    
    # missing value → keep as NaN
    if pd.isna(value):
        return np.nan
    
    # get allowed low–high range
    low, high = ranges.get(cat, (0, float("inf")))
    
    # outlier → convert to NaN
    if value < low or value > high:
        return np.nan
    
    return value

df["unit_price"] = df.apply(
    remove_outlier,
    axis=1,
    column_name="unit_price"
)


df["cost"] = df.apply(
    remove_outlier,
    axis=1,
    column_name="cost"
)




#cleaning null values
df.dropna(subset=["date"], inplace=True)

columns = ["transaction_id", "customer_id", "customer_phone_no",
           "product_category", "brand_name", "city", "state",
           "sales_rep", "branch_id"
           ]
df[columns] = df[columns].fillna("unknown")

df["customer_age"] = df["customer_age"].fillna(df["customer_age"].median())
df["customer_gender"] = df["customer_gender"].fillna(df["customer_gender"].mode()[0])
df["transaction_method"] = df["transaction_method"].fillna(df["transaction_method"].mode()[0])

columns = ["unit_price", "cost"]
for col in columns:
    df[col] = df[col].fillna(df.groupby(["product_category", "brand_name"])[col].transform('median'))
    df[col] = pd.to_numeric(df[col], errors='coerce')

df["quantity"] = df["quantity"].fillna(df["quantity"].median())
df["review_after_2_months"] = df["review_after_2_months"].fillna(0)


#Cleaning wrong cost values

df["cost"] = df.groupby(["product_category", "brand_name"])["cost"].transform(
    lambda x: x.mask(
        x > df.loc[x.index, "unit_price"],
        df.loc[x.index, "unit_price"] * 0.7
    )
)


#Creating total_price column

df["total_price"] = df["quantity"]*df["unit_price"]




#Creating profit column

df["profit"] = df["total_price"]-(df["quantity"]*df["cost"])




#Reorder columns
new_order = [
    "date", "transaction_id", "customer_id", "customer_phone_no",
    "customer_age", "customer_gender", "transaction_method",
    "product_category", "brand_name",

    # Move these before city
    "branch_id", "sales_rep",
    
    "city", "state",

    # Move quantity before cost
    "quantity", "cost",

    # Move these before review
    "unit_price", "total_price", "profit",

    "review_after_2_months"
]

df = df[new_order]


#Final check
print(df.isnull().sum())
print(df.shape)
print(df.dtypes)
print(df.columns)


#Save cleaned file

output_path = os.path.join(BASE_DIR, "..", "Data", "Retail sales data - Cleaned.csv")
df.to_csv(output_path, index=False)
