from fastapi import APIRouter, HTTPException, Header, Depends
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from app.core.config import settings

# Path to your Chrome WebDriver executable
webdriver_path = settings.WEBDRIVER_DIR

logging.basicConfig(level=logging.INFO)

router = APIRouter()

# Define the valid token
X_API_KEY = "secret-key-123"

# Dependency function to validate the token
def validate_token(x_api_key: str = Header(None)):
    if x_api_key is None or x_api_key != X_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing x-token-key header")

@router.get("/youtube-comments/", dependencies=[Depends(validate_token)])
async def fetch_youtube_comments(video_url: str):
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )

        # WebDriver service
        service = Service(webdriver_path)  # Replace with the path to your chromedriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 10)

        # Navigate to the video URL
        driver.get(video_url)

        # Scroll to load comments
        for _ in range(5):  # Adjust as needed to load more comments
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(3)

        # Extract comments
        comments = []
        for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text"))):
            comments.append(comment.text)

        # Close the driver
        driver.quit()

        return {"comments": comments}

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/youtube-comments-with-excel/", dependencies=[Depends(validate_token)])
async def fetch_youtube_comments(video_url: str, reply: str = None):
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )

        # WebDriver service
        service = Service(webdriver_path)  # Replace with the path to your chromedriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 10)

        # Navigate to the video URL
        driver.get(video_url)

        # Scroll to load comments
        for _ in range(2000):  # Adjust as needed to load more comments
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(3)

        # Extract comments, usernames, and published times
        comments_data = []
        comment_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text")))
        username_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #author-text")))
        published_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#header-author #published-time-text")))

        for username, comment, published in zip(username_elements, comment_elements, published_elements):
            comments_data.append({
                "Name": username.text.strip(),
                "Comment": comment.text.strip(),
                "Published Date": published.text.strip()
            })

        # Reply to the first comment if reply text is provided
        if reply:
            reply_buttons = driver.find_elements(By.CSS_SELECTOR, "yt-formatted-string#reply-button")
            if reply_buttons:
                reply_buttons[0].click()  # Click the reply button for the first comment
                time.sleep(2)

                reply_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#contenteditable-root")))
                reply_box.send_keys(reply)  # Type the reply
                time.sleep(1)

                post_button = driver.find_element(By.CSS_SELECTOR, "yt-button-renderer#submit-button")
                post_button.click()  # Post the reply
                time.sleep(2)

        # Save comments to Excel
        df = pd.DataFrame(comments_data)
        excel_path = "youtube_comments.xlsx"  # Adjust the path as needed
        df.to_excel(excel_path, index=False)

        # Close the driver
        driver.quit()

        return {"message": "Comments fetched and saved to Excel.", "file": excel_path}

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/youtube-comments-with-excel-while/", dependencies=[Depends(validate_token)])
async def fetch_youtube_comments(video_url: str):
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )

        # WebDriver service
        service = Service(webdriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 10)

        # Navigate to the video URL
        driver.get(video_url)

        comments = set()  # Use a set to avoid duplicates
        prev_len = 0

        # Scroll and fetch comments
        while True:
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(3)

            # Extract comments
            comment_elements = driver.find_elements(By.CSS_SELECTOR, "#comment #content-text")
            for comment in comment_elements:
                comments.add(comment.text)

            # Stop if no new comments are loaded
            if len(comments) == prev_len:
                break

            prev_len = len(comments)

        # Close the driver
        driver.quit()

        # Save comments to Excel
        df = pd.DataFrame({"Comments": list(comments)})
        excel_path = "youtube_comments.xlsx"  # Path to save the file
        df.to_excel(excel_path, index=False)

        return {"message": "Comments fetched and saved to Excel.", "file": excel_path}

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))