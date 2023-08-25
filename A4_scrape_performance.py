from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import pandas as pd
import os
import schedule


def start_program():
    return time.time()


def end_program(start_time):
    end_time = time.time()
    seconds = end_time - start_time
    minutes = seconds // 60
    hours = minutes // 60
    print("################")
    print("%02d:%02d:%02d" % (hours, minutes % 60, seconds % 60))


def date_info():
    dt = datetime.today()
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    dt = str(dt.date())
    return dt


def url_date_range(fm_date, to_date):
    # date info
    today = datetime.today().date()
    # print(today)

    # verify date info
    if fm_date >= to_date:
        print("Search date range incorrect.")
        os._exit(1)
    elif to_date > today:
        print("Search date range has passed today")
        os._exit(1)

    return fm_date, to_date


def open_browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_position(170, 0)  # set browser opening position
    # driver.maximize_window()

    return driver


def extract_player_performance(fm_date, to_date):
    # create url list
    fm_date, to_date = url_date_range(fm_date=fm_date, to_date=to_date)
    # url = "https://kixstats.com/ratings?from=2023-06-08&to=2023-07-07&type=choice&league=NBA&by=kicks#results"
    url_core1 = f"https://kixstats.com/ratings?from={fm_date}&to={to_date}&type="
    url_core2 = "&league=NBA&by=kicks#results"

    print("6 urls: Top Players Choice, Top Scorer Kicks, Top Rebound Kicks, Top Assist Kicks, Top Steal Kicks, Top Block Kicks")

    # key for use in csv, value for use in url
    top_dict = {"top player": "choice", "top scorer": "pts", "top rebound": "reb",
                "top assist": "ast", "top steal": "stl", "top block": "blk"}

    url_top = f"{url_core1}{top_dict.get('top player')}{url_core2}"
    url_pts = f"{url_core1}{top_dict.get('top scorer')}{url_core2}"
    url_reb = f"{url_core1}{top_dict.get('top rebound')}{url_core2}"
    url_ast = f"{url_core1}{top_dict.get('top assist')}{url_core2}"
    url_stl = f"{url_core1}{top_dict.get('top steal')}{url_core2}"
    url_blk = f"{url_core1}{top_dict.get('top block')}{url_core2}"

    url_master_list = [url_top, url_pts, url_reb, url_ast, url_stl, url_blk]
    # print(url_master_list)

    choice_list, rank_list, shoe_model_list = [], [], []
    for url, key in zip(url_master_list, list(top_dict.keys())):
        # ACCESS TO PAGE
        driver = open_browser()
        driver.get(url)
        time.sleep(2)

        # extract shoe ranking
        right_panel = driver.find_elements(By.CLASS_NAME, "card-body")[-1]
        # print(right_panel.text)
        bottom_panel = right_panel.find_elements(By.CLASS_NAME, "row")[2]
        # print(bottom_panel.text)

        rows = bottom_panel.find_elements(By.CLASS_NAME, "filter-kick")
        for row in rows:
            # print(row.text)
            rank = row.find_element(By.CLASS_NAME, "corner-text-big").text
            ttl_rank = int(rank.split(".")[-1])
            shoe_model = row.find_element(By.TAG_NAME, "h1").text
            # print(rank, shoe_model)
            rank_list.append(rank)
            shoe_model_list.append(shoe_model)

        # create type list match with rank list
        choice_list.extend([key]*ttl_rank)

        driver.quit()

        # print(len(choice_list), choice_list)
        # print(len(rank_list), rank_list)
        # print(len(shoe_model_list), shoe_model_list)

    return choice_list, rank_list, shoe_model_list


def save_csv(filename, dict):
    df = pd.DataFrame(dict)
    print(df)
    df.to_csv(filename)


def save_hdf(filename, group_name, dict):
    df = pd.DataFrame(dict)
    print(df)
    df.to_hdf(filename, group_name, mode="w", format="table")


def main():
    start_time = start_program()

    print("Scrape Top Player Performance and Shoe Selection")

    # date info
    today = date_info()
    print(today)

    # set search date range here
    start_date = datetime(2023, 6, 8).date()
    end_date = datetime(2023, 7, 7).date()

    # extract signature shoes
    choice_list, rank_list, shoe_model_list = extract_player_performance(fm_date=start_date, to_date=end_date)
    print(len(choice_list), choice_list)
    print(len(rank_list), rank_list)
    print(len(shoe_model_list), shoe_model_list)

    # create date list match with df length
    date_list = [today]*len(choice_list)

    # save data to file
    df_dict = {"record date": date_list, "choice by": choice_list, "rank": rank_list, "shoe model": shoe_model_list}

    # save csv
    save_csv(filename=f"csv\\4_shoe_choice_by_top_{today}.csv", dict=df_dict)
    # save h5file
    save_hdf(filename=f"h5\\4_shoe_choice_by_top_{today}.h5", group_name="data", dict=df_dict)

    # # test print
    # print("TEST PRINT")
    # # read h5
    # hdf = pd.read_hdf(f"h5\\3_ig_followers_{today}.h5", 'data')
    # print(hdf)

    end_program(start_time)
    os._exit(1)


# ----------------------------------------------------
# while True:
#     schedule.run_pending()
#     time.sleep(3)
#
#     schedule.every().day.at("10:15").do(main)


if __name__ == "__main__":
    main()