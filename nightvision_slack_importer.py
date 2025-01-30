import json
import requests
import markdown
from bs4 import BeautifulSoup
import sys
import getopt
import re
import jinja2
from datetime import datetime, timezone  # Ensure correct imports
import os
from pyhtml2pdf import converter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def create_pdf_from_html(html_report_file_path, output_file_path):
    """Convert HTML content to PDF using Selenium and headless Chrome."""

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    try:
        # Initialize the WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Open the HTML file in Chrome
        driver.get(f'file:///{html_report_file_path}')

        # Wait for the page to load (you can adjust the sleep if necessary)
        driver.implicitly_wait(10)

        # Use print_to_pdf method to generate the PDF (adjust if necessary)
        pdf_bytes = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True,
            "displayHeaderFooter": False,
            "marginTop": 0,
            "marginBottom": 0,
            "marginLeft": 0,
            "marginRight": 0
        })

        # Write PDF to output file
        with open(output_file_path, "wb") as f:
            f.write(bytes.fromhex(pdf_bytes['data']))

    except Exception as e:
        print(f"Error converting to PDF: {e}")

    finally:
        # Ensure the browser instance is closed
        if 'driver' in locals():
            driver.quit()

# (Rest of your code remains unchanged)
if __name__ == "__main__":
    generate_and_send_report()
