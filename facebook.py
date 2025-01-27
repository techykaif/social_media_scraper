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

def setup_driver():
    """Sets up the Chrome WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return driver
    except WebDriverException as e:
        logging.error(f"Failed to set up Chrome driver: {e}")
        return None

def login_facebook(driver, username, password):
    """Logs in to Facebook."""
    try:
        driver.get("https://www.facebook.com/")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "email")))

        driver.find_element(By.ID, "email").send_keys(username)
        driver.find_element(By.ID, "pass").send_keys(password)
        driver.find_element(By.ID, "pass").send_keys(Keys.RETURN)

        WebDriverWait(driver, 15).until(EC.url_contains("facebook.com"))
        logging.info("Login successful.")
        return True
    except TimeoutException:
        logging.error("Timeout while trying to log in.")
    except Exception as e:
        logging.error(f"Error during login: {e}")
    return False

def scrape_facebook_profile(driver, profile_url):
    """Scrapes basic profile data from a Facebook profile and saves it to a JSON file."""
    logging.info(f"Opening Facebook profile: {profile_url}")
    profile_data = {}

    try:
        # Open the profile URL
        driver.get(profile_url)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logging.info("Profile page loaded successfully.")

        # Extract profile name
        try:
            profile_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div/div/div/span/h1").text
            logging.info(f"Profile Name: {profile_name}")
            profile_data["Profile Name"] = profile_name
        except Exception as e:
            error_message = f"Could not find profile name: {e}"
            logging.warning(error_message)
            profile_data["Profile Name"] = error_message

        # Click on the "About" section
        try:
            about_link = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'about')]")
            ))
            driver.execute_script("arguments[0].click();", about_link)  # Click using JavaScript
            logging.info("Navigated to the About section.")
            time.sleep(3)  # Allow time for the About page to load

            # Extract Overview details
            try:
                location = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[4]/div/div/div[2]/div/span").text
                logging.info(f"Location: {location}")
                profile_data["Location"] = location
            except Exception:
                error_message = "No places to show: "
                logging.warning(error_message)
                profile_data["Location"] = error_message

            try:
                relationship_status = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[5]/div/div/div[2]/span").text
                logging.info(f"Relationship Status: {relationship_status}")
                profile_data["Relationship Status"] = relationship_status
            except Exception:
                error_message = f"Information not available:"
                logging.warning(error_message)
                profile_data["Relationship Status"] = error_message

            try:
                contact_info = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[1]/div/div[2]/div/div/div[2]/span").text
                logging.info(f"Contact Info: {contact_info}")
                profile_data["Contact Info"] = contact_info
            except Exception:
                error_message = "No contact info available:"
                logging.warning(error_message)
                profile_data["Contact Info"] = error_message

            try:
                website_social_links = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/ul/li/div/div/div[1]/span/a").text
                logging.info(f"Website and Social Links: {website_social_links}")
                profile_data["Website and Social Links"] = website_social_links
            except Exception:
                error_message = "No website and social links available:"
                logging.warning(error_message)
                profile_data["Website and Social Links"] = error_message

            try:
                basic_info = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[3]/div/div[2]/div/div/div[2]/div/div/div/div/div[1]/span").text
                logging.info("Basic Info: {basic_info}")
                profile_data["Basic Info"] = basic_info
            except Exception:
                error_message = f"No basic info available:"
                logging.warning(error_message)
                profile_data["Basic Info"] = error_message

        except Exception as e:
            error_message = f"Could not click or navigate to the About section: {e}"
            logging.warning(error_message)
            profile_data["About Section"] = error_message

        # Save profile data to JSON
        file_name = f"{profile_data.get('Profile Name', 'profile')}.json"
        with open(file_name, "w", encoding="utf-8") as json_file:
            json.dump(profile_data, json_file, ensure_ascii=False, indent=4)
        logging.info(f"Profile data saved to {file_name}")

    except TimeoutException:
        logging.error(f"Timeout while loading profile: {profile_url}")
    except Exception as e:
        logging.error(f"Error while scraping profile: {e}")


def main():
    driver = setup_driver()
    if not driver:
        logging.error("Failed to initialize driver. Exiting.")
        return

    try:
        fb_username = input("Enter your Facebook email/phone: ")
        fb_password = input("Enter your Facebook password: ")

        if login_facebook(driver, fb_username, fb_password):
            while True:
                profile_url = input("Enter Facebook profile URL to scrape (or type 'exit' to quit): ")
                if profile_url.lower() == "exit":
                    break
                scrape_facebook_profile(driver, profile_url)
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
