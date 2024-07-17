from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

def extract_data_from_url(url):
    # Configure Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1200,800")  # Set window size to a standard desktop resolution
    
    # Initialize WebDriver with Chrome
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Open the URL
    driver.get(url)
    
    # Wait for 10 seconds (adjust as needed)
    time.sleep(0.5)
    
    # Get the page source after loading
    html = driver.page_source
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the specific div with coordinator information
    coordinator_div = soup.find('div', class_='card-content coordinator')
    if not coordinator_div:
        print(f"No coordinator information found in {url}")
        driver.quit()
        return None

    # Extract details from the coordinator_div
    coordinator_info = coordinator_div.find_all(['p', 'div'], recursive=False)
    
    # Close the browser tab
    driver.quit()
    
    # Convert the extracted data into a dictionary
    data = {
        'URL': url,
        'Coordinator Name': None,
        'Address': None,
        'City': None,
        'Country': None,
        'Coordinator Type': None,
        'Website': None,
        'Phone': None,

    }
    
    for item in coordinator_info:
        text = item.get_text(strip=True)
        if 'Coordinator Type:' in text:
            data['Coordinator Type'] = text.split(':')[1].strip()
        if 'Website:' in text:
            data['Website'] = item.find('a')['href']
        if 'Phone:' in text:
            data['Phone'] = text.split('Phone:')[1].strip()
        else:
            # Assuming the rest are address components
            if data['Coordinator Name'] is None:
                data['Coordinator Name'] = text
            elif data['Address'] is None:
                data['Address'] = text
            elif data['City'] is None:
                data['City'] = text
            elif data['Country'] is None:
                data['Country'] = text
    
    return data

def save_to_excel(data, filename='coordinator_info.xlsx'):
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)
    
    # Save to Excel
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

def main(urls):
    data = []
    for url in urls:
        coordinator_info = extract_data_from_url(url)
        if coordinator_info:
            data.append(coordinator_info)

    if data:
        save_to_excel(data)
    else:
        print("No data to save.")

if __name__ == "__main__":
    urls = [
        'https://erasmus-plus.ec.europa.eu/projects/search/details/2023-3-BG01-KA152-YOU-000176203',
        'https://erasmus-plus.ec.europa.eu/projects/search/details/2021-1-BG01-KA131-HED-000003440',
        'https://erasmus-plus.ec.europa.eu/projects/search/details/2022-3-BG01-KA152-YOU-000093550',
        'https://erasmus-plus.ec.europa.eu/projects/search/details/2022-1-BG01-KA210-YOU-000084531',
    ]
    main(urls)



