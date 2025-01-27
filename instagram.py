import time
import logging
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# To keep track of profile count for file naming
profile_counter = 1

def setup_driver():
    """Sets up the Chrome WebDriver with Developer Tools enabled."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    chrome_options.add_argument("--auto-open-devtools-for-tabs")  # Automatically open Developer Tools

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return driver
    except WebDriverException as e:
        logging.error(f"Failed to set up Chrome driver: {e}")
        return None


def login_instagram(driver, username, password):
    """Logs in to Instagram."""
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "username")))

        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        WebDriverWait(driver, 15).until(EC.url_contains("instagram.com"))

        handle_popups(driver)
        logging.info("Login successful.")
        return True
    except TimeoutException:
        logging.error("Timeout while trying to log in.")
    except Exception as e:
        logging.error(f"Error during login: {e}")
    return False


def handle_popups(driver):
    """Handles common Instagram popups."""
    popups = [
        ("//button[contains(text(), 'Save Info')]", "Save login info prompt"),
        ("//button[contains(text(), 'Not Now')]", "Notifications prompt"),
    ]

    for xpath, popup_name in popups:
        try:
            button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            button.click()
            logging.info(f"Handled {popup_name}")
        except Exception:
            logging.warning(f"{popup_name} not displayed or couldn't be handled.")
def scrape_instagram_user(driver, username):
    """Opens Instagram profile, extracts specific span texts, and saves them as a JSON file."""
    logging.info(f"Opening profile for user: {username}")
    try:
        # Open the Instagram profile
        driver.get(f"https://www.instagram.com/{username}")

        # Wait until the profile page is fully loaded
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//section/main/div/header"))
        )
        logging.info("Profile page loaded successfully.")

        # Wait for additional elements to load
        time.sleep(5)  # Adjust the delay if necessary

        # JavaScript code to extract specific spans
        js_code = """
        const spans = document.querySelectorAll('span');
        const uniqueSpans = new Set();
        spans.forEach(span => {
            const text = span.textContent.trim();
            if (text !== "") {
                uniqueSpans.add(text);
            }
        });
        const uniqueSpansArray = Array.from(uniqueSpans);
        const targetIndices = [2, 3, 5, 7, 9, 10, 11];
        const extractedSpans = targetIndices
            .map(index => uniqueSpansArray[index - 1])
            .filter(text => text !== undefined);
        JSON.stringify(extractedSpans);
        """
        # Execute the JavaScript in the browser and capture the result
        result = driver.execute_cdp_cmd("Runtime.evaluate", {"expression": js_code})
        extracted_data = json.loads(result['result']['value'])

        # Save the extracted data to a JSON file
        profile_filename = f"profile_{username}.json"
        with open(profile_filename, "w", encoding="utf-8") as file:
            json.dump(extracted_data, file, indent=4)
        logging.info(f"Data saved to {profile_filename}")

    except TimeoutException:
        logging.error(f"Timeout while loading profile for {username}.")
    except Exception as e:
        logging.error(f"Error while opening profile for {username}: {e}")



def main():
    driver = setup_driver()
    if not driver:
        logging.error("Failed to initialize driver. Exiting.")
        return

    try:
        insta_username = input("Enter Instagram username: ")
        insta_password = input("Enter Instagram password: ")

        if login_instagram(driver, insta_username, insta_password):
            while True:
                username_to_scrape = input("Enter Instagram username to scrape (or type 'exit' to quit): ")
                if username_to_scrape.lower() == "exit":
                    break
                scrape_instagram_user(driver, username_to_scrape)
        else:
            logging.error("Login failed. Please check your credentials.")
    except KeyboardInterrupt:
        logging.info("Script interrupted by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        if driver:
            driver.quit()
            logging.info("Driver closed.")


if __name__ == "__main__":
    main()
