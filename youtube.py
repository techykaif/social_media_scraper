import logging
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import re
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# Sanitize filename (remove special characters)
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)
# Check if URL is valid
def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# Setup Selenium WebDriver with headless mode
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for performance
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)
    return driver

# Function to extract YouTube channel data
def get_youtube_channel_data(driver, url):
    if not is_valid_url(url):
        logging.error("Invalid URL. Please check the input.")
        return

    driver.get(url)
    data = {}

    # Wait for the channel name to load
    try:
        name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page-header"]/yt-page-header-renderer/yt-page-header-view-model/div/div[1]/div/yt-dynamic-text-view-model/h1/span'))
        ).text
        data["Channel Name"] = name
        logging.info(f"Channel Name: {name}")
    except Exception as e:
        logging.error(f"Error extracting channel name: {e}")

    # Wait for the follower (subscriber) count to load
    try:
        followers = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page-header"]/yt-page-header-renderer/yt-page-header-view-model/div/div[1]/div/yt-content-metadata-view-model/div[2]/span[1]'))
        ).text
        data["Followers"] = followers
        logging.info(f"Followers: {followers}")
    except Exception as e:
        logging.error(f"Error extracting followers: {e}")

    # Wait for the 'About' section and retrieve the join date
    try:
    # Click on the 'About' tab
        about_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="page-header"]/yt-page-header-renderer/yt-page-header-view-model/div/div[1]/div/yt-description-preview-view-model/truncated-text/button/span'))
        )
        about_tab.click()  # Navigate to the 'About' tab

    # Wait for the Joined Date to be visible and extract it
        joined_date = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="additional-info-container"]/table/tbody/tr[7]/td[2]/yt-attributed-string/span'))
        ).text
        data["Joined Date"] = joined_date
        logging.info(f"Joined Date: {joined_date}")
    except Exception as e:
        logging.error(f"Error extracting join date: {e}")


    # Save data to JSON file with a sanitized name
    try:
        sanitized_name = sanitize_filename(name)
        file_path = os.path.join(os.getcwd(), f"{sanitized_name}.json")
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        logging.info(f'Channel data saved to {file_path}')
    except Exception as e:
        logging.error(f"Error saving data to JSON: {e}")

# Main function
if __name__ == "__main__":
    url = str(input("Enter the YouTube channel URL: "))
    driver = setup_driver()

    try:
        get_youtube_channel_data(driver, url)
    finally:
        driver.quit()
