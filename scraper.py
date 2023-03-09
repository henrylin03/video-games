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


def find_release_date(game_elem):
    nested_span_tags_without_class = game_elem.find_all("span", {"class": None})
    if len(nested_span_tags_without_class) > 1:
        raise Exception("More than one release date found for game.")
    return nested_span_tags_without_class[0].text


def scrape(platform):
    DRIVER = setup_chrome_driver()
    url_platform = f"https://www.metacritic.com/browse/games/release-date/available/{platform}/name?view=condensed"
    DRIVER.get(url_platform)

    platform_str = DRIVER.find_element(
        By.XPATH, ".//*[@class='platform']/*[@class='data']"
    ).text

    last_page = DRIVER.find_element(
        By.XPATH, ".//*[@class='page last_page']/*[@class='page_num']"
    ).text

    games_by_platform_list_of_dicts = []
    for page_no in range(int(last_page)):
        if page_no:  # page numbers on metacritic are zero-indexed
            DRIVER.get(f"{url_platform}&page={page_no}")

        expand_buttons = DRIVER.find_elements(By.XPATH, ".//button[text()='Expand']")
        # [button.click() for button in expand_buttons]

        page_html = DRIVER.page_source
        soup = BeautifulSoup(page_html, "html.parser")

        games_elems_on_page = soup.find_all("tr", class_="expand_collapse")
        for g in games_elems_on_page:
            game_name = g.find("a", class_="title").text.replace("\n", "")
            release_date = find_release_date(g)

            print(release_date)
            return

        break
        # release_date = g.find_element(
        #     By.XPATH, ".//*[@class='details']/span[not(@class)]"
        # ).text
        # summary = g.find_element(By.XPATH, ".//*[@class='summary']/p").text
        # metascore = g.find_element(
        #     By.XPATH, ".//*[@class='score']/*[@class='metascore_anchor']/div"
        # ).text
        # userscore = g.find_element(
        #     By.XPATH,
        #     ".//*[@class='score title']/*[@class='metascore_anchor']/div",
        # ).text  # a bit confusing for Metacritic to call its user score elem's class "metascore_anchor" as well!

        # games_attributes_dict = {
        #     "name": game_name,
        #     "platform": platform_str,
        #     "release_date": release_date,
        #     "summary": summary,
        #     "metascore": metascore,
        #     "userscore": userscore,
        # }
        # games_by_platform_list_of_dicts.append(games_attributes_dict)
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
