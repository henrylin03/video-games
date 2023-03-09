import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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


def open_page(url, webdriver_name):
    webdriver_name.get(url)
    return


def scrape(platform):
    DRIVER = setup_chrome_driver()

    # scrape all games on all platforms by metascore, expanding and extracting user score in each ticket
    url_platform = f"https://www.metacritic.com/browse/games/release-date/available/{platform}/name?view=condensed"
    open_page(url_platform, DRIVER)
    last_page = DRIVER.find_element(
        By.XPATH, ".//*[@class='page last_page']/*[@class='page_num']"
    ).text

    games_by_platform_list_of_dicts = []
    for page_no in range(int(last_page)):
        if page_no:  # page numbers on metacritic are zero-indexed
            open_page(f"{url_platform}&page={page_no}", DRIVER)

        games_elems_on_page = DRIVER.find_elements(
            By.XPATH, ".//tr[@class='expand_collapse']"
        )

        expand_buttons = DRIVER.find_elements(By.XPATH, ".//button[text()='Expand']")
        [button.click() for button in expand_buttons]

        # setting up bsd4
        page_html = DRIVER.page_source
        soup = BeautifulSoup(page_html, "html.parser")

        for g in games_elems_on_page:
            name = g.find_element(By.XPATH, ".//*[@class='title']/h3").text
            platform = g.find_element(
                By.XPATH, ".//*[@class='platform']/*[@class='data']"
            ).text
            release_date = g.find_element(
                By.XPATH, ".//*[@class='details']/span[not(@class)]"
            ).text
            summary = g.find_element(By.XPATH, ".//*[@class='summary']/p").text
            metascore = g.find_element(
                By.XPATH, ".//*[@class='score']/*[@class='metascore_anchor']/div"
            ).text
            userscore = g.find_element(
                By.XPATH,
                ".//*[@class='score title']/*[@class='metascore_anchor']/div",
            ).text  # a bit confusing for Metacritic to call its user score elem's class "metascore_anchor" as well!

            games_attributes_dict = {
                "name": name,
                "platform": platform,
                "release_date": release_date,
                "summary": summary,
                "metascore": metascore,
                "userscore": userscore,
            }
            games_by_platform_list_of_dicts.append(games_attributes_dict)
    return games_by_platform_list_of_dicts


scrape("ios")

# def generate_df():
#     PLATFORMS = [
#         "ps",
#         "ps2",
#         "ps3",
#         "ps4",
#         "ps5",
#         "psp",
#         "xbox",
#         "xbox360",
#         "xboxone",
#         "xbox-series-x",
#         "n64",
#         "gamecube",
#         "switch",
#         "wii",
#         "wii-u",
#         "gba",
#         "ds",
#         "3ds",
#         "vita",
#         "ios",
#         "stadia",
#         "dreamcast",
#         "pc",
#     ]

#     games_list_of_dicts = []
#     for platform in PLATFORMS:
#         games_on_platform = scrape(platform)
#         games_list_of_dicts.extend(games_on_platform)
#     return pd.DataFrame(games_list_of_dicts).sort_values("name")


# if __name__ == "__main__":
#     res_df = generate_df()
#     res_df.to_csv(r"./input/input.csv", index=False)
