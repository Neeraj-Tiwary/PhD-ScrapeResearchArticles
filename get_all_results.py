from common_functions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Levenshtein import ratio
from bs4 import BeautifulSoup
from math import ceil
from operator import itemgetter
from urllib.parse import quote
from time import sleep
import re
import subprocess

import config


def quit_drivers(drivers):
    for driver in drivers:
        driver.quit()
        print("Error! Driver has quit.")

    return True


def is_valid_search() -> List:
    """
    - Input: N.A.
    - Output: 7 -> [1], [2], [3], [4] are drivers for ACM, Springer, IEEE, and ScienceDirect; [5] search query gathered from IO;
    --             [6], [7], [8], [9] are the number of pages to traverse when searching for results on ACM, Springer, IEEE, and ScienceDirect
    - Number of essential steps (labeled below as comments): 4
    """
    drivers = []
    try:
        # 0 - Query for search word
        query = io_query()


        ###################################################################################################
        # 1.1 - create drivers for each database
        driver_for_acm = make_chrome_headless()  # True hides automated browser
        drivers.append(driver_for_acm)
        print("Driver for ACM is ready.")

        url_acm = f"https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&AfterYear=2018&BeforeYear=2023&AllField=Keyword%3A%28{quote(query)}%29"

        # 1.2 - driver visits links with user input term as search query and check for results between years 2018 - 2023
        driver_for_acm.get(url_acm)

        # Implicit wait for 30 seconds
        driver_for_acm.implicitly_wait(100)

        # 1.3 - acm driver checks max page results
        source_code_acm = driver_for_acm.page_source
        soup_acm = BeautifulSoup(source_code_acm, "html.parser")
        try:
            # No of records in a page
            hits_to_show_acm_text = WebDriverWait(driver_for_acm, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "js--selected"))
            )
            hits_to_show_acm = int(hits_to_show_acm_text[0].text)

            # Total number of results of search query
            temp_hits_acm = soup_acm.find("span", class_="hitsLength").text.strip()
            hits_acm = "".join(filter(str.isalnum, temp_hits_acm))
        except:
            hits_acm = 0
            hits_to_show_acm = 0
            driver_for_acm.quit()

        max_pages_temp_acm = int(hits_acm) / hits_to_show_acm
        max_pages_acm = ceil(max_pages_temp_acm)

        print(
            "Please wait for the drivers to begin deploying on their respective digital libraries...", end="\n",
            flush=True,
        )
        print("max_pages_acm: %s , hits_to_show_acm: %s " % (max_pages_acm, hits_to_show_acm))

        # 1.4 Quit the driver
        #driver_for_acm.quit()
        ###################################################################################################

        ###################################################################################################
        # 2.1 - create drivers for each database
        driver_for_springer = make_chrome_headless()
        drivers.append(driver_for_springer)
        print("Driver for Springer is ready.")

        url_springer = f"https://link.springer.com/search?query={quote(query)}&showAll=true&date-facet-mode=between&facet-end-year=2023&facet-start-year=2018"

        # 2.2 - driver visits links with user input term as search query and check for results between years 2018 - 2023
        driver_for_springer.get(url_springer)

        # Implicit wait for 30 seconds
        driver_for_springer.implicitly_wait(500)

        # 2.3 - Springer driver parses max pages of results
        try:
            source_code_springer = driver_for_springer.page_source
            soup_springer = BeautifulSoup(source_code_springer, "html.parser")
            max_pages_springer = int(soup_springer.find("span", class_="number-of-pages").text.strip())
            hits_to_show_springer = 20
        except:
            max_pages_springer = 0
            hits_to_show_springer = 0

        print(
            "Please wait for the drivers to begin deploying on their respective digital libraries...", end="\n",
            flush=True,
        )
        print("max_pages_springer: %s , hits_to_show_springer: %s " % (max_pages_springer, hits_to_show_springer))

        # 2.4 Quit the driver
        #driver_for_springer.quit()
        ###################################################################################################

        ###################################################################################################
        # 3.1 - create drivers for each database
        driver_for_ieee = make_chrome_headless()
        drivers.append(driver_for_ieee)
        print("Driver for IEEE Xplore is ready.")

        url_ieee = f"https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&matchBoolean=true&queryText=(%22Author%20Keywords%22:{quote(query)})&ranges=2018_2023_Year"

        # 3.2 - driver visits links with user input term as search query and check for results between years 2018 - 2023
        driver_for_ieee.get(url_ieee)

        # Implicit wait for 30 seconds
        driver_for_ieee.implicitly_wait(100)

        # 3.3 - ieee driver checks max page results
        try:
            # No of records in a page
            hits_to_show_ieee_text = WebDriverWait(driver_for_ieee, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "strong"))
            )[1].text
            hits_to_show_ieee = int(hits_to_show_ieee_text.split('-')[1])

            # Total number of results of search query
            num_hits_ieee = int(WebDriverWait(driver_for_ieee, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "strong"))
            )[2].text)
        except:
            hits_to_show_ieee = 0
            num_hits_ieee = 0
            driver_for_ieee.quit()

        max_pages_temp_ieee = num_hits_ieee / hits_to_show_ieee
        max_pages_ieee = ceil(max_pages_temp_ieee)

        print(
            "Please wait for the drivers to begin deploying on their respective digital libraries...", end="\n",
            flush=True,
        )
        print("max_pages_ieee: %s , hits_to_show_ieee: %s " % (max_pages_ieee, hits_to_show_ieee))

        # 3.4 Quit the driver
        #driver_for_ieee.quit()
        ###################################################################################################

        ###################################################################################################
        # 4.1 - create drivers for each database
        driver_for_sciencedirect = make_chrome_headless()
        drivers.append(driver_for_sciencedirect)
        print("Driver for sciencedirect is ready.")

        url_sciencedirect = f"https://www.sciencedirect.com/search?date=2018-2023&tak=%s" % quote(query)

        # 4.2 - driver visits links with user input term as search query and check for results between years 2018 - 2023
        driver_for_sciencedirect.get(url_sciencedirect)

        # Implicit wait for 30 seconds
        driver_for_sciencedirect.implicitly_wait(100)

        # 4.3 - sciencedirect driver checks max page results
        try:
            # No of records in a page
            hits_to_show_sciencedirect_text = WebDriverWait(driver_for_sciencedirect, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "active-per-page"))
            )
            hits_to_show_sciencedirect = int(hits_to_show_sciencedirect_text[0].text)

            # Total number of results of search query
            num_hits_sciencedirect = WebDriverWait(driver_for_sciencedirect, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "search-body-results-text"))
            )
            num_hits_sciencedirect = int(num_hits_sciencedirect[0].text.split(" ")[0].replace(',', ''))

        except Exception as e:
            num_hits_sciencedirect = 0
            hits_to_show_sciencedirect = 0
            print("Exception: ", e)
            driver_for_sciencedirect.quit()

        #hits_to_show_ieee = int(25)
        max_pages_temp_sciencedirect = num_hits_sciencedirect / hits_to_show_sciencedirect
        max_pages_sciencedirect = ceil(max_pages_temp_sciencedirect)

        print(
            "Please wait for the drivers to begin deploying on their respective digital libraries...", end="\n",
            flush=True,
        )
        print("max_pages_sciencedirect: %s , hits_to_show_sciencedirect: %s " % (max_pages_sciencedirect, hits_to_show_sciencedirect))

        # 4.4 Quit the driver
        #driver_for_sciencedirect.quit()
        ###################################################################################################

        # Quit drivers
        print("Done and quit drivers!")
        #quit_drivers(drivers)

        # 5 - return data to get_all_results()
        return [
            driver_for_acm,
            driver_for_springer,
            driver_for_ieee,
            driver_for_sciencedirect,
            query,
            int(max_pages_acm),
            int(max_pages_springer),
            int(max_pages_ieee),
            int(max_pages_sciencedirect),
            int(hits_to_show_acm),
            int(hits_to_show_springer),
            int(hits_to_show_ieee),
            int(hits_to_show_sciencedirect)
        ]
    except Exception as e:
        fail_message(e)
        if platform == "win32":
            subprocess.call([r"kill_edgedriver.bat"])
        else:
            quit_drivers(drivers)
        return []
    except KeyboardInterrupt as k:
        fail_message(k)
        if platform == "win32":
            subprocess.call([r"kill_edgedriver.bat"])
            # raise SystemExit(0)
        else:
            quit_drivers(drivers)
        return []


def get_all_articles() -> bool:
    """
    - Input: N.A.
    - Output: bool (True/False) -> if True, then this function runs again
    - Number of essential steps (labeled below as comments): 5
    """
    try:
        # 1 - assign values from is_valid_search()
        (
            driver_for_acm,
            driver_for_springer,
            driver_for_ieee,
            driver_for_sciencedirect,
            query,
            max_pages_acm,
            max_pages_springer,
            max_pages_ieee,
            max_pages_sciencedirect,
            hits_to_show_acm,
            hits_to_show_springer,
            hits_to_show_ieee,
            hits_to_show_sciencedirect
        ) = itemgetter(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)(is_valid_search())

        # 2 - do IO to: (1) get similarity_percentage user wants, (2) create file for results, and (3) let user know that drivers are starting to find & place results now
        similarity_percentage, sp = itemgetter(0, 1)(sp_io())
        file_path = create_file(config.path_to_search_results)
        with open(str(file_path), "w", encoding="UTF8", newline="") as f:
            # create the csv writer
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)
        print_checking_all_results(sp)

        # 3 - create a list of titles to append to in order to prevent duplicate additions
        added_titles = []
        result_count = 0  # keep track of how many results are added to the final list
        drivers = []

        # 4 - check all databases
        # 4a - check acm first
        checkACM = input(
            "Would you like to check the ACM database? Enter 'y' if yes, otherwise enter any other key: "
        )

        if checkACM.lower() == "y":
            print("Checking results in ACM:")
            # webdriver for ACM
            #driver_for_acm = make_chrome_headless()
            drivers.append(driver_for_acm)

            with open(str(file_path), "a+", encoding="UTF8", newline="") as f:
                # create the csv writer
                writer = csv.writer(f)
                k = 0  # counts how many results match selected journals/conferences
                print('max_pages_acm: ', max_pages_acm)

                # List of JC belongs to ACM
                #list_of_selected_jc_acm = create_list_of_selected_jc("ACM")

                for i in range(int(max_pages_acm)):  # traverse each page
                    t = i + 1
                    print(f"Checking results on page {t}...")
                    url_acm = f"https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&AfterYear=2018&BeforeYear=2023&AllField=Keyword%3A%28{quote(query)}%29&startPage={str(i)}&pageSize={hits_to_show_acm}"
                    driver_for_acm.get(url_acm)
                    # Implicit wait for 30 seconds
                    driver_for_acm.implicitly_wait(100)
                    # parse source code
                    soup = BeautifulSoup(driver_for_acm.page_source, "html.parser")
                    # Get the result containers
                    result_containers = soup.findAll(
                        "div", class_="issue-item__content"
                    )
                    j = 0  # set increment representing how many hits the user wants to traverse

                    # Loop through every container
                    for container in result_containers:
                        # Final results list
                        results = []

                        # check if result journal is in list of selected journals
                        try:
                            journal = container.find("div", class_="issue-item__detail").a["title"]
                        except:
                            journal = "Not Found"

                        #matched_journal = [matched_with for matched_with in list_of_selected_jc_acm if (ratio(journal, matched_with) >= similarity_percentage)]
                        matched_journal = [matched_with for matched_with in list_of_selected_jc if (ratio(journal, matched_with) >= similarity_percentage)]

                        if len(matched_journal) > 0:
                            # Result title
                            title_tmp = container.find("h5").text
                            title = title_tmp.strip("'")
                            if (
                                added_titles.count(title) == 0
                            ):  # only add to result CSV if title hasn't been added already
                                added_titles.append(title)
                                k += 1
                                result_count += 1
                                print(
                                    f"Placed {k} results from ACM and {result_count} in total so far! Still checking..."
                                )
                                # Result url
                                temp_url = container.find("h5").a["href"]
                                lst = [
                                    "https:/",
                                    temp_url[:4],
                                    ".org",
                                    temp_url[4:],
                                ]
                                url = "".join(lst)
                                # Result authors
                                authors = []
                                ul = container.find("ul")
                                for li in ul.findAll("li"):  # list of authors
                                    authors.append(
                                        li.text.rstrip(", \n").strip("'")
                                    )
                                t_author_list = str(authors).strip("[]")
                                author_list = t_author_list.replace("'", "")
                                # Result date
                                date = (
                                    container.find(
                                        "div", class_="issue-item__detail"
                                    )
                                    .find("span", class_="dot-separator")
                                    .find("span")
                                    .text.rstrip(", ")
                                )
                                numbers = re.compile(r"\d+(?:\.\d+)?")
                                p_year = numbers.findall(date)[0]
                                # Result num
                                j += 1
                                # Similarity %
                                t_sim_per = max([ratio(journal, matched_jour) * 100 for matched_jour in matched_journal])
                                matched_with = [matched_jour for matched_jour in matched_journal if ratio(journal, matched_jour) * 100 >= t_sim_per][0]
                                sim_per = format(t_sim_per, ".2f")
                                data = [
                                    url,
                                    title,
                                    author_list,
                                    p_year,
                                    journal,
                                    matched_with,
                                    sim_per,
                                    "ACM",
                                    query,
                                ]
                                # write the data
                                writer.writerow(data)
            driver_for_acm.quit()
            print("Done! Driver for ACM has quit.")
        else:
            print("Skipping the ACM database...")

        # 4b - check springer second
        checkSpringer = input(
            "Would you like to check the Springer database? Enter 'y' if yes, otherwise enter any other key: "
        )
        drivers.append(driver_for_springer)

        if checkSpringer.lower() == "y":
            i_springer = 0  # set increment representing how many pages the user wants to traverse
            print("Checking results in Springer:")
            print("max pages springer:", max_pages_springer)
            # webdriver for springer
            #driver_for_springer = make_chrome_headless()
            drivers.append(driver_for_springer)

            with open(str(file_path), "a+", encoding="UTF8", newline="") as f:
                # create the csv writer
                writer = csv.writer(f)
                # list of journal names to append to prevent duplicate additions
                added_titles = []
                k = 0  # counts how many results match selected journals/conferences
                print('max_pages_springer: ', max_pages_springer)

                # List of JC belongs to Springer
                #list_of_selected_jc_springer = create_list_of_selected_jc("Springer")

                for i in range(int(max_pages_springer)):  # traverse each page
                    t = i + 1
                    print(f"Checking results on page {t}...")
                    url_springer = f"https://link.springer.com/search/page/{str(t)}?facet-end-year=2023&date-facet-mode=between&facet-start-year=2018&query={quote(query)}&showAll=true"
                    driver_for_springer.get(url_springer)
                    # Implicit wait for 30 seconds
                    driver_for_springer.implicitly_wait(100)
                    # parse source code
                    soup = BeautifulSoup(driver_for_springer.page_source, "html.parser")
                    # get result containers
                    result_containers = soup.findAll("li", class_="no-access")
                    j = 0  # set increment representing how many hits the user wants to traverse
                    # Loop through every container
                    for container in result_containers:
                        # Result journal title
                        try:
                            journal = container.find("a", class_="publication-title")["title"]
                        except:
                            journal = "Not found"

                        #matched_journal = [matched_with for matched_with in list_of_selected_jc_springer if (ratio(journal, matched_with) >= similarity_percentage)]
                        matched_journal = [matched_with for matched_with in list_of_selected_jc if (ratio(journal, matched_with) >= similarity_percentage)]

                        if len(matched_journal) > 0:
                            # Result title
                            title = container.find("h2").text.lstrip()
                            if (
                                added_titles.count(title) == 0
                            ):  # only add to result CSV if title hasn't been added already
                                added_titles.append(title)
                                k += 1
                                result_count += 1
                                print(
                                    f"Placed {k} results from Springer and {result_count} in total so far! Still checking..."
                                )
                                # Result url
                                temp_url = container.find("h2").a["href"]
                                lst = ["https://link.springer.com", temp_url]
                                url = "".join(lst)
                                # Result author(s)
                                author_list = container.find(
                                    "span", class_="authors"
                                ).text.lstrip()
                                # Result publish year
                                p_year = container.find("span", class_="year")[
                                    "title"
                                ]
                                # Result num
                                j += 1
                                # Similarity %
                                t_sim_per = max([ratio(journal, matched_jour) * 100 for matched_jour in matched_journal])
                                matched_with = [matched_jour for matched_jour in matched_journal if ratio(journal, matched_jour) * 100 >= t_sim_per][0]
                                sim_per = format(t_sim_per, ".2f")
                                data = [
                                    url,
                                    title,
                                    author_list,
                                    p_year,
                                    journal,
                                    matched_with,
                                    sim_per,
                                    "Springer",
                                    query,
                                ]
                                # write the data
                                writer.writerow(data)
            driver_for_springer.quit()
            print("Done! Driver for Springer has quit.")
        else:
            print("Skipping the Springer database...")

        # 4c - check ieee third
        checkIEEE = input(
            "Would you like to check the IEEE Xplore database? Enter 'y' if yes, otherwise enter any other key: "
        )
        drivers.append(driver_for_ieee)

        if checkIEEE.lower() == "y":
            print("Checking results in IEEE:")
            # webdriver for ieee
            #driver_for_ieee = make_chrome_headless()
            drivers.append(driver_for_ieee)

            with open(str(file_path), "a+", encoding="UTF8", newline="") as f:
                # create the csv writer
                writer = csv.writer(f)
                k = 0  # counts how many results match selected journals/conferences
                print('max_pages_ieee: ', max_pages_ieee)

                # List of JC belongs to Springer
                #list_of_selected_jc_ieee = create_list_of_selected_jc("IEEE")

                for i in range(1, int(max_pages_ieee) + 1):
                    t = i
                    print(f"Checking results on page {t}...")
                    url_ieee = f"https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&matchBoolean=true&queryText=(%22Author%20Keywords%22:{quote(query)})&ranges=2018_2023_Year&pageNumber={str(i)}&rowsPerPage={hits_to_show_ieee}"
                    driver_for_ieee.get(url_ieee)

                    # Implicit wait for 30 seconds
                    sleep(10)
                    driver_for_ieee.implicitly_wait(300)
                    #results_per_page = driver_for_ieee.find_elements_by_class_name(
                    #    "List-results-items"
                    #)
                    soup = BeautifulSoup(driver_for_ieee.page_source, "html.parser")
                    # get result containers
                    result_containers = soup.findAll("div", class_="List-results-items")
                    for container in result_containers:
                        # journal title
                        try:
                            journal = container.find("div", class_="description").a.text
                        except:
                            journal = "Not found"

                        #for matched_with in list_of_selected_jc_ieee:
                        #matched_journal = [matched_with for matched_with in list_of_selected_jc_ieee if (ratio(journal, matched_with) >= similarity_percentage)]
                        matched_journal = [matched_with for matched_with in list_of_selected_jc if (ratio(journal, matched_with) >= similarity_percentage)]

                        if len(matched_journal) > 0:
                            # Result title
                            title = container.find("h3").text.lstrip()
                            if (
                                added_titles.count(title) == 0
                            ):  # only add to result CSV if title hasn't been added already
                                added_titles.append(title)
                                k += 1
                                result_count += 1
                                print(
                                    f"Placed {k} results from IEEE and {result_count} in total so far! Still checking..."
                                )
                                # Result url
                                tmp_url = container.find("h3").a["href"]
                                lst = ["https://ieeexplore.ieee.org", tmp_url]
                                url = "".join(lst)
                                # Result author_list
                                author_list = container.find(
                                    "p", class_="author"
                                ).text
                                # Result publish year
                                p_year_tmp = container.find(
                                    "div", class_="publisher-info-container"
                                ).text
                                p_year = re.sub(r"\D", "", p_year_tmp)
                                # Similarity %
                                t_sim_per = max([ratio(journal, matched_jour) * 100 for matched_jour in matched_journal])
                                matched_with = [matched_jour for matched_jour in matched_journal if ratio(journal, matched_jour) * 100 >= t_sim_per][0]
                                sim_per = format(t_sim_per, ".2f")
                                data = [
                                    url,
                                    title,
                                    author_list,
                                    p_year,
                                    journal,
                                    matched_with,
                                    sim_per,
                                    "IEEE",
                                    query,
                                ]
                                # write the data
                                writer.writerow(data)
            driver_for_ieee.quit()
            print("Done! Driver for IEEE Xplore has quit.")
        else:
            print("Skipping the IEEE Xplore database...")

        # 4d - check sciencedirect fourth
        checksciencedirect = input(
            "Would you like to check the sciencedirect database? Enter 'y' if yes, otherwise enter any other key: "
        )
        drivers.append(driver_for_sciencedirect)

        if checksciencedirect.lower() == "y":
            print("Checking results in sciencedirect:")
            # webdriver for ieee
            #driver_for_sciencedirect = make_chrome_headless()
            drivers.append(driver_for_sciencedirect)

            with open(str(file_path), "a+", encoding="UTF8", newline="") as f:
                # create the csv writer
                writer = csv.writer(f)

                k = 0  # counts how many results match selected journals/conferences
                print('max_pages_sciencedirect: ', max_pages_sciencedirect)

                # List of JC belongs to Elsevier
                #list_of_selected_jc_sciencedirect = create_list_of_selected_jc("Elsevier")

                for i in range(int(max_pages_sciencedirect)):  # traverse each page
                    t = i + 1
                    var_offset = i * hits_to_show_sciencedirect
                    print(f"Checking results on page {t}...")

                    # Read data from URL
                    url_sciencedirect = f"https://www.sciencedirect.com/search?date=2018-2023&tak=%s&offset=%s" % (quote(query), var_offset)
                    driver_for_sciencedirect.get(url_sciencedirect)
                    # Implicit wait for 30 seconds
                    driver_for_sciencedirect.implicitly_wait(100)

                    # Initialize code
                    result_containers = driver_for_sciencedirect.find_elements(By.CSS_SELECTOR, "#srp-results-list > ol > li > div > div.result-item-content")
                    #print('result_containers:', result_containers)
                    j = 0  # set increment representing how many hits the user wants to traverse

                    # Loop through every container
                    for container in result_containers:
                        html = container.get_attribute('outerHTML')
                        container = BeautifulSoup(html, "lxml")

                        # Final results list
                        results = []
                        # check if result journal is in list of selected journals
                        journal = (
                            container.find("span", class_="srctitle-date-fields")
                            .find("a", class_="anchor subtype-srctitle-link anchor-default anchor-has-inherit-color")
                            .find("span", class_="anchor-text")
                            .find("span")
                            .text.strip()
                        )
                        #print('journal: ', journal)
                        #matched_journal = [matched_with for matched_with in list_of_selected_jc_sciencedirect if (ratio(journal, matched_with) >= similarity_percentage)]
                        matched_journal = [matched_with for matched_with in list_of_selected_jc if (ratio(journal, matched_with) >= similarity_percentage)]

                        if len(matched_journal) > 0:
                        #for matched_with in list_of_selected_jc_sciencedirect:
                            #if ratio(journal, matched_with) >= similarity_percentage:
                            # Result title
                            title = container.find("h2").text.strip("'")
                            if (
                                    added_titles.count(title) == 0
                            ):  # only add to result CSV if title hasn't been added already
                                added_titles.append(title)
                                k += 1
                                result_count += 1
                                # Result url
                                temp_url = container.find("h2").a["href"]
                                lst = [
                                    "https://sciencedirect.com",
                                    temp_url,
                                ]
                                url = "".join(lst)
                                # Result authors
                                authors = []
                                ul = container.findAll("span", class_="author")
                                for li in ul:  # list of authors
                                    authors.append(
                                        li.text.rstrip(", \n").strip("'")
                                    )
                                t_author_list = str(authors).strip("[]")
                                author_list = t_author_list.replace("'", "")
                                # Result date
                                date = (
                                    container.select_one(
                                        "span.srctitle-date-fields > span:last-child"
                                    )
                                    .text.strip()
                                )

                                numbers = re.compile(r"\d+(?:\.\d+)?")
                                p_year = numbers.findall(date)[-1]
                                # Result num
                                j += 1
                                # Similarity %
                                t_sim_per = max([ratio(journal, matched_jour) * 100 for matched_jour in matched_journal])
                                matched_with = [matched_jour for matched_jour in matched_journal if ratio(journal, matched_jour) * 100 >= t_sim_per][0]
                                sim_per = format(t_sim_per, ".2f")
                                data = [
                                    url,
                                    title,
                                    author_list,
                                    p_year,
                                    journal,
                                    matched_with,
                                    sim_per,
                                    "sciencedirect",
                                    query,
                                ]
                                # write the data
                                writer.writerow(data)
                                print(
                                    f"Placed {k} results from sciencedirect and {result_count} in total so far! Still checking..."
                                )
            driver_for_sciencedirect.quit()
            print("Done! Driver for sciencedirect has quit.")
        else:
            print("Skipping the sciencedirect database...")

    # 5 - let user know this round of searching for & placing results is finished
        print(f"Done! Placed {result_count} results in total.\n")
        quit_drivers(drivers)
        return True
    except Exception as e:
        fail_message(e)
        if platform == "win32":
            subprocess.call([r"kill_edgedriver.bat"])
            # raise SystemExit(0)
        else:
            driver_for_acm.quit()
            print("Error! Driver for ACM has quit.")
            driver_for_springer.quit()
            print("Error! Driver for Springer has quit.")
            driver_for_ieee.quit()
            print("Error! Driver for IEEE Xplore has quit.")
            driver_for_sciencedirect.quit()
            print("Error! Driver for sciencedirect has quit.")
        return False
    except KeyboardInterrupt as k:
        fail_message(k)
        if platform == "win32":
            subprocess.call([r"kill_edgedriver.bat"])
            # raise SystemExit(0)
        else:
            driver_for_acm.quit()
            print("Error! Driver for ACM has quit.")
            driver_for_springer.quit()
            print("Error! Driver for Springer has quit.")
            driver_for_ieee.quit()
            print("Error! Driver for IEEE Xplore has quit.")
            driver_for_sciencedirect.quit()
            print("Error! Driver for sciencedirect has quit.")
        return False



