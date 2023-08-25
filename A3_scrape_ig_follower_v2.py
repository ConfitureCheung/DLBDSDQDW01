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


def open_browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_position(170, 0)  # set browser opening position
    # driver.maximize_window()

    return driver


def extract_ig_followers():
    url = "https://www.popularbasketballers.com/"
    # ACCESS TO PAGE
    driver = open_browser()
    driver.get(url)
    time.sleep(2)

    # extract nba player name and ig account followers
    player_name_list, ig_followers_list = [], []
    table = driver.find_element(By.TAG_NAME, "table")
    # print(table.text)
    trs = table.find_elements(By.TAG_NAME, "tr")[1:]
    for tr in trs:
        # print(tr.text)
        player_name = tr.find_elements(By.TAG_NAME, "td")[1].text
        ig_followers = int(tr.find_elements(By.TAG_NAME, "td")[-1].text.replace(",", ""))
        # print(player_name, ig_followers)
        player_name_list.append(player_name)
        ig_followers_list.append(ig_followers)

    # print(len(player_name_list), player_name_list)
    # print(len(ig_followers_list), ig_followers_list)

    driver.quit()
    time.sleep(1.5)

    return player_name_list, ig_followers_list


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

    print("Scrape IG followers of Popular NBA Basketballers")

    # date info
    today = date_info()
    print(today)

    # # read csv
    # df = pd.read_csv(f"1_nba_player_name_{today}.csv")
    # nba_player_name_list = df["player name"].tolist()

    # read hdf
    hdf = pd.read_hdf(f"h5\\1_nba_player_name_{today}.h5", 'data')
    nba_player_name_list = hdf["player name"].tolist()

    # extract signature shoes
    player_name_list, ig_followers_list = extract_ig_followers()
    # print(len(player_name_list), player_name_list)
    # print(len(ig_followers_list), ig_followers_list)

    # sort out non nba players
    print("Sort out non nba players.")
    for player_name, ig_followers in zip(player_name_list, ig_followers_list):
        if player_name not in nba_player_name_list:
            print(player_name, ig_followers)

    # keep only nba players info
    nba_player_list, nba_ig_followers_list = [], []
    for player_name, nba_ig_followers in zip(player_name_list, ig_followers_list):
        if player_name in nba_player_name_list:
            nba_player_list.append(player_name)
            nba_ig_followers_list.append(nba_ig_followers)

    # create date list match with df length
    date_list = [today]*len(nba_player_list)

    # save data to file
    df_dict = {"record date": date_list, "nba player": nba_player_list, "ig follower": nba_ig_followers_list}

    # save csv
    save_csv(filename=f"csv\\3_ig_followers_{today}.csv", dict=df_dict)
    # save h5file
    save_hdf(filename=f"h5\\3_ig_followers_{today}.h5", group_name="data", dict=df_dict)

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
#     schedule.every().day.at("10:10").do(main)


if __name__ == "__main__":
    main()