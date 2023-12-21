  <h2 align="center">ScrapeResearchArticles</h2>

  <p align="center">
    An efficient way to collect results from the ACM, Springer, IEEE Xplore, and ScienceDirect (Elsevier) digital libraries


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#Scope">Scope</a></li>
        <li><a href="#dependencies">Dependencies</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#steps">Steps</a></li>
      </ul>
    </li>
    <li><a href="#status">Status</a></li>
    <li><a href="#issues">Issues</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

In the ever-expanding landscape of academic research, efficiently navigating and accessing papers from reputable databases is a paramount challenge for researchers. This project addresses this issue by developing a web scraper tailored to enhance the search and categorization process for papers within the ACM, Springer, IEEE Xplore, and ScienceDirect (Elsevier) online databases.

The project begins with a curated compilation of 296 journals and conferences, including their CCF, Core, and Qualis rankings, encapsulated in the "_SelectedJournalsAndConferences.csv_" file. The web scraper employs a Levenshtein ratio-based similarity metric to compare the titles of search results with the entries in the compiled dataset. This allows for a flexible and user-specified threshold for similarity percentages, enabling researchers to tailor their search criteria.

Upon conducting a search, the scraper meticulously analyzes each search result's journal or conference title, determining its similarity to the precompiled list. Results exceeding the specified similarity threshold are systematically organized and stored in a user-designated CSV file, streamlining the process of identifying relevant publications.

The scraper's functionality extends to multiple pages, ensuring a comprehensive examination of search results. To keep users informed of the scraper's progress, status alerts are provided at the completion of each page traversal. This user-friendly approach enhances transparency and facilitates effective utilization of the tool.

As a tool designed to optimize the efficiency of literature searches and paper categorization, this web scraper offers a valuable resource for researchers seeking to streamline their exploration of academic databases. Its adaptability, user-friendly interface, and systematic categorization contribute to a more efficient and informed research experience, empowering researchers to stay abreast of the latest developments in their respective fields.
### Scope

* This web scraping tool is built on the Selenium framework, utilizing the EDGE webdriver for effective scraping operations. Notably, its design is modular, facilitating easy extension to support alternative web browsers such as Chrome, Firefox, and others.

### Dependencies

* asttokens @ file:///home/conda/feedstock_root/build_artifacts/asttokens_1698341106958/work
* attrs==23.1.0
* beautifulsoup4==4.12.2
* bs4==0.0.1
* certifi==2023.11.17
* cffi==1.16.0
* charset-normalizer==3.3.2
* colorama @ file:///home/conda/feedstock_root/build_artifacts/colorama_1666700638685/work
* comm @ file:///home/conda/feedstock_root/build_artifacts/comm_1691044910542/work
* debugpy @ file:///C:/b/abs_c0y1fjipt2/croot/debugpy_1690906864587/work
* decorator @ file:///home/conda/feedstock_root/build_artifacts/decorator_1641555617451/work
* exceptiongroup==1.1.3
* executing @ file:///home/conda/feedstock_root/build_artifacts/executing_1698579936712/work
* h11==0.14.0
* idna==3.4
* importlib-metadata @ file:///home/conda/feedstock_root/build_artifacts/importlib-metadata_1701632192416/work
* ipykernel @ file:///D:/bld/ipykernel_1698244157926/work
* ipython @ file:///D:/bld/ipython_1701831845989/work
* jedi @ file:///home/conda/feedstock_root/build_artifacts/jedi_1696326070614/work
* jupyter_client @ file:///home/conda/feedstock_root/build_artifacts/jupyter_client_1699283905679/work
* jupyter_core @ file:///D:/bld/jupyter_core_1698673856358/work
* Levenshtein==0.23.0
* lxml==4.9.3
* matplotlib-inline @ file:///home/conda/feedstock_root/build_artifacts/matplotlib-inline_1660814786464/work
* nest-asyncio @ file:///home/conda/feedstock_root/build_artifacts/nest-asyncio_1697083700168/work
* outcome==1.3.0.post0
* packaging @ file:///home/conda/feedstock_root/build_artifacts/packaging_1696202382185/work
* parso @ file:///home/conda/feedstock_root/build_artifacts/parso_1638334955874/work
* pickleshare @ file:///home/conda/feedstock_root/build_artifacts/pickleshare_1602536217715/work
* platformdirs @ file:///home/conda/feedstock_root/build_artifacts/platformdirs_1701708255999/work
* prompt-toolkit @ file:///home/conda/feedstock_root/build_artifacts/prompt-toolkit_1702399386289/work
* psutil @ file:///C:/Windows/Temp/abs_b2c2fd7f-9fd5-4756-95ea-8aed74d0039flsd9qufz/croots/recipe/psutil_1656431277748/work
* pure-eval @ file:///home/conda/feedstock_root/build_artifacts/pure_eval_1642875951954/work
* pycparser==2.21
* Pygments @ file:///home/conda/feedstock_root/build_artifacts/pygments_1700607939962/work
* PySocks==1.7.1
* python-dateutil @ file:///home/conda/feedstock_root/build_artifacts/python-dateutil_1626286286081/work
* python-dotenv==1.0.0
* pywin32==305.1
* pyzmq @ file:///D:/bld/pyzmq_1660329059232/work
* rapidfuzz==3.5.2
* requests==2.31.0
* selenium==4.15.2
* six @ file:///home/conda/feedstock_root/build_artifacts/six_1620240208055/work
* sniffio==1.3.0
* sortedcontainers==2.4.0
* soupsieve==2.5
* stack-data @ file:///home/conda/feedstock_root/build_artifacts/stack_data_1669632077133/work
* tornado @ file:///D:/bld/tornado_1656937966227/work
* traitlets @ file:///home/conda/feedstock_root/build_artifacts/traitlets_1701095650114/work
* trio==0.23.1
* trio-websocket==0.11.1
* typing_extensions @ file:///home/conda/feedstock_root/build_artifacts/typing_extensions_1702176139754/work
* urllib3==2.1.0
* wcwidth @ file:///home/conda/feedstock_root/build_artifacts/wcwidth_1700607916581/work
* webdriver-manager==4.0.1
* wsproto==1.2.0
* zipp @ file:///home/conda/feedstock_root/build_artifacts/zipp_1695255097490/work




<!-- GETTING STARTED -->

## Getting Started

To get this project running on your local machine, follow these simple steps:

### Steps

1. Clone the repo
   ```sh
   git clone https://github.com/neeraj-tiwary/PhD-ScrapeResearchArticles.git
   ```
2. Make sure you're running Python 3 (I wrote and tested this project with Python 3.10.13 64-bit)
   ```sh
   python -V
   ```
3. Install all the packages specified in the configuration file (`requirements.txt`)
   ```sh
   pip install -r requirements.txt
   ```
4. You will need the latest version of Microsoft's EDGE installed on your machine
5. Create a file called `config.py` inside this repo and add the following:
   ```py
   from common_functions import platform

   if platform == "win32":
       path_to_search_results = "C:/<PATH TO SEARCH RESULTS>"
   else:
       path_to_search_results = "/Users/<PATH TO SEARCH RESULTS>"
   ``` 
6. View the "Name" column inside `SelectedJournalsAndConferences.csv`: this is the list of names whose [similarity (Levenshtein ratio)](https://rawgit.com/ztane/python-Levenshtein/master/docs/Levenshtein.html#Levenshtein-ratio) will be checked against each search result's journal/conference name. Feel free to modify this column on your local machine to add/remove journal names (not) of interest to you. 
7. Execute `main.py` using Python
   ```sh
   PATH_TO_PYTHON_INTERPRETER PATH_TO_main.py
   ``` 


<!-- STATUS -->
## Status
Given that the layouts of online research databases are updated occasionally, the scraper may also need to be updated accordingly to successfully retrieve the necessary information therein. The table below provides the current status of the scraper's ability to retrieve information from different online research databases.
<i>As of 12/22/23...</i>

|   Database      | Scraper Status     |
|:---------------:|:------------------:|
|     ACM         |        ✅          |
|   Springer      |        ✅          |
| IEEE Xplore     |        ✅          |
| ScienceDirect   |        ✅          |


<!-- ISSUES -->
## Issues
On Windows only: Selenium's quit() method alone fails to kill chromedriver processes thereby leading to a sort of memory leak. To counter this, I added a batch file (`kill_chromedriver.bat`) that kills all `chrome.exe` processes. As a result, ANY Chrome process unrelated to this program will ALSO die at the hands of this rather brute approach.  



<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

🏠 neeraj.tiwary@gmail.com

Project Link: [https://github.com/neeraj-tiwary/PhD-ScrapeResearchArticles](https://github.com/neeraj-tiwary/PhD-ScrapeResearchArticles)
