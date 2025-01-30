import json
import requests
import markdown
from bs4 import BeautifulSoup
import sys
import getopt
import re
import jinja2
from datetime import datetime
import os
from pyhtml2pdf import converter
from selenium import webdriver  # Import Selenium
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# ... (rest of your imports and global variables)

def create_pdf_from_html(html_report_file_path, output_file_path):
    """Convert HTML content to PDF using Selenium and headless Chrome."""

    chrome_options = Options()  # Initialize Chrome Options
    chrome_options.add_argument("--headless")  # Run in headless mode (essential)
    chrome_options.add_argument("--no-sandbox")  # Often needed in Docker
    chrome_options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems
    chrome_options.add_argument("--disable-gpu") # Disable GPU acceleration

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) # Use webdriver_manager
        driver.get(f'file:///{html_report_file_path}')  # Open the HTML file in Chrome
        driver.print_to_pdf({
            "printBackground": True,
            "displayHeaderFooter": False,
            "marginTop": 0,
            "marginLeft": 0,
            "marginRight": 0
        })
        with open(output_file_path, "wb") as f:
            f.write(driver.print_to_pdf({}))  # Save the PDF
    except Exception as e:
        print(f"Error converting to PDF: {e}")
    finally:
        if 'driver' in locals():  # Check if the driver was initialized
            driver.quit()  # Close the browser instance

# ... (rest of your functions: md2html, generate_html_report, upload_file_to_slack, generate_and_send_report)

if __name__ == "__main__":
    generate_and_send_report()
