from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import pandas as pd
import re
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


def extract_players_via_brand():
    url = "https://www.soleretriever.com/news/articles/every-nba-player-that-has-a-signature-sneaker-2022-2023"
    # ACCESS TO PAGE
    driver = open_browser()
    driver.get(url)
    time.sleep(2)

    # get brand and player sequence according to tag
    seq_list = []
    content = driver.find_element(By.ID, "content")
    tag_info = content.get_attribute("innerHTML")

    # split string by ">", turn to list
    tag_list = tag_info.split(">")
    # remove "</" & "<"
    tag_list = [re.sub("</", '', char) for char in tag_list]
    tag_list = [re.sub("<", '', char) for char in tag_list]

    for tag in tag_list:
        # clean h2 tag issues
        if tag.startswith("h2 ") and tag.endswith('-athletes-with-a-signature-sneaker"'):
            tag_type = tag.split(" ")[0]
            id_content = tag.replace('-athletes-with-a-signature-sneaker"', '"')
            id_content = id_content.replace("-", " ").split('id="')[1]
            id_content = id_content[:-1].title()
            # print(tag_type, id_content)
            seq_list.append([tag_type, id_content])

        # fix Anthony Edwards wrongly put in h2, should be h3 under brand adidas
        elif tag.startswith('h2 id="a-href'):
            tag_type = "h3"
            id_content = "Anthony Edwards"
            # print(tag_type, id_content)
            seq_list.append([tag_type, id_content])

        # split h3 with player and brand
        elif tag.endswith(")h3"):
            tag_type = "h2"
            id_content = tag.split(" (")[1].replace(")h3", "")
            # print(tag_type, id_content)
            seq_list.append([tag_type, id_content])
            tag_type = "h3"
            id_content = tag.split(" (")[0]
            # print(tag_type, id_content)
            seq_list.append([tag_type, id_content])

        # with whitespace after h2 and h3
        # fix Miscellaneous Brands at the end put in h3, in format: name (brand)
        elif tag.startswith("h2 ") and not tag.endswith('have-signature-sneaker"') or tag.startswith("h3 "):
            tag_type = tag.split(" ")[0]
            tag = tag.replace("nbsp", " ")
            id_content = tag.replace("-", " ").split('id="')[1]
            id_content = id_content[:-1].title()
            if id_content.count(" ") < 2:
                # print(tag_type, id_content)
                seq_list.append([tag_type, id_content])

    # reorder seq by mapping brand with player
    brand_player_list = []
    for seq in seq_list:
        # print(seq)
        if seq[0] == "h2":
            brand = seq[1]
        if seq[0] == "h3":
            player = seq[1]
            # fix special char issue for csv
            if player == "Luka Dončić":
                player = "Luka Doncic"
            # print(brand, player)
            brand_player_list.append([brand, player])

    return brand_player_list



def save_csv(filename, nested_list, col_list):
    df = pd.DataFrame(nested_list, columns=col_list)
    print(df)
    df.to_csv(filename, encoding="UTF-8")


def save_hdf(filename, group_name, data_list, col_list):
    df = pd.DataFrame(data_list, columns=col_list)
    print(df)
    df.to_hdf(filename, group_name, mode="w", format="table")


def main():
    start_time = start_program()

    print("Scrape NBA Player via Shoe Brand")

    # date info
    today = date_info()
    print(today)

    # extract signature shoes
    brand_player_list = extract_players_via_brand()

    for brand_player in brand_player_list:
        # print(brand_player)
        brand_player.insert(0, today)
    print(brand_player_list)

    # save csv
    save_csv(filename=f"csv\\6_shoe_brand_n_player_{today}.csv", nested_list=brand_player_list,
             col_list=["record date", "brand", "player"])
    # save h5file
    save_hdf(filename=f"h5\\6_shoe_brand_n_player_{today}.h5", group_name="data", data_list=brand_player_list,
             col_list=["record date", "brand", "player"])

    # # test print
    # print("TEST PRINT")
    # # read h5
    # hdf = pd.read_hdf(f"h5\\6_shoe_brand_n_player_{today}.h5", 'data')
    # print(hdf)

    end_program(start_time)
    os._exit(1)


# ----------------------------------------------------
# while True:
#     schedule.run_pending()
#     time.sleep(3)
#
#     schedule.every().day.at("10:25").do(main)


if __name__ == "__main__":
    main()