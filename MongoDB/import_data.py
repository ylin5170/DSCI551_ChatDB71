import pandas as pd

df1 = pd.read_csv('title.basics.tsv', sep='\t', dtype=str)
df1.to_json('title_basics.json', orient='records', lines=False)

df2 = pd.read_csv('title.akas.tsv', sep='\t', dtype=str)
df2.to_json('title_akas.json', orient='records', lines=False)

df3 = pd.read_csv('title.ratings.tsv', sep='\t', dtype=str)
df3.to_json('title_ratings.json', orient='records', lines=False)

#After that I used mongoimport to import data into MongoDb
#mongoimport --db IMDB --collection title_basics --file title_basics.json --jsonArray
#mongoimport --db IMDB --collection title_akas --file title_akas.json --jsonArray
#mongoimport --db IMDB --collection title_ratings --file title_ratings.json --jsonArray