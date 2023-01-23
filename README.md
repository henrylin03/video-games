# Video Games: Data Analysis

## Description

In this project, I analyse video games' review data from [Metacritic.com](https://www.metacritic.com).

<p align="center">
    <img src="https://seekvectorlogo.com/wp-content/uploads/2020/06/metacritic-vector-logo.png" alt="" width="550">
</p>

The project is split into two parts:

### Scraper

The data is scraped from [Metacritic.com](https://www.metacritic.com) using the `scraper.py` script, which uses Selenium in Python.

Due to some video games having Metascores but insufficient user reviews for a user score, and vice versa, the script requires scraping of both lists.

### Analysis

`analysis.ipynb` is a Jupyter Notebook where I perform cleaning of the data using Python's `pandas` library, and analysis using SQL (`sqlite3`).

## Feedback

Thank you for joining me on my journey to learn coding and data analysis!

If you have any feedback or suggestions, please feel free to raise a [GitHub Issue](https://github.com/henrylin03/video-games/issues).
