from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def setup_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--start-maximized")
    return webdriver.Chrome(
        options=options, service=Service(ChromeDriverManager().install())
    )


DRIVER = setup_chrome_driver()
actions = ActionChains(DRIVER)

# get game title, platform, release date, summary ranked by user score, then ranked by metascore, and then do a full outer merge?
def extract():
    games = DRIVER.find_elements(By.XPATH, ".//*[@class='title']")
    game_names = [
        g.text for g in games if g.text
    ]  # conditionally excludes blank strings, potentially due to "title" class being elsewhere on page
    print(game_names)
    # print(g_name.split(".", maxsplit=1)[-1])


DRIVER.get(
    "https://www.metacritic.com/browse/games/score/userscore/all/all/filtered?page=0"
)
extract()

# def main():
#     DRIVER.get("https://au.indeed.com/")
#     DRIVER.close()


# if __name__ == "__main__":
#     main()
