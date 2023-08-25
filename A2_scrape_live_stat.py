import requests
import time
from datetime import datetime
import pandas as pd
import os
import json
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
    website = "https://allsportsapi.com/"
    APIkey = "e4949ca79cc5aa8e80e59eb434757073785d0cf025ab2dcec650b8775b47644e"
    url = f"https://apiv2.allsportsapi.com/basketball/?met=Livescore&APIkey={APIkey}"

    response = requests.get(url)
    print(response.json())

    # # league_name = "NBA"
    # league_name = "BBL"
    # if "league_name" == league_name:
    #     print(response.json())


def read_json():
    print("Since NBA is now off season, cannot scrape live data for demonstration.")
    print("Use the website provided json example as demonstration instead with 1 fake player stat info added")

    with open("allsportsapi.json", "r", encoding="utf-8") as i:
        data = json.load(i)

    event_date_list, league_name_list, home_team_list, away_team_list, home_score_list, away_score_list, win_list = [], [], [], [], [], [], []
    player_list, score_list, rebound_list, assist_list, steal_list, block_list = [], [], [], [], [], []

    for result in data["result"]:
        # print(result)

        # game general information
        event_date = result["event_date"]
        league_name = result["league_name"]
        home_team = result["event_home_team"]
        away_team = result["event_away_team"]
        final_result = result["event_final_result"]
        home_score = int(final_result.split(" ")[0])
        away_score = int(final_result.split(" ")[-1])
        win = ""
        if home_score > away_score:
            win = "home"
        elif away_score > home_score:
            win = "away"

        print(event_date, league_name, home_team, away_team, home_score, away_score, win)
        # print(player_statistics_H)  # list

        # home stat player info (same for away stat player if have)
        player_statistics_H = result["player_statistics"]["home_team"]
        # each player stat in dict
        for player_stat in player_statistics_H:
            player = player_stat.get("player")
            score = int(player_stat.get("player_points"))
            rebound = int(player_stat.get("player_total_rebounds"))
            assist = int(player_stat.get("player_assists"))
            steal = int(player_stat.get("player_steals"))
            block = int(player_stat.get("player_blocks"))

            print(player, score, rebound, assist, steal, block)

            event_date_list.append(event_date)
            league_name_list.append(league_name)
            home_team_list.append(home_team)
            away_team_list.append(away_team)
            home_score_list.append(home_score)
            away_score_list.append(away_score)
            win_list.append(win)
            player_list.append(player)
            score_list.append(score)
            rebound_list.append(rebound)
            assist_list.append(assist)
            steal_list.append(steal)
            block_list.append(block)

    return event_date_list, league_name_list, home_team_list, away_team_list, home_score_list, away_score_list, \
           win_list, player_list, score_list, rebound_list, assist_list, steal_list, block_list


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

    print("Scrape Live Score for Performance via All Sports API")

    # date info
    today = date_info()
    print(today)

    # open_browser()
    event_date_list, league_name_list, home_team_list, away_team_list, home_score_list, away_score_list, \
    win_list, player_list, score_list, rebound_list, assist_list, steal_list, block_list = read_json()

    # create date list match with df length
    date_list = [today]*len(event_date_list)

    # save data to file
    df_dict = {"record date": date_list, "event date": event_date_list, "league": league_name_list,
            "home team": home_team_list, "away team": away_team_list, "home score": home_score_list,
            "away score": away_score_list, "win team": win_list, "player name": player_list, "score": score_list,
            "rebound": rebound_list, "assist": assist_list, "steal": steal_list, "block": block_list}

    # save csv
    save_csv(filename=f"csv\\2_nba_player_stat_{today}.csv", dict=df_dict)
    # save h5file
    save_hdf(filename=f"h5\\2_nba_player_stat_{today}.h5", group_name="data", dict=df_dict)

    # # test print
    # print("TEST PRINT")
    # # read h5
    # hdf = pd.read_hdf(f"h5\\2_nba_player_stat_{today}.h5", 'data')
    # print(hdf)

    end_program(start_time)
    os._exit(1)


# ----------------------------------------------------
# while True:
#     schedule.run_pending()
#     time.sleep(3)
#
#     schedule.every().day.at("10:05").do(main)


if __name__ == "__main__":
    main()
