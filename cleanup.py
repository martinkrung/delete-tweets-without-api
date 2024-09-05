from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import pickle
import random
import os

def get_tweet_id_from_url(url):
    match = re.search(r'/status/(\d+)', url)
    if match:
        return match.group(1)
    return None

def load_cookies(driver, cookie_file):
    with open(cookie_file, 'rb') as f:
        cookies = pickle.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)

def save_cookies(driver, cookie_file):
    cookies = driver.get_cookies()
    with open(cookie_file, "wb") as f:
        pickle.dump(cookies, f)

def login_and_save_cookies(cookie_file):
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=selenium")
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://x.com/login")
        input("Please log in manually and press Enter when done...")
        save_cookies(driver, cookie_file)
        print("Cookies saved successfully.")
    finally:
        driver.quit()

def delete_tweet_with_selenium(url, cookie_file):
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=selenium")
    driver = webdriver.Chrome(options=options)
    
    try:
        # First, navigate to Twitter's homepage
        driver.get("https://x.com")
        
        # Load the cookies
        load_cookies(driver, cookie_file)
        
        # Refresh the page to apply cookies
        driver.refresh()
        
        # Now navigate to the tweet URL
        driver.get(url)
        
        # Wait for the page to load and the delete button to be clickable
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='More']"))
        )
        delete_button.click()
        
        # Wait for the delete option in the dropdown menu and click it
        delete_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Delete']"))
        )
        delete_option.click()
        
        # Confirm deletion
        confirm_delete = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Delete']"))
        )
        confirm_delete.click()
        
        print("Tweet deleted successfully")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Close the browser
        time.sleep(2)
        driver.quit()

def natural_sleep():
    """
    Sleep for a random duration between 3 and 13 seconds, including subseconds.
    The sleep duration is generated to look more natural and less uniform.
    """
    # Generate a base sleep time between 3 and 13 seconds
    base_sleep = random.uniform(3, 13)
    
    # Add some variability to make it look more natural
    variability = random.gauss(0, 0.5)  # Gaussian distribution with mean 0 and std dev 0.5
    
    # Ensure the final sleep time stays within the 3-13 second range
    sleep_time = max(3, min(13, base_sleep + variability))
    
    # Round to 2 decimal places for a natural look
    sleep_time = round(sleep_time, 2)
    
    print(f"Sleeping for {sleep_time} seconds...")
    time.sleep(sleep_time)

# Usage example:
if __name__ == "__main__":
    cookie_file = "twitter_cookies.pkl"
    
    if not os.path.exists(cookie_file):
        print("Cookie file not found. Logging in and saving cookies...")
        login_and_save_cookies(cookie_file)
    else:
        print("Cookie file found. Using saved cookies.")
    
    username = "martinkrung"
    
    url = "https://x.com/{username}/status/1234567890"
    tweet_id = get_tweet_id_from_url(url)
    if tweet_id:
        print(f"Tweet ID: {tweet_id}")
        delete_tweet_with_selenium(url, cookie_file)
    else:
        print("Could not extract tweet ID from URL")

# Note: Make sure to run login_and_save_cookies() once to save your login session.
# After that, you can comment it out and use the saved cookies for future runs.
