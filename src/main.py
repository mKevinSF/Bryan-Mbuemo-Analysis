import json
import os
import pandas as pd
from extract_fbref import extract_scouting_report
from transform_fbref import transform_player_data
from extract_understat import extract_understat_players
from transform_understat import transform_shots_understat
from load import combine_fbref, combine_understat

def load_config(path):
    with open(path, "r") as f:
        return json.load(f)["players"]

def run_fbref_pipeline():
    players = load_config("config/player_config_fbref.json")
    for player in players:
        slug = player["slug"]
        name = player["name"]
        scout_id = player["scout_id"]

        extract_scouting_report(slug, name, scout_id)
        transform_player_data(name)

    df_fbref = combine_fbref()
    if not df_fbref.empty:
        print("\n✅ FBref Data Combined:")
        print(df_fbref.groupby("player").mean(numeric_only=True))
    else:
        print("❌ No FBref data combined.")

def run_understat_pipeline():
    extract_understat_players("config/player_config_understat.json", force=False)

    df_understat = combine_understat()

    if df_understat.empty:
        print("❌ No Understat data combined.")
        return

    if "outcome" in df_understat.columns:
        outcome_col = "outcome"
    elif "result" in df_understat.columns:
        outcome_col = "result"
    else:
        print("⚠️ No 'outcome'/'result' column found. Columns:", df_understat.columns.tolist())
        return

    if "player" not in df_understat.columns:
        for alt in ["Player", "player_name", "name"]:
            if alt in df_understat.columns:
                df_understat = df_understat.rename(columns={alt: "player"})
                break
        if "player" not in df_understat.columns:
            print("⚠️ No player column found. Columns:", df_understat.columns.tolist())
            return

    outcome_counts = pd.crosstab(df_understat["player"], df_understat[outcome_col])
    outcome_counts = outcome_counts.sort_index()
    outcome_counts["TotalShots"] = outcome_counts.sum(axis=1)

    print("\n✅ Understat outcome counts (per player):\n")
    print(outcome_counts)

if __name__ == "__main__":
    os.makedirs("data/final", exist_ok=True)
    
    print("🚀 Running FBref Pipeline...")
    run_fbref_pipeline()

    print("\n🚀 Running Understat Pipeline...")
    run_understat_pipeline()
