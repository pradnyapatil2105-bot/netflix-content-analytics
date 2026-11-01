# Netflix Content Analytics

## Project Overview
Netflix Content Analytics is a data analysis project that explores Netflix's movies and TV shows catalogue. The project uses Python, MySQL, and Tableau to clean, analyze, and visualize content-related data.

## Dashboard Preview
![Netflix Dashboard](netflix-content-analytics/images/Dashboard%201.png)


## Tools & Technologies
- Python: Data cleaning and exploratory data analysis
- Pandas: Data manipulation
- MySQL: Data storage and SQL analysis
- Tableau: Interactive dashboard and visualization

## Project Structure
```text
netflix-content-analytics/
├── data/
│   ├── netflix_cleaned.csv
│   ├── netflix_genres.csv
│   └── ntfx_prjct_data.txt
├── images/
│   └── Dashboard 1.png
├── python/
│   ├── main.py
│   └── create_genre_table.py
├── sql/
│   └── sql.sql
└── tableau/
    └── netflix_dashboard.twbx
```

## Key Analysis
- Movies vs TV Shows distribution
- Top 10 genres
- Top 10 countries
- Release year trends
- Content ratings analysis
- Content type trends over release years

## Key Insights (all release years)
- The catalogue has 6,234 titles: 4,265 movies (68.4%) and 1,969 TV shows (31.6%)
- The United States has the most titles, followed by India
- TV-MA and TV-14 are the most common ratings

## Dashboard
The Tableau dashboard presents Netflix catalogue insights through KPI cards, bar charts, a donut chart, a line chart, and a stacked area chart. It includes a Release Year filter and a Top N parameter.

## Data Cleaning
Python and Pandas were used to handle missing values, clean text fields, extract duration values, and prepare the dataset for analysis.

## Project Objective
To explore and understand the distribution and characteristics of Netflix content using data analysis and visualization tools.

## Author
Pradnya Patil  
[LinkedIn](https://linkedin.com/in/pradnya-patil-8a97b4370)
