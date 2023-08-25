import time
from datetime import datetime
import pandas as pd
import numpy as np
import os
import plotly
import plotly.express as px
import plotly.graph_objects as go


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


def data_collection_n_cleansing():
    # read directory
    path = "h5"
    folder = os.listdir(path)

    _1_player_name_h5_list, _2_player_stat_h5_list, _3_ig_followers_h5_list, _4_shoe_choice_h5_list, \
    _5_shoe_brand_info_h5_list, _6_shoe_brand_player_h5_list = [], [], [], [], [], []
    for h5_file in folder:
        # merge h5 files by name
        if h5_file.startswith("1_"):
            # read hdf
            hdf = pd.read_hdf(f"{path}\\{h5_file}", 'data')
            _1_player_name_h5_list.append(hdf)

        if h5_file.startswith("2_"):
            # read hdf
            hdf = pd.read_hdf(f"{path}\\{h5_file}", 'data')
            _2_player_stat_h5_list.append(hdf)

        if h5_file.startswith("3_"):
            # read hdf
            hdf = pd.read_hdf(f"{path}\\{h5_file}", 'data')
            _3_ig_followers_h5_list.append(hdf)

        if h5_file.startswith("4_"):
            # read hdf
            hdf = pd.read_hdf(f"{path}\\{h5_file}", 'data')
            _4_shoe_choice_h5_list.append(hdf)

        if h5_file.startswith("5_"):
            # read hdf
            hdf = pd.read_hdf(f"{path}\\{h5_file}", 'data')
            _5_shoe_brand_info_h5_list.append(hdf)

        if h5_file.startswith("6_"):
            # read hdf
            hdf = pd.read_hdf(f"{path}\\{h5_file}", 'data')
            _6_shoe_brand_player_h5_list.append(hdf)


    # concatenate dfs to 1 master df
    player_name_h5 = pd.concat(_1_player_name_h5_list, axis=0)
    player_stat_h5 = pd.concat(_2_player_stat_h5_list, axis=0)
    ig_followers_h5 = pd.concat(_3_ig_followers_h5_list, axis=0)
    shoe_choice_h5 = pd.concat(_4_shoe_choice_h5_list, axis=0)
    shoe_brand_info_h5 = pd.concat(_5_shoe_brand_info_h5_list, axis=0)
    shoe_brand_player_h5 = pd.concat(_6_shoe_brand_player_h5_list, axis=0)

    return player_name_h5, player_stat_h5, ig_followers_h5, shoe_choice_h5, shoe_brand_info_h5, shoe_brand_player_h5


def main():
    start_time = start_program()

    # date info
    today = date_info()

    print("Data Visualization, demo by ig_followers")

    info1, info2, info3, info4, info5, info6 = data_collection_n_cleansing()

    # create pivot table to reorder the df format
    df3 = pd.pivot_table(info3, index=["nba player"], columns="record date", values="ig follower",
                                 aggfunc=np.sum, margins=True, margins_name="total")
    df3 = df3[0:-1]  # remove "total" at bottom
    df3 = df3.sort_values(by=["total"], ascending=False)
    df3 = df3[0:5]  # keep only top 5
    df3_t = df3.transpose()  # transpose row and col
    df3_t = df3_t[0:-1]  # remove "total" at bottom
    print(df3_t)

    # ------------------------------
    # plot graph
    path = "graph"
    x = df3_t.index
    y1 = df3_t[df3_t.columns[0]]
    y2 = df3_t[df3_t.columns[1]]
    y3 = df3_t[df3_t.columns[2]]
    y4 = df3_t[df3_t.columns[3]]
    y5 = df3_t[df3_t.columns[4]]

    # PLOT MULTIPLE LINES
    # add_trace: FOR MULTI-LINE  # mode="lines": SWITCH TO LINE CHART
    # LEGEND WILL SHOW WHEN MORE THAN 1 TRACE. COLOR IS AUTO GEN
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1, name=df3_t.columns[0], mode="lines"))
    fig.add_trace(go.Scatter(x=x, y=y2, name=df3_t.columns[1], mode="lines"))
    fig.add_trace(go.Scatter(x=x, y=y3, name=df3_t.columns[2], mode="lines"))
    fig.add_trace(go.Scatter(x=x, y=y4, name=df3_t.columns[3], mode="lines"))
    fig.add_trace(go.Scatter(x=x, y=y5, name=df3_t.columns[4], mode="lines"))


    fig.update_layout(title="Player IG Followers 7 Days Trend", xaxis_title="Player Name", yaxis_title="Date")

    # html file
    plotly.offline.plot(fig, filename=f'{path}\\info3_fake_{today}.html')


    end_program(start_time)
    os._exit(1)


# ----------------------------------------------------
# while True:
#     schedule.run_pending()
#     time.sleep(3)
#
#     schedule.every().day.at("10:30").do(main)


if __name__ == "__main__":
    main()