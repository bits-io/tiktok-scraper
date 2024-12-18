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
X_API_KEY = "secret-key-123"

# Dependency function to validate the token
def validate_token(x_api_key: str = Header(None)):
    if x_api_key is None or x_api_key != X_API_KEY:
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
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

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

@router.get('/content/',dependencies=[Depends(validate_token)])
async def get_content(username: str, content_id: str):
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
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

        # Set up the WebDriver service
        service = Service(webdriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Fetch the TikTok page
        url = f'https://www.tiktok.com/@{username}/video/{content_id}'
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

        print(soup.prettify())

        # Close the WebDriver
        driver.quit()

        # Find the required data with conditional assignments
        like_count = soup.find(attrs={"data-e2e": "like-count"}).get_text() if soup.find(attrs={"data-e2e": "like-count"}) else ""
        comment_count = soup.find(attrs={"data-e2e": "comment-count"}).get_text() if soup.find(attrs={"data-e2e": "comment-count"}) else ""
        undefined_count = soup.find(attrs={"data-e2e": "undefined-count"}).get_text() if soup.find(attrs={"data-e2e": "undefined-count"}) else ""
        share_count = soup.find(attrs={"data-e2e": "share-count"}).get_text() if soup.find(attrs={"data-e2e": "share-count"}) else ""
        browse_video_desc = soup.find(attrs={"data-e2e": "browse-video-desc"}).get_text() if soup.find(attrs={"data-e2e": "browse-video-desc"}) else ""
        browse_video = soup.find('div', class_='tiktok-web-player no-controls').find('video')['src'] if soup.find('div', class_='tiktok-web-player no-controls').find('video') else ""
        created_at = soup.find('span', {'data-e2e': 'browser-nickname'}).find_all('span')[-1].text.strip() if soup.find('span', {'data-e2e': 'browser-nickname'}) else ""
        browse_music = soup.find(attrs={"data-e2e": "browse-music"}).get_text() if soup.find(attrs={"data-e2e": "browse-music"}) else ""

        # Construct the response
        response = {
            "content_id": content_id,
            "like_count": like_count,
            "comment_count": comment_count,
            "undefined_count": undefined_count,
            "share_count": share_count,
            "browse_video_desc": browse_video_desc,
            "browse_video": browse_video,
            "browse_music": browse_music,
            "created_at": created_at
        }

        return response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def init_driver(webdriver_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("start-maximized")  # Open browser in maximized mode
    chrome_options.add_argument("disable-infobars")  # Disable infobars
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation-controlled
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def fetch_page_source(driver, url):
    driver.get(url)
    time.sleep(5)  # Give some time for the page to load
    for _ in range(20):  # Adjust the range as needed to scroll more times
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(1)  # Adjust the sleep time as needed
    return driver.page_source

@router.get("/user-content/", dependencies=[Depends(validate_token)])
async def fetch_tiktok_data(username: str):
    try:
        driver = init_driver(webdriver_path)
        url = f'https://www.tiktok.com/@{username}'
        html = fetch_page_source(driver, url)
        soup = BeautifulSoup(html, 'html.parser')

        post_list = soup.find(attrs={"data-e2e": "user-post-item-list"})
        post_count = len(post_list.find_all(attrs={"data-e2e": "user-post-item"})) if post_list else 0

        content_list = []
        if post_list:
            for post_item in post_list.find_all(attrs={"data-e2e": "user-post-item"}):
                a_tag = post_item.find('a', href=True)
                img_tag = post_item.find('img', src=True)

                if a_tag and img_tag:
                    post_url = a_tag['href']
                    post_html = fetch_page_source(driver, post_url)
                    post_soup = BeautifulSoup(post_html, 'html.parser')

                    like_count = post_soup.find(attrs={"data-e2e": "like-count"})
                    like_count = like_count.get_text() if like_count else ""

                    comment_count = post_soup.find(attrs={"data-e2e": "comment-count"})
                    comment_count = comment_count.get_text() if comment_count else ""

                    undefined_count = post_soup.find(attrs={"data-e2e": "undefined-count"})
                    undefined_count = undefined_count.get_text() if undefined_count else ""

                    share_count = post_soup.find(attrs={"data-e2e": "share-count"})
                    share_count = share_count.get_text() if share_count else ""

                    browse_video_desc = post_soup.find(attrs={"data-e2e": "browse-video-desc"})
                    browse_video_desc = browse_video_desc.get_text() if browse_video_desc else ""

                    browse_video = post_soup.find('div', class_='tiktok-web-player no-controls')
                    browse_video = browse_video.find('video')['src'] if browse_video and browse_video.find('video') else ""

                    created_at = post_soup.find('span', {'data-e2e': 'browser-nickname'})
                    created_at = created_at.find_all('span')[-1].text.strip() if created_at and created_at.find_all('span') else ""

                    browse_music = post_soup.find(attrs={"data-e2e": "browse-music"})
                    browse_music = browse_music.get_text() if browse_music else ""

                    content_list.append({
                        'link': a_tag['href'],
                        'thumbnail': img_tag['src'],
                        "like_count": like_count,
                        "comment_count": comment_count,
                        "undefined_count": undefined_count,
                        "share_count": share_count,
                        "browse_video_desc": browse_video_desc,
                        "browse_video": browse_video,
                        "browse_music": browse_music,
                        "created_at": created_at
                    })

        driver.quit()

        response = {
            "post_count": post_count,
            "content_list": content_list
        }

        return response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))