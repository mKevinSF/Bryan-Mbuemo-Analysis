from utils import load_config
from extract_fbref import extract_scouting_report
from transform_fbref import transform_player_data
from load import load_combined_data

def main():
    players = load_config()

    # ETL Pipeline
    for player in players:
        slug = player["slug"]
        name = player["name"]
        scout_id = player["scout_id"]

        extract_scouting_report(slug, name, scout_id)
        transform_player_data(name)
    
    # Load All Data
    df_all = load_combined_data(players)

    if not df_all.empty:
        print("\nCombined Player Stats:")
        print(df_all.groupby("player")[["per_90", "percentile"]].mean())
    else:
        print("No data loaded.")

if __name__ == "__main__":
    main()
