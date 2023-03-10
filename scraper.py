import re
import sys
import requests
import lxml
from bs4 import BeautifulSoup
import pandas as pd


def find_release_date(game_elem):
    nested_span_tags_without_class = game_elem.find_all("span", {"class": None})
    if len(nested_span_tags_without_class) > 1:
        raise Exception("More than one release date found for game.")
    return nested_span_tags_without_class[0].text


def scrape(platform):
    s = requests.Session()
    s.headers[
        "User-Agent"
    ] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

    url_platform = f"https://www.metacritic.com/browse/games/release-date/available/{platform}/name?view=condensed"

    r_platform = s.get(url_platform)
    soup_platform = BeautifulSoup(r_platform.content, "lxml")

    platform_str = (
        soup_platform.find("span", class_="data").text.replace("\n", "").strip()
    )
    print(f"\nScraping {platform_str} games...")

    last_page = soup_platform.find("li", class_="page last_page").contents[-1].text

    games_by_platform_list_of_dicts = []
    for page_no in range(int(last_page)):
        url_platform_page = f"{url_platform}&page={page_no}"
        r_page = s.get(url_platform_page)
        soup_page = BeautifulSoup(r_page.content, "lxml")

        games_elems_on_page = soup_page.find_all("tr", class_="expand_collapse")
        for g in games_elems_on_page:
            game_name = g.find("a", class_="title").text.replace("\n", "")
            release_date = find_release_date(g)
            summary = g.find("div", class_="summary").contents[1].text
            metascore = g.find("div", class_=re.compile("^metascore_w large game")).text
            userscore = g.find(
                "div", class_=re.compile("^metascore_w user large game")
            ).text

        games_attributes_dict = {
            "name": game_name,
            "platform": platform_str,
            "release_date": release_date,
            "summary": summary,
            "metascore": metascore,
            "userscore": userscore,
        }
        games_by_platform_list_of_dicts.append(games_attributes_dict)
        print(f"\t✅ Page {page_no + 1} of {last_page}")
    return games_by_platform_list_of_dicts


def generate_df():
    PLATFORMS = [
        "ps",
        "ps2",
        "ps3",
        "ps4",
        "ps5",
        "psp",
        "xbox",
        "xbox360",
        "xboxone",
        "xbox-series-x",
        "n64",
        "gamecube",
        "switch",
        "wii",
        "wii-u",
        "gba",
        "ds",
        "3ds",
        "vita",
        "ios",
        "stadia",
        "dreamcast",
        "pc",
    ]

    games_list_of_dicts = []
    for platform in PLATFORMS:
        games_on_platform = scrape(platform)
        games_list_of_dicts.extend(games_on_platform)
    return pd.DataFrame(games_list_of_dicts).sort_values("name")


if __name__ == "__main__":
    res_df = generate_df()
    res_df.to_csv(r"./input/input.csv", index=False)
    print("\n✅ CSV outputted")
