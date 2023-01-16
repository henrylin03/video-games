from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import lxml
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
    # extract all rows from table element, but ignore the table rows (<tr>) that are class="spacer", which are empty
    games = DRIVER.find_elements(By.XPATH, ".//tr[not(@class='spacer')]")
    # create list of lists of scraped attributes for each row
    games_attribs_list = []
    for g in games:
        # set maxsplit=5 as there are 6 attributes (5 "slices") in each list
        game_attribs = g.text.split("\n", maxsplit=5)
        # remove 2nd elem which is the ranking
        del game_attribs[1]
        games_attribs_list.append(game_attribs)

    print(games_attribs_list[0])
    # next step is convert to a dataframe as a list of list!


DRIVER.get(
    "https://www.metacritic.com/browse/games/score/userscore/all/all/filtered?page=0"
)
extract()

# def main():
#     DRIVER.get("https://au.indeed.com/")
#     DRIVER.close()


# if __name__ == "__main__":
#     main()
