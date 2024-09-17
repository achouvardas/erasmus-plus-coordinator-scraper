# Coordinator Data Scraper

This project contains a Python script that use Selenium, BeautifulSoup, and Pandas to extract coordinator information from Erasmus+ project URLs. The extracted data is processed and saved into an Excel file for easy access.

## Features

- **Web Scraping**: Automatically opens a URL using a headless Chrome browser and extracts coordinator information from specific Erasmus+ project pages.
- **Data Extraction**: Collects details such as coordinator name, address, city, country, type, website, and phone number.
- **Excel Export**: Saves the extracted data to an Excel file.

## Requirements

Make sure the following Python packages are installed before running the script:

- `selenium`: Web automation tool for navigating and interacting with web pages.
- `webdriver-manager`: Automatically manages and installs the appropriate browser drivers.
- `beautifulsoup4`: A Python library used for parsing HTML and extracting data from it.
- `pandas`: A powerful data manipulation library for working with data structures and writing data to Excel.
- `openpyxl`: Required by `pandas` to write data to Excel files.
