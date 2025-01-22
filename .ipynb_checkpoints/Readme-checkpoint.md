Twitter Trends Scraper
This project scrapes the top 5 trending topics on Twitter and displays them on a webpage using Flask. The data is stored in MongoDB, and the app supports optional proxy integration for anonymity.

Features
Scrapes Twitter's top 5 trending topics.
Displays results on a user-friendly webpage.
Stores trends in a MongoDB database.
Proxy-ready (configurable via .env).
Prerequisites
Python 3.8+ installed on your system.
MongoDB server installed and running locally or on a cloud service.
Chrome browser installed.
ChromeDriver installed (automated using webdriver_manager).
Setup Instructions
Clone the Repository:

```bash
git clone https://github.com/Nerd-coderZero/twitter-trends-scraper.git
cd twitter-trends-scraper
```
Create a Virtual Environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
## Install Dependencies:

```bash
pip install -r requirements.txt
```
Set Up the .env File: Create a file(if not found in repository) named .env in the project root with the following content:

# Twitter credentials (replace with your own)
TWITTER_EMAIL=your_email@example.com
TWITTER_USERNAME=your_username
TWITTER_PASSWORD=your_password
PROXY_URL=http://Username:Password@open.proxymesh.com:31280
MONGO_URI=MongoDB_URI(AFTER SETTING UP CONNECTION IN MONGODB COMPASS)

[ # Optional proxy (leave blank if not using) Since proxymesh proxy is not working for my environment I left it out but provided the code
PROXY_URL=http://USERNAME:PASSWORD@open.proxymesh.com:31280 ]

## Run the Flask App: Start the MongoDB server locally and run the app:

```bash
python app.py
```
## Access the App: Open your browser and visit:

http://127.0.0.1:5000

## Future Improvements
Add support for rotating proxies using premium services.
Optimize for faster scraping and reduced API detection.

## Security Note
Ensure that your .env file is never shared publicly to protect your credentials and sensitive data.