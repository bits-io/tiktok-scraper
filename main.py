from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = FastAPI()

# Path to your Chrome WebDriver executable
webdriver_path = 'C:\\chromedriver-win64\\chromedriver.exe'  # Update this with the correct path

@app.get("/")
async def root():
    return {
        "status": True,
        "message": "This scrape app"
    }

@app.post("/user-info/")
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
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Disable automation-controlled
        chrome_options.add_argument(
            f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        # Set up the WebDriver service
        service = Service(webdriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Fetch the TikTok page
        url = f'https://www.tiktok.com/@{username}'
        driver.get(url)

        # Wait for the page to load completely (optional)
        driver.implicitly_wait(1)  # Wait for 10 seconds

        # Scroll down the page to ensure all elements are loaded
        for _ in range(20):  # Adjust the range as needed to scroll more times
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(1)  # Adjust the sleep time as needed

        # Get the page source and parse it with BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Close the WebDriver
        driver.quit()

        # Find the required data
        username = soup.find(attrs={"data-e2e": "user-title"}).get_text()
        name = soup.find(attrs={"data-e2e": "user-subtitle"}).get_text()
        following_count = soup.find(attrs={"data-e2e": "following-count"}).get_text()
        followers_count = soup.find(attrs={"data-e2e": "followers-count"}).get_text()
        likes_count = soup.find(attrs={"data-e2e": "likes-count"}).get_text()
        bio = soup.find(attrs={"data-e2e": "user-bio"}).get_text()
        user_link = soup.find(attrs={"data-e2e": "user-link"}).get_text()

        user_avatar = soup.find(attrs={"data-e2e": "user-avatar"})
        img_tag = user_avatar.find('img')

        post_list = soup.find(attrs={"data-e2e": "user-post-item-list"})

        print(soup.prettify())

        # Construct the response
        response = {
            "username": username,
            "name": name,
            "following_count": following_count,
            "followers_count": followers_count,
            "likes_count": likes_count,
            "bio": bio,
            "user_link": user_link,
            "post_count": len(post_list.find_all(attrs={"data-e2e": "user-post-item"})),
            "user_avatar": img_tag['src']
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))