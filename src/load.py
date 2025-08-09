import pandas as pd
import os
import json

def load_config_fbref():
    with open("config/player_config_fbref.json", "r") as f:
        return json.load(f)["players"]

def load_config_understat():
    with open("config/player_config_understat.json", "r") as f:
        return json.load(f)["players"]

def combine_fbref():
    dfs = []
    for player in load_config_fbref():
        name = player["name"]
        file_path = f"data/processed/fbref/{name.lower().replace(' ', '_')}_processed.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df["player"] = name
            dfs.append(df)
        else:
            print(f"❌ FBref file not found: {file_path}")
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def combine_understat():
    dfs = []
    for player in load_config_understat():
        name = player["name"]
        file_path = f"data/processed/understat/{name.lower().replace(' ', '_')}_shots_processed.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df["player"] = name
            dfs.append(df)
        else:
            print(f"❌ Understat file not found: {file_path}")
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

if __name__ == "__main__":
    os.makedirs("data/final", exist_ok=True)

    df_fbref = combine_fbref()
    if not df_fbref.empty:
        df_fbref = df_fbref.sort_values(by="player").reset_index(drop=True)
        df_fbref.insert(0, "index", range(len(df_fbref)))
        df_fbref.to_csv("data/final/all_players_fbref.csv", index=False)
        print("✅ FBref combined saved to data/final/all_players_fbref.csv")
    else:
        print("❌ No FBref data to combine.")

    df_understat = combine_understat()
    if not df_understat.empty:
        df_understat = df_understat.sort_values(by="player").reset_index(drop=True)
        df_understat.insert(0, "index", range(len(df_understat)))
        df_understat.to_csv("data/final/all_players_understat.csv", index=False)
        print("✅ Understat combined saved to data/final/all_players_understat.csv")
    else:
        print("❌ No Understat data to combine.")
