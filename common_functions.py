from typing import List
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from os import path, makedirs
import csv
from sys import platform


def make_chrome_headless(o=True):
    """
    Return a headless driver of Chrome
    """
    headless_driver = webdriver.Edge()
    return headless_driver


def create_list_of_selected_jc(publisher) -> List:
    """
    Return the "SelectedJournalsAndConferences.csv" as a list
    """
    selected_jc = []
    with open("SelectedJournalsAndConferences.csv", mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if ((row["SJR-Quartile"] is not None and row["SJR-Quartile"] == "Q1") or (row["QUALIS"] in ["A1", "A2"] or row["CORE"] in ["A", "A*"] or row["CCF"] in ["A"])):
                if publisher == "all":
                    selected_jc.append(row["Name"])
                elif publisher in row["Publisher"]:
                    selected_jc.append(row["Name"])
    #selected_jc.pop(0)
    return selected_jc


def io_input(input_type) -> str:
    """
    IO: returns search term
    """
    if input_type == "query":
        return_str = input("Enter your search term here: ")
    elif input_type == "start_year":
        return_str = input("Enter your start year for the articles to be retrieved: ")
    elif input_type == "end_year":
        return_str = input("Enter your end year for the articles to be retrieved: ")
    return return_str


def io_hits_to_show(database) -> int:
    """
    IO: returns how many hits to search for per page
    """
    if database == "ACM":
        return input("How many hits would you like to search for per page? (max = 50): ")
    return input("How many hits would you like to search for per page? (10, 25, 50, or 75): ")


def create_file(path_to_search_results) -> str:
    """
    Return file path
    """
    file_name = input(
        "Enter a file name where you would like to store the search results: "
    )
    if not path.exists(path_to_search_results):
        makedirs(path_to_search_results)
    file_path = path.join(path_to_search_results, str(file_name + ".csv"))
    return file_path


def fail_message(e):
    """
    Print failure message
    """
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(e).__name__, e.args)
    print(message)


def print_checking_results(num_results, sp):
    """
    IO: print status to show results are getting checked
    *unused
    """
    print(
        "Checking "
        + str(num_results)
        + " results where journal/conference name matches selected ones by "
        + str(sp)
        + chr(37)
    )


def print_checking_all_results(sp):
    """
    IO: print status to show results are getting checked
    """
    print(
        "Checking all results where journal/conference name matches selected ones by "
        + str(sp)
        + chr(37)
    )


def sp_io() -> List:
    """
    Return (1) similarity percentage [0, 1] and (2) sp [0, 100]
    - The similarity corresponds to the minimum percentage likeness between the journal/conference name of each result and those listed in "SelectedJournalsAndConferences.csv"
    """
    similarity_percentage = float(
        input(
            "What is the minimum percentage likeness you like to check against the selected journals/conferences (choose between 0.0 and 1.0): "
        )
    )
    sp = similarity_percentage * 100
    return [similarity_percentage, sp]


def io_pages_to_show(
    database,
    max_pages,
    num_results_per_page=0,
) -> int:
    """
    IO: returns how many pages to search
    """
    if database == "Springer":
        return input(
            "How many pages would you like to see the results for? (max = %s and results per page = %s): "
            % (str(max_pages), str(num_results_per_page))
        )
    return input(
        "How many pages would you like to see the results for? (max = "
        + str(max_pages)
        + "): "
    )


# result CSV file's header
header = [
    "URL",
    "Title",
    "Author(s)",
    "Year",
    "Journal",
    #"Matched with Selected Journal/Conference",
    #"Similarity %",
    "Database",
    "Citations_Counts",
    "Open_Access",
    "Query",
    "Start_Year",
    "End_Year"
]

# create list of selected journals and conferences using below function
list_of_selected_jc = create_list_of_selected_jc("all")
#print(list_of_selected_jc)

