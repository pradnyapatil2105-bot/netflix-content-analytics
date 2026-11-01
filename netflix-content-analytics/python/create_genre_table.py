import pandas as pd
from sqlalchemy import create_engine, URL

# ==========================================
# NETFLIX GENRE DATA PREPARATION
# ==========================================

print("===== NETFLIX GENRE DATA IMPORT =====")

# Read cleaned Netflix data
df = pd.read_csv("netflix_cleaned.csv")

# Select required columns
genre_df = df[["show_id", "title", "type", "listed_in"]].copy()

# Split multiple genres into separate rows
genre_df["genre"] = genre_df["listed_in"].str.split(", ")

# Convert each genre into a separate row
genre_df = genre_df.explode("genre")

# Remove extra spaces
genre_df["genre"] = genre_df["genre"].str.strip()

# Keep required columns
genre_df = genre_df[["show_id", "title", "type", "genre"]]

# Remove duplicate show_id-genre combinations
genre_df = genre_df.drop_duplicates(
    subset=["show_id", "genre"]
)

# Save separate CSV
genre_df.to_csv("netflix_genres.csv", index=False)

print("\nTotal Genre Records:", len(genre_df))

print("\n----- FIRST 10 RECORDS -----")
print(genre_df.head(10))

print("\nGenre CSV saved successfully as 'netflix_genres.csv'!")


# ==========================================
# MYSQL DATABASE CONNECTION
# ==========================================

print("\n===== MYSQL DATABASE IMPORT =====")

connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="raj@123",
    host="localhost",
    port=3306,
    database="netflix_analysis"
)

try:
    # Create database connection
    engine = create_engine(connection_url)

    # Import genre data into MySQL
    genre_df.to_sql(
        name="netflix_genres",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=500,
        method="multi"
    )

    # Verify total imported records
    result = pd.read_sql(
        "SELECT COUNT(*) AS total_genre_records FROM netflix_genres",
        engine
    )

    print("\nGenre table imported successfully!")
    print(result)

    # Preview data
    preview = pd.read_sql(
        "SELECT * FROM netflix_genres LIMIT 10",
        engine
    )

    print("\n----- MYSQL TABLE PREVIEW -----")
    print(preview)

    # Close connection
    engine.dispose()

except Exception as e:
    print("\nMYSQL ERROR:")
    print(e)

print("\n===== GENRE DATA IMPORT COMPLETED =====")