# DSCI551_ChatDB71

This repository contains the codebase for our DSCI551 ChatDB Group 71 project, which enables natural language querying of movie metadata using both **MySQL** and **MongoDB**, powered by OpenAI's GPT-3.5.

---

## Overview

This project provides a Natural Language Interface (NLI) that translates user input into SQL or MongoDB queries. It supports:

- Data querying
- Schema exploration
- Data mutation (insert, update, delete)

### Databases Used

- **MySQL**: Stores structured data such as movie titles, ratings, and crew.
- **MongoDB**: Manages localized and alias movie data from `title.akas.tsv`.

---

## Prerequisites

- Python 3.8+
- pip / virtualenv
- MySQL installed and running locally
- MongoDB installed and running locally (on `localhost:27017`)
- Access to [OpenAI GPT-3.5 API](https://platform.openai.com/account/api-keys)

### Dataset Access

Due to GitHub’s file size limit, datasets are hosted on Google Drive:

- **MySQL**: [Download data.zip](https://drive.google.com/drive/folders/1wFFFx37nBeJFPEnGqU0D5iy4GDnKn_lk?usp=sharing)
- **MongoDB**: [Download TSV files](https://drive.google.com/drive/folders/17uRg72ne2JSUxMDWCgnb6Jzpj58EKrdN?usp=sharing)

---

## Setup Instructions

### MySQL Component (by Eason Lin)

```bash
cd MySQL
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
