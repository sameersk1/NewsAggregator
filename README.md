# News Aggregator

## Overview

The News Aggregator is a Flask-based web application that scrapes news articles from multiple sources, categorizes them, and provides access via a REST API and a simple front-end interface. The application uses spaCy for text categorization and Beautiful Soup for web scraping.

## Features

- **Scraping**: Automatically scrape news articles from BBC and other sources.
- **Categorization**: Automatically categorize articles based on their content.
- **REST API**: Access articles via a RESTful API.
- **Front-End**: The front-end is built using simple **HTML** templates, styled with **CSS** for an appealing layout, and enhanced with **JavaScript** for dynamic interactions. This setup presents the articles in a user-friendly manner, allowing users to easily navigate through the articles and utilize the search functionality to find specific content.

## Requirements

To run this project, you need to have Python installed along with the following dependencies:

- Flask
- Pandas
- Requests
- BeautifulSoup4
- spaCy
- (Optionally) Other dependencies as specified in `requirements.txt`

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd news-aggregator

2. **Install requirements**:
   ```bash
   pip install -r requirements.txt

3. **Download spaCy model**:
   ```bash
   python -m spacy download en_core_web_sm

4. **Run the application:**
   ```bash   
   python app.py

## Access the Application

To access the application, open your browser and navigate to:

**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

## API Endpoints

### Get All Articles
- **Endpoint**: `GET /articles`
- **Description**: Retrieve a list of all articles.

### Get Article by ID
- **Endpoint**: `GET /articles/<int:article_id>`
- **Description**: Retrieve a specific article using its unique ID.

### Search Articles
- **Endpoint**: `GET /search?q=<query>`
- **Description**: Search for articles matching the query string.

## CSV File

The scraped articles are stored in the file **`news_articles.csv`**. This file will be automatically created after the first run of the application if it does not already exist.
