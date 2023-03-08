import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
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
            attribs_dict[s] += attribs_on_page

    DRIVER.close()
    return attribs_dict


def generate_dfs(attribs_dict):
    dfs = {}
    for k, v in attribs_dict.items():
        dfs[k] = pd.DataFrame(
            v,
            columns=[
                f"{k}_score",
                f"{k}_rank",
                "name",
                "platform",
                "release_date",
                "summary",
            ],
        )
    return dfs


def output_csvs(dfs_dict):
    for k, v in dfs_dict.items():
        output_path = os.path.join("./input", f"{k}.csv")
        v.to_csv(output_path, index=False)
    return


if __name__ == "__main__":
    dfs = generate_dfs(extract())
    output_csvs(dfs)
