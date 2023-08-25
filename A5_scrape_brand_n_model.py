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


def extract_signature_shoes():
    url = "https://nbashoesdb.com/"
    # ACCESS TO PAGE
    driver = open_browser()
    driver.get(url)
    time.sleep(2)

    # extract nba shoes brands relation
    brand_list, quantity_list = [], []
    donut_legend = driver.find_element(By.ID, "dougnut-legend")
    # print(donut_legend.text)
    trs = donut_legend.find_elements(By.TAG_NAME, "tr")
    for tr in trs:
        brand = tr.find_elements(By.TAG_NAME, "td")[0].text.replace("°", "")
        qty = int(tr.find_elements(By.TAG_NAME, "td")[1].text)
        # print(brand, int(qty))
        brand_list.append(brand)
        quantity_list.append(int(qty))

    driver.quit()

    # print(len(brand_list), brand_list)
    # print(len(quantity_list), quantity_list)

    return brand_list, quantity_list


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

    print("Scrape Brand Shoes model quantity available on the market")

    # date info
    today = date_info()
    print(today)

    # extract signature shoes
    brand_list, quantity_list = extract_signature_shoes()
    print(len(brand_list), brand_list)
    print(len(quantity_list), quantity_list)

    # create date list match with df length
    date_list = [today]*len(brand_list)

    # save data to file
    df_dict = {"record date": date_list, "brand": brand_list, "quantity": quantity_list}

    # save csv
    save_csv(filename=f"csv\\5_shoe_brand_n_model_{today}.csv", dict=df_dict)
    # save h5file
    save_hdf(filename=f"h5\\5_shoe_brand_n_model_{today}.h5", group_name="data", dict=df_dict)

    # # test print
    # print("TEST PRINT")
    # # read h5
    # hdf = pd.read_hdf(f"h5\\5_shoe_brand_n_model_{today}.h5", 'data')
    # print(hdf)

    end_program(start_time)
    os._exit(1)


# ----------------------------------------------------
# while True:
#     schedule.run_pending()
#     time.sleep(3)
#
#     schedule.every().day.at("10:20").do(main)


if __name__ == "__main__":
    main()