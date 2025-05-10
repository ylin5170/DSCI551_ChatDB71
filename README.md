# DSCI551_ChatDB71
This repository is for our DSCI551 ChatDB 71 group project 
Overview
This project enables natural language interaction with a MongoDB movie database using OpenAI's GPT-based model. Users can perform data queries, mutations (insert/update/delete), and schema exploration by typing conversational inputs.

Prerequisites
Make sure the following tools are installed:

Python 3.8+

MongoDB running locally (localhost:27017) with title_basics, title_akas, and title_ratings collections imported

OpenAI API access (GPT-3.5-Turbo)

pip / virtualenv or conda (for environment setup)


Due to GitHub's file size limitations, the full IMDB .tsv dataset used in this project has been uploaded to Google Drive.
https://drive.google.com/drive/folders/17uRg72ne2JSUxMDWCgnb6Jzpj58EKrdN?usp=sharing
Installation Steps
1.Clone the Repository
2.Create and Activate Virtual Environment
3.Install Required Dependencies
pip install -r requirements.txt
4.Add Your OpenAI API Key
5.Import MongoDB Data
Make sure title_basics, title_akas, and title_ratings are loaded into MongoDB.

Running the System
Start the terminal interface:
python main.py

You'll be prompted with:
Welcome to ChatDB (Mongo Edition)!
What would you like to do?

You can try examples like:

Show me the top 5 Japanese movies

Add a US English alias "Demo Movie" for tt0000001

Change the language of alias for tt0000001 to French

Delete the Chinese alias for tt0000001

Show samples from title_akas

Project Structure
main.py – Command line interface

query_parser.py – Converts NL queries to MongoDB pipelines

mutation_parser.py – Converts NL instructions into insert/update/delete actions

parser.py – Dispatches query or mutation routes

import_data.py – Optional utility for loading IMDB CSV data