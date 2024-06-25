from fastapi import APIRouter, HTTPException, Header, Depends
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import logging
from app.core.config import settings

# Path to your Chrome WebDriver executable
webdriver_path = settings.WEBDRIVER_DIR

logging.basicConfig(level=logging.INFO)

router = APIRouter()

# Define the valid token
VALID_TOKEN = "your_hardcoded_token_here"

# Dependency function to validate the token
def validate_token(x_token_key: str = Header(...)):
    if x_token_key != VALID_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing x-token-key header")

@router.get("/user-info/", dependencies=[Depends(validate_token)])
async def fetch_tiktok_data(username: str):
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("start-maximized")  # Open browser in maximized mode
        chrome_options.add_argument("disable-infobars")  # Disable infobars
        chrome_options.add_argument("--disable-extensions")  # Disable extensions
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation-controlled
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        # Set up the WebDriver service
        service = Service(webdriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Fetch the TikTok page
        url = f'https://www.tiktok.com/@{username}'
        driver.get(url)

        # Wait for the page to load completely
        time.sleep(5)  # Give some time for the page to load

        # Scroll down the page to ensure all elements are loaded
        for _ in range(20):  # Adjust the range as needed to scroll more times
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(1)  # Adjust the sleep time as needed

        # Get the page source and parse it with BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Close the WebDriver
        driver.quit()

        # Find the required data with conditional assignments
        username = soup.find(attrs={"data-e2e": "user-title"}).get_text() if soup.find(attrs={"data-e2e": "user-title"}) else ""
        name = soup.find(attrs={"data-e2e": "user-subtitle"}).get_text() if soup.find(attrs={"data-e2e": "user-subtitle"}) else ""
        following_count = soup.find(attrs={"data-e2e": "following-count"}).get_text() if soup.find(attrs={"data-e2e": "following-count"}) else ""
        followers_count = soup.find(attrs={"data-e2e": "followers-count"}).get_text() if soup.find(attrs={"data-e2e": "followers-count"}) else ""
        likes_count = soup.find(attrs={"data-e2e": "likes-count"}).get_text() if soup.find(attrs={"data-e2e": "likes-count"}) else ""
        bio = soup.find(attrs={"data-e2e": "user-bio"}).get_text() if soup.find(attrs={"data-e2e": "user-bio"}) else ""
        user_link = soup.find(attrs={"data-e2e": "user-link"}).get_text() if soup.find(attrs={"data-e2e": "user-link"}) else ""

        user_avatar = soup.find(attrs={"data-e2e": "user-avatar"})
        img_tag = user_avatar.find('img') if user_avatar else None

        post_list = soup.find(attrs={"data-e2e": "user-post-item-list"})

        post_count = len(post_list.find_all(attrs={"data-e2e": "user-post-item"})) if post_list else 0

        # Construct the response
        response = {
            "username": username,
            "name": name,
            "following_count": following_count,
            "followers_count": followers_count,
            "likes_count": likes_count,
            "bio": bio,
            "user_link": user_link,
            "post_count": post_count,
            "user_avatar": img_tag['src'] if img_tag else None
        }

        return response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
