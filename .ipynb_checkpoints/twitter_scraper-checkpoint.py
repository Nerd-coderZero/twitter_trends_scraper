from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os
import time
import logging
from dotenv import load_dotenv
import random

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='scraper.log')

class TwitterScraper:
    def __init__(self, proxy=None):
        load_dotenv()
        self.twitter_email = os.getenv('TWITTER_EMAIL')
        self.twitter_username = os.getenv('TWITTER_USERNAME')
        self.twitter_password = os.getenv('TWITTER_PASSWORD')
        self.proxy = proxy
        
        if not all([self.twitter_email, self.twitter_username, self.twitter_password]):
            raise ValueError("Missing Twitter credentials in .env file")

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        if self.proxy:
            options.add_argument(f'--proxy-server={self.proxy}')
        
        options.add_argument('--start-maximized')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)
        return driver

    def login_to_twitter(self, driver):
        try:
            driver.get("https://x.com/i/flow/login")
            time.sleep(5)
            
            # Email step
            email_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))
            )
            email_input.send_keys(self.twitter_email)
            time.sleep(2)
            
            # Click next after email
            next_buttons = driver.find_elements(By.XPATH, "//*[text()='Next']")
            if next_buttons:
                next_buttons[0].click()
            time.sleep(3)
            
            # Username step (new)
            username_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='ocfEnterTextTextInput']"))
            )
            username_input.send_keys(self.twitter_username)
            time.sleep(2)
            
            # Click next after username
            next_buttons = driver.find_elements(By.XPATH, "//*[text()='Next']")
            if next_buttons:
                next_buttons[0].click()
            time.sleep(3)
            
            # Password step
            password_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
            )
            password_input.send_keys(self.twitter_password)
            time.sleep(2)
            
            # Final login
            login_buttons = driver.find_elements(By.XPATH, "//*[text()='Log in']")
            if login_buttons:
                login_buttons[0].click()
            time.sleep(5)
            
            return "home" in driver.current_url or "explore" in driver.current_url
            
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            return False

    def get_trending_topics(self, driver):
        try:
            driver.get("https://twitter.com/i/trends") # Direct to trends to avoid explore
            logging.info("Navigated to Trends page")
            time.sleep(5)

            trends = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='trend']"))
            )

            trend_texts = []
            for trend in trends[:5]:  # Get the top 5
                try:
                    trend_text = trend.find_element(By.CSS_SELECTOR, "span").text # Get the span text
                    trend_texts.append(trend_text)
                except NoSuchElementException:
                    logging.warning("Trend text element not found. Skipping.")
                    continue  # Skip to the next trend

            while len(trend_texts) < 5:
                trend_texts.append("No trend found")

            return trend_texts

        except TimeoutException:
            logging.error("Timeout waiting for trends to load.")
            return ["Timeout fetching trends"] * 5
        except Exception as e:
            logging.error(f"Error fetching trends: {e}")
            logging.error(traceback.format_exc())
            return ["Error fetching trends"] * 5

    def scrape(self):
        driver = None
        try:
            driver = self.setup_driver()
            if not self.login_to_twitter(driver):
                raise Exception("Failed to login to Twitter")

            trends = self.get_trending_topics(driver)
            return {
                "trends": trends,
                "timestamp": datetime.now()
            }

        except Exception as e:
            logging.error(f"Scraping failed: {e}")
            raise
        finally:
            if driver:
                input("Press Enter to close the browser...")
                driver.quit()

def main():
    try:
        scraper = TwitterScraper()
        result = scraper.scrape()
        print("Successfully scraped trends:", result)
    except Exception as e:
        print(f"Failed to scrape trends: {e}")
        print("Check scraper.log for more details")

if __name__ == "__main__":
    main()