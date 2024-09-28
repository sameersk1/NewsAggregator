from flask import Flask, jsonify, request, render_template
import pandas as pd
import requests
from bs4 import BeautifulSoup
import spacy
import os
from datetime import datetime

app = Flask(__name__)

# CSV file path for storing the scraped and categorized articles
CSV_FILE = 'news_articles.csv'

# Load the spaCy model for categorization
nlp = spacy.load('en_core_web_sm')

# Scraper function
def scrape_bbc_news():
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []

    # Find all article elements on the page
    for article in soup.find_all('article'):
        # Find all title elements within each article
        title_tags = article.find_all('h2')  # Assuming titles are in <h2> tags
        titles = [title.get_text().strip() for title in title_tags]  # Get all titles

        # Find all summary elements within each article
        summary_tags = article.find_all('p')  # Assuming summaries are in <p> tags
        summaries = [summary.get_text().strip() for summary in summary_tags]  # Get all summaries

        # Find all link elements within each article
        link_tags = article.find_all('a', href=True)  # Find all <a> tags with href
        links = [f"https://www.bbc.com{link['href']}" for link in link_tags]  # Get all links

        # Optional: Extract publication date (currently set to None)
        publication_date = "25-10-10"

        # Source
        source = "BBC"

        # Append all data, if titles and links are found
        if titles and links:
            for title, link,summary in zip(titles, links,summaries):
                # Adding one title per row; summary can be the first <p> found (or blank)
               
                articles.append({
                    'Title': title,
                    'Summary': summary,
                    'Publication Date': publication_date,
                    'Source': source,
                    'URL': link
                })

    # Save the scraped articles to a CSV file
    if articles:
        df = pd.DataFrame(articles)
        df.to_csv(CSV_FILE, index=False)
        print(f"Scraped {len(articles)} articles and saved to 'bbc_news_articles.csv'")
    else:
        print("No articles found.")

# Categorizer function
def categorize_articles():
    if not os.path.exists(CSV_FILE):
        print("No CSV file found. Please scrape data first.")
        return

    # Load the articles from the existing CSV file
    df = pd.read_csv(CSV_FILE)

    def categorize(text):
        if pd.isnull(text):
            return 'General'  # Default category for NaN values

        # Process the text with spaCy
        doc = nlp(text.lower())  # Convert text to lowercase for consistency

        # Keywords for categorization
        # Keywords for categorization
        politics_keywords = [
            'election', 'government', 'policy', 
            'politics', 'campaign', 'Kashmir', 
            'Hezbollah', 'Israel', 'Lebanon'
        ]

        technology_keywords = [
            'tech', 'software', 'AI', 
            'gadget', 'innovation', 'robotics','research', 'discovery', 'study', 
            'experiment'
        ]

        sports_keywords = [
            'sports', 'football', 'basketball', 
            'tournament', 'game', 'rugby', 
            'cricket', 'championship'
        ]

        health_keywords = [
            'health', 'medicine', 'disease', 
            'vaccine', 'treatment'
        ]

        entertainment_keywords = [
            'movie', 'music', 'celebrity', 
            'show', 'theater'
        ]

        business_keywords = [
            'business', 'economy', 'finance', 
            'market', 'investment'
        ]

        environment_keywords = [
            'climate', 'pollution', 'conservation', 
            'wildlife', 'ecosystem'
        ]

        disaster_keywords = [
            'storm', 'earthquake', 'flood', 
            'devastation'
        ]

        crime_keywords = [
            'shooting', 'attack', 'manhunt', 
            'murder'
        ]

        science_keywords = [
            
        ]


        # Check for keywords in the article summary
        if any(keyword in doc.text for keyword in politics_keywords):
            return 'Politics'
        elif any(keyword in doc.text for keyword in technology_keywords):
            return 'Technology'
        elif any(keyword in doc.text for keyword in sports_keywords):
            return 'Sports'
        elif any(keyword in doc.text for keyword in health_keywords):
            return 'Health'
        elif any(keyword in doc.text for keyword in entertainment_keywords):
            return 'Entertainment'
        elif any(keyword in doc.text for keyword in disaster_keywords):
            return 'Disaster'
        elif any(keyword in doc.text for keyword in crime_keywords):
            return 'Crime'
        else:
            return 'General'  # Default category if no keywords match

    # Apply the categorization function to the Summary column
    df['Category'] = df['Summary'].apply(categorize)

    # Save the updated DataFrame back to CSV
    df.to_csv(CSV_FILE, index=False)

# Load articles from the CSV
def load_articles():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame()

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')  # Assuming an index.html file exists in the 'templates' folder

@app.route('/articles', methods=['GET'])
def get_articles():
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    df = load_articles()

    if df.empty:
        return jsonify({"error": "No data found. Please scrape and categorize first."}), 404

    # Filter by category if specified
    if category:
        filtered_df = df[df['Category'].str.contains(category, case=False)]
    else:
        filtered_df = df

    # Filter by date range if specified
    if start_date or end_date:
        # Convert 'Publication Date' to datetime
        filtered_df['Publication Date'] = pd.to_datetime(filtered_df['Publication Date'], errors='coerce')

        # Apply date filters
        if start_date:
            filtered_df = filtered_df[filtered_df['Publication Date'] >= pd.to_datetime(start_date)]
        if end_date:
            filtered_df = filtered_df[filtered_df['Publication Date'] <= pd.to_datetime(end_date)]

    return jsonify(filtered_df.to_dict(orient='records'))

@app.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    df = load_articles()
    if df.empty:
        return jsonify({"error": "No data found. Please scrape and categorize first."}), 404

    if article_id < len(df):
        return jsonify(df.iloc[article_id].to_dict())
    else:
        return jsonify({'error': 'Article not found'}), 404

@app.route('/search', methods=['GET'])
def search_articles():
    query = request.args.get('q')
    df = load_articles()
    if df.empty:
        return jsonify({"error": "No data found. Please scrape and categorize first."}), 404

    if query:
        filtered_df = df[df['Title'].str.contains(query, case=False, na=False)]
        return jsonify(filtered_df.to_dict(orient='records'))
    else:
        return jsonify({'error': 'Query parameter is missing'}), 400

# Main function that runs everything
if __name__ == '__main__':
    if not os.path.exists(CSV_FILE):
        print("Scraping BBC News articles...")
        scrape_bbc_news()
        print("Categorizing articles...")
        categorize_articles()
    else:
        print(f"CSV file already exists at {CSV_FILE}. Skipping scraping and categorization.")

    print("Starting Flask server...")
    app.run(debug=True)
