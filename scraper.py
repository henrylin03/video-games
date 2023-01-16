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

# as there is no list of games with attributes, across platforms, need to scrape all data by user-score, then meta-score
def extract():
    # dictionary to hold the two different types of scores (key) and their games' attributes (value)
    attribs_dict = {}
    for s in ["user", "meta"]:
        url = f"https://www.metacritic.com/browse/games/score/{s}score/all/all"
        DRIVER.get(url)

        # find count of last page of content - for metacritic.com, this number does not change as you click through the pages
        last_page = DRIVER.find_element(
            By.XPATH, ".//*[@class='page last_page']/*[@class='page_num']"
        ).text

        attribs_dict[s] = []
        for p in range(0, int(last_page)):
            # skip reloading first page
            if p:
                DRIVER.get(f"{url}/filtered?page={p}")

            # extract all rows from table element, but ignore the table rows (<tr>) that are class="spacer", which are empty
            games = DRIVER.find_elements(By.XPATH, ".//tr[not(@class='spacer')]")

            # create list of lists of scraped attributes for each row
            # set maxsplit=5 as there are 6 attributes (5 "slices") in each list
            attribs_on_page = [g.text.split("\n", maxsplit=5) for g in games]
            attribs_dict[s].append(attribs_on_page)
    return attribs_dict


# DRIVER.get(
#     "https://www.metacritic.com/browse/games/score/userscore/all/all/filtered?page=0"
# )
# DRIVER.get(
#     "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0"
# )
extract()

# def main():
#     DRIVER.get("https://au.indeed.com/")
#     DRIVER.close()


# if __name__ == "__main__":
#     main()
