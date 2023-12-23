from get_all_results import *


def main():
    if get_all_articles() is False:
        print("Please wait for this program to terminate...")
        raise SystemExit
    else:
        print("The search results have been scraped and updated in the target destination file ...")



if __name__ == "__main__":
    main()
