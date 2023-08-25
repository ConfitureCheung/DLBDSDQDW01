from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import pandas as pd
import schedule
import os
import numpy as np
import h5py


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


def extract_player_name():
    url = "https://www.nba.com/players"
    # ACCESS TO PAGE
    driver = open_browser()
    driver.get(url)
    time.sleep(2)

    ttl_num_of_pgs = driver.find_element("xpath", "//div[@class='Pagination_totalPages__jLWZ1']").text
    ttl_num_of_pgs = int(ttl_num_of_pgs.split(" ")[1])
    print(ttl_num_of_pgs)

    player_name_list = []
    # num of clicks to page end
    for i in range(ttl_num_of_pgs):
        # extract player name
        table = driver.find_element("xpath", "//table[@class='players-list']")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        trs = tbody.find_elements(By.TAG_NAME, "tr")
        for tr in trs:
            player_name = tr.find_elements(By.TAG_NAME, "td")[0].text
            player_name = " ".join(line.strip() for line in player_name.splitlines())  # fix splitline issue
            # print(type(player_name), player_name)
            player_name_list.append(player_name)

        # click next button after scrape on page is done
        driver.find_element("xpath", "//button[@title='Next Page Button']").click()
        time.sleep(2)

    driver.quit()

    return player_name_list


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

    print("Scrape NBA.com for NBA player name info")

    # date info
    today = date_info()
    print(today)

    player_name_list = extract_player_name()

    # create date list match with df length
    date_list = [today]*len(player_name_list)

    # save data to file
    df_dict = {"record date": date_list, "player name": player_name_list}

    # save csv
    save_csv(filename=f"csv\\1_nba_player_name_{today}.csv", dict=df_dict)
    # save h5file
    save_hdf(filename=f"h5\\1_nba_player_name_{today}.h5", group_name="data", dict=df_dict)

    # # test print
    # print("TEST PRINT")
    # # read h5
    # hdf = pd.read_hdf(f"h5\\1_nba_player_name_{today}.h5", 'data')
    # print(hdf)

    end_program(start_time)
    os._exit(1)  # for schedule work


# ----------------------------------------------------
# while True:
#     schedule.run_pending()
#     time.sleep(3)
#
#     schedule.every().day.at("10:00").do(main)


if __name__ == "__main__":
    main()



