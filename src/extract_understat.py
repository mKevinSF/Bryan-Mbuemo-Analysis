import requests
import re
import json
import pandas as pd
import os
from utils import ensure_dir

BASE_URL = "https://understat.com/player"

def fetch_understat_player(player_id, target_season="2024"):
    """
    Ambil HTML Understat -> extract matchesData & shotsData -> parse JSON
    Filter hanya season 2024/2025
    """
    url = f"{BASE_URL}/{player_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to fetch Understat page for player_id={player_id}")
        return None

    html_text = response.text

    # Cari matchesData di dalam <script>
    matches_pattern = re.search(r"matchesData\s*=\s*JSON.parse\('([^']+)'\)", html_text)
    shots_pattern = re.search(r"shotsData\s*=\s*JSON.parse\('([^']+)'\)", html_text)

    matches = []
    shots = []

    if matches_pattern:
        matches_json = matches_pattern.group(1).encode('utf-8').decode('unicode_escape')
        matches = json.loads(matches_json)
        # Filter hanya season target
        matches = [m for m in matches if target_season in m["season"] or "2024/2025" in m["season"]]
    else:
        print("⚠️ matchesData not found in page!")

    if shots_pattern:
        shots_json = shots_pattern.group(1).encode('utf-8').decode('unicode_escape')
        shots = json.loads(shots_json)
        # Filter hanya season target
        shots = [s for s in shots if target_season in s["season"] or "2024/2025" in s["season"]]
    else:
        print("⚠️ shotsData not found in page!")

    return {"matches": matches, "shots": shots}


def save_understat_csv(player_name, data):
    """
    Simpan data matches & shots ke CSV
    """
    ensure_dir("data/raw/understat")

    if data["matches"]:
        matches_df = pd.DataFrame(data["matches"])
        matches_path = f"data/raw/understat/{player_name.lower().replace(' ', '_')}_matches.csv"
        matches_df.to_csv(matches_path, index=False)
        print(f"✅ Saved matches ({len(matches_df)}) to {matches_path}")
    else:
        print(f"⚠️ No matches found for {player_name} in 2024/2025")

    if data["shots"]:
        shots_df = pd.DataFrame(data["shots"])
        shots_path = f"data/raw/understat/{player_name.lower().replace(' ', '_')}_shots.csv"
        shots_df.to_csv(shots_path, index=False)
        print(f"✅ Saved shots ({len(shots_df)}) to {shots_path}")
    else:
        print(f"⚠️ No shots found for {player_name} in 2024/2025")


def extract_understat_players(config_path="config/player_config_understat.json", force=False):
    """
    Loop semua pemain dari config & ambil data mereka
    """
    with open(config_path, "r") as f:
        config = json.load(f)

    for player in config["players"]:
        player_id = player["understat_id"]
        player_name = player["name"]

        matches_path = f"data/raw/understat/{player_name.lower().replace(' ', '_')}_matches.csv"
        shots_path = f"data/raw/understat/{player_name.lower().replace(' ', '_')}_shots.csv"

        if not force and os.path.exists(matches_path) and os.path.exists(shots_path):
            print(f"🔁 Understat data already exists for {player_name}, skipping fetch.")
            continue

        data = fetch_understat_player(player_id, target_season="2024")
        if data:
            save_understat_csv(player_name, data)

if __name__ == "__main__":
    extract_understat_players(force=True)
