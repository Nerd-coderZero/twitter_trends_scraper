from flask import Flask, render_template, jsonify
from twitter_scraper import TwitterScraper
from datetime import datetime
import pymongo
import uuid
from bson import ObjectId
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Flask app
app = Flask(__name__)

# Setup MongoDB connection
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["twitter_trends"]
    collection = db["trends"]
    client.server_info()  # Raise an exception if the connection fails
    logging.info("MongoDB connection successful")
except Exception as e:
    logging.error(f"MongoDB connection failed: {e}")
    raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    try:
        # Fetch proxy credentials from environment variables
        proxy_url = os.getenv('PROXY_URL')  # Example: "http://USERNAME:PASSWORD@open.proxymesh.com:31280"
        
        # Initialize the scraper with or without a proxy
        if proxy_url:
            logging.info("Using proxy for scraping")
            scraper = TwitterScraper(proxy=proxy_url)
        else:
            logging.info("No proxy configured; using direct connection")
            scraper = TwitterScraper()
        
        # Scrape trends
        result = scraper.scrape()
        trends = result["trends"]
        timestamp = result["timestamp"]
        
        # Create a unique MongoDB document
        document = {
            "unique_id": str(uuid.uuid4()),
            "nameoftrend1": trends[0],
            "nameoftrend2": trends[1],
            "nameoftrend3": trends[2],
            "nameoftrend4": trends[3],
            "nameoftrend5": trends[4],
            "datetime": timestamp,
            "ip_address": proxy_url or "Direct connection"
        }
        
        # Insert the document into MongoDB
        insert_result = collection.insert_one(document)
        
        # Retrieve the inserted document
        stored_document = collection.find_one({"_id": insert_result.inserted_id})
        stored_document['_id'] = str(stored_document['_id'])  # Convert ObjectId to string for JSON serialization
        
        # Prepare the response
        response_data = {
            "success": True,
            "data": {
                "trends": trends,
                "datetime": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "ip_address": proxy_url or "Direct connection",
                "mongodb_record": stored_document
            }
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        logging.error(f"Scraping endpoint failed: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
