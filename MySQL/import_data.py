import pandas as pd
import mysql.connector

def insert_in_batches(cursor, query, data, batch_size=1000):
    total = len(data)
    for i in range(0, total, batch_size):
        batch = data[i:i+batch_size]
        cursor.executemany(query, batch)
        conn.commit()
        print(f"Inserted {i + len(batch)} of {total} rows")

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="movie_metadata"
)
cursor = conn.cursor()

### --- title.basics.tsv ---
print("📄 Loading title.basics.tsv...")
df_basics = pd.read_csv("./data/title.basics.tsv", sep="\t", dtype=str, na_values="\\N")
df_basics = df_basics.where(pd.notnull(df_basics), None)

insert_basics = """
INSERT IGNORE INTO title_basics
(tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
insert_in_batches(cursor, insert_basics, df_basics.values.tolist())

### --- title.ratings.tsv ---
print("📄 Loading title.ratings.tsv...")
df_ratings = pd.read_csv("./data/title.ratings.tsv", sep="\t", dtype=str, na_values="\\N")
df_ratings = df_ratings.where(pd.notnull(df_ratings), None)

insert_ratings = """
INSERT IGNORE INTO title_ratings
(tconst, averageRating, numVotes)
VALUES (%s, %s, %s)
"""
insert_in_batches(cursor, insert_ratings, df_ratings.values.tolist())

### --- title.principals.tsv ---
print("📄 Loading title.principals.tsv...")
df_principals = pd.read_csv("./data/title.principals.tsv", sep="\t", dtype=str, na_values="\\N")
df_principals = df_principals.where(pd.notnull(df_principals), None)

insert_principals = """
INSERT IGNORE INTO title_principals
(tconst, ordering, nconst, category, job, characters)
VALUES (%s, %s, %s, %s, %s, %s)
"""
insert_in_batches(cursor, insert_principals, df_principals.values.tolist())

cursor.close()
conn.close()
print("All data imported successfully!")