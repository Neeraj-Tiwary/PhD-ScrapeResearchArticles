from get_all_results import *


def main():
    while True:
        if get_all_articles() is False:
            print("Please wait for this program to terminate...")
            raise SystemExit


if __name__ == "__main__":
    main()
