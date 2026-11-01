import pandas as pd
from sqlalchemy import create_engine, URL, text


# ==========================================
# 1. LOAD NETFLIX DATASET
# ==========================================

print("\n===== NETFLIX DATA ANALYSIS PROJECT =====")

file_path = "ntfx_prjct_data.txt"

try:
    df = pd.read_csv(file_path, encoding="utf-8")
    print("\nDataset loaded successfully!")

except FileNotFoundError:
    print(f"\nERROR: File '{file_path}' was not found.")
    print("Make sure the dataset file is in the same folder as your Python script.")
    exit()

except Exception as e:
    print("\nERROR while loading dataset:")
    print(e)
    exit()


# ==========================================
# 2. DATASET OVERVIEW
# ==========================================

print("\n----- FIRST 5 RECORDS -----")
print(df.head())

print("\n----- DATASET INFORMATION -----")
df.info()

print("\nTotal Rows:", df.shape[0])
print("Total Columns:", df.shape[1])

print("\n----- MISSING VALUES -----")
print(df.isnull().sum())


# ==========================================
# 3. DATA QUALITY ANALYSIS
# ==========================================

print("\n===== DATA QUALITY ANALYSIS =====")

print("\n----- DUPLICATE RECORDS -----")
print("Total Duplicates:", df.duplicated().sum())

print("\n----- CONTENT TYPE -----")
print(df["type"].value_counts())

print("\n----- UNIQUE GENRE COMBINATIONS -----")
print("Total Genre Combinations:", df["listed_in"].nunique())


# ==========================================
# 4. DATA CLEANING
# ==========================================

print("\n===== DATA CLEANING =====")

# Create a copy to preserve original data
cleaned_df = df.copy()


# Remove extra spaces from text columns
text_columns = [
    "type",
    "title",
    "director",
    "cast",
    "country",
    "date_added",
    "rating",
    "duration",
    "listed_in",
    "description"
]

for col in text_columns:
    if col in cleaned_df.columns:
        cleaned_df[col] = cleaned_df[col].astype("string").str.strip()


# Remove duplicate records
duplicates_before = cleaned_df.duplicated().sum()

if duplicates_before > 0:
    cleaned_df = cleaned_df.drop_duplicates()
    print(f"\nRemoved {duplicates_before} duplicate records.")
else:
    print("\nNo duplicate records found.")


# Handle missing values
missing_columns = ["director", "cast", "country", "rating"]

for col in missing_columns:
    if col in cleaned_df.columns:
        cleaned_df[col] = cleaned_df[col].fillna("Not Specified")


# Convert date_added into datetime
if "date_added" in cleaned_df.columns:
    cleaned_df["date_added"] = pd.to_datetime(
        cleaned_df["date_added"],
        format="%B %d, %Y",
        errors="coerce"
    )


# Extract duration number
if "duration" in cleaned_df.columns:

    cleaned_df["duration_int"] = pd.to_numeric(
        cleaned_df["duration"]
        .str.extract(r"(\d+)")[0],
        errors="coerce"
    )

    # Extract duration type
    cleaned_df["duration_type"] = (
        cleaned_df["duration"]
        .str.extract(r"([A-Za-z]+)")[0]
    )


print("\n----- MISSING VALUES AFTER CLEANING -----")
print(cleaned_df.isnull().sum())

print("\n----- CLEANED DATASET SHAPE -----")
print("Rows:", cleaned_df.shape[0])
print("Columns:", cleaned_df.shape[1])


# ==========================================
# 5. SAVE CLEANED DATASET AS CSV
# ==========================================

output_file = "netflix_cleaned.csv"

try:
    cleaned_df.to_csv(
        output_file,
        index=False,
        date_format="%Y-%m-%d"
    )

    print(f"\nCleaned dataset saved successfully as '{output_file}'!")

except Exception as e:
    print("\nERROR while saving cleaned dataset:")
    print(e)


# ==========================================
# 6. EXPLORATORY DATA ANALYSIS
# ==========================================

print("\n===== EXPLORATORY DATA ANALYSIS =====")


# Movies vs TV Shows
print("\n----- MOVIES VS TV SHOWS -----")
print(cleaned_df["type"].value_counts())


# Top 10 Countries
print("\n----- TOP 10 COUNTRIES -----")

top_countries = (
    cleaned_df["country"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
)

print(top_countries)


# Top 10 Genres
print("\n----- TOP 10 GENRES -----")

top_genres = (
    cleaned_df["listed_in"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
)

print(top_genres)


# Content Ratings
print("\n----- TOP 10 CONTENT RATINGS -----")
print(cleaned_df["rating"].value_counts().head(10))


# Year Wise Content
print("\n----- YEAR WISE CONTENT -----")

print(
    cleaned_df["release_year"]
    .value_counts()
    .sort_index()
    .tail(10)
)


# Movie Duration Analysis
print("\n----- MOVIE DURATION ANALYSIS -----")

movie_duration = cleaned_df.loc[
    cleaned_df["type"] == "Movie",
    "duration_int"
].dropna()

print(movie_duration.describe())


# ==========================================
# 7. MYSQL DATABASE CONNECTION
# ==========================================

print("\n===== MYSQL DATABASE IMPORT =====")

# MySQL connection details
connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="raj@123",
    host="localhost",
    port=3306,
    database="netflix_analysis"
)

engine = None

try:
    # Create MySQL engine
    engine = create_engine(connection_url)

    print("\nTesting MySQL connection...")

    # Test connection
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("MySQL connection successful!")


    # ==========================================
    # 8. IMPORT DATA INTO MYSQL
    # ==========================================

    print("\nImporting cleaned data into MySQL...")

    cleaned_df.to_sql(
        name="netflix_titles",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=500,
        method="multi"
    )

    print("Data imported successfully!")


    # ==========================================
    # 9. VERIFY MYSQL IMPORT
    # ==========================================

    result = pd.read_sql(
        text("SELECT COUNT(*) AS total_records FROM netflix_titles"),
        engine
    )

    print("\n----- MYSQL IMPORT RESULT -----")
    print(result)


    # Display first 5 records from MySQL
    preview = pd.read_sql(
        text("SELECT * FROM netflix_titles LIMIT 5"),
        engine
    )

    print("\n----- MYSQL TABLE PREVIEW -----")
    print(preview)


except Exception as e:

    print("\n===== MYSQL CONNECTION OR IMPORT ERROR =====")
    print("Error details:")
    print(e)

    print("\nTroubleshooting:")
    print("1. Make sure MySQL service is running.")
    print("2. Check MySQL username and password.")
    print("3. Make sure database 'netflix_analysis' exists.")
    print("4. Install required packages:")
    print("   pip install pandas sqlalchemy pymysql")


finally:

    # Close connection
    if engine is not None:
        engine.dispose()
        print("\nMySQL connection closed.")


# ==========================================
# 10. PROJECT COMPLETION
# ==========================================

print("\n==========================================")
print("===== PROJECT EXECUTION COMPLETED =====")
print("==========================================")