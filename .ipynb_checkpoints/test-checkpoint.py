import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_working_proxy():
    # Get free proxy list
    response = requests.get('https://free-proxy-list.net/')
    soup = BeautifulSoup(response.text, 'html.parser')
    proxies = []
    
    # Get proxy table rows
    for row in soup.find('table').find_all('tr')[1:]:
        tds = row.find_all('td')
        if tds[6].text == 'yes':  # Check if HTTPS
            proxy = f"{tds[0].text}:{tds[1].text}"
            proxies.append(proxy)
    
    # Test each proxy
    for proxy in proxies[:5]:  # Test first 5 only
        try:
            print(f"Testing proxy: {proxy}")
            options = webdriver.ChromeOptions()
            options.add_argument(f'--proxy-server=https://{proxy}')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            driver.set_page_load_timeout(10)
            driver.get("https://www.google.com")
            print(f"Proxy {proxy} works!")
            driver.quit()
            return proxy
        except:
            print(f"Proxy {proxy} failed")
            if 'driver' in locals():
                driver.quit()
    return None

if __name__ == "__main__":
    working_proxy = get_working_proxy()
    print(f"Working proxy found: {working_proxy}")