import requests
import json
import os
from io import StringIO
from bs4 import BeautifulSoup
import pandas as pd
from utils import ensure_dir

def fetch_table(url, table_id=None):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch URL: {url}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    if table_id:
        table = soup.find("table", id=table_id)
    else:
        table = soup.find("table")

    if table is None:
        print(f"No table found at {url}")
        return None

    df = pd.read_html(StringIO(str(table)))[0]

    # Flatten multiindex if needed
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(-1)

    df = df.dropna(how="all")
    return df

def extract_scouting_report(slug, name, scout_id, force=False):
    file_path = f"data/raw/fbref/{name.lower().replace(' ', '_')}_scout.csv"
    if not force and os.path.exists(file_path):
        print(f"🔁 Scout data already exists for {name}, skipping fetch.")
        return pd.read_csv(file_path)
    
    scout_url = f"https://fbref.com/en/players/{slug}/scout/{scout_id}/{name.replace(' ', '-')}-Scouting-Report"
    response = requests.get(scout_url)
    if response.status_code != 200:
        print(f"❌ Failed to fetch scouting report for {name}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # Cari hanya div dengan id = 'div_scout_summary_AM'
    target_div = soup.find("div", id="div_scout_summary_AM")
    if not target_div:
        print(f"⚠️ No div_scout_summary_AM found for {name}")
        return None

    table = target_div.find("table")
    if not table:
        print(f"⚠️ No table inside div_scout_summary_AM for {name}")
        return None

    try:
        raw_df = pd.read_html(StringIO(str(table)), header=[0, 1])[0]
        raw_df.columns = raw_df.columns.get_level_values(1)  # ambil kolom bawah (nama metrik)
        raw_df = raw_df.dropna(how="all")
        raw_df["Table"] = "scout_summary_AM"
    except ValueError:
        print(f"⚠️ Failed to parse scout_summary_AM table for {name}")
        return None

    ensure_dir("data/raw")
    raw_df.to_csv(file_path, index=False)
    print(f"✅ Scouting data saved for {name}: {file_path}")
    return raw_df

def main(force=False):
    with open("config/player_config_fbref.json", "r") as f:
        data = json.load(f)

    for player in data["players"]:
        extract_scouting_report(
            player["slug"], player["name"], player["scout_id"], force=force
        )

if __name__ == "__main__":
    main(force=True)
