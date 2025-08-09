import pandas as pd
from utils import ensure_dir

def transform_player_data(name):
    file_path = f"data/raw/fbref/{name.lower().replace(' ', '_')}_scout.csv"
    print(f"Reading from: {file_path}")

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"[ERROR] No raw file found for {name}")
        return None

    # Filter scout_summary_AM saja
    df = df[df["Table"] == "scout_summary_AM"].copy()

    # Bersihkan Per 90 dan Percentile → numeric
    df["Per 90"] = df["Per 90"].astype(str).str.replace('%', '', regex=False)
    df["Per 90"] = pd.to_numeric(df["Per 90"], errors="coerce")
    df["Percentile"] = pd.to_numeric(df["Percentile"], errors="coerce")

    # --- Gabung per statistic ---
    merged_dict = {"player": name}
    for _, row in df.iterrows():
        stat = row["Statistic"]

        per90_val = row["Per 90"]
        pct_val = row["Percentile"]

        merged_dict[f"{stat}_p90"] = per90_val
        merged_dict[f"{stat}_pct"] = pct_val

    # Ubah ke DataFrame 1 baris
    merged_df = pd.DataFrame([merged_dict])

    # Simpan processed
    ensure_dir("data/processed")
    out_path = f"data/processed/fbref/{name.lower().replace(' ', '_')}_processed.csv"
    merged_df.to_csv(out_path, index=False)
    print(f"[SUCCESS] Saved merged data: {out_path}")

    return merged_df

if __name__ == "__main__":
    player_list = ["Alejandro Garnacho", "Amad Diallo", "Bryan Mbeumo", "Marcus Rashford"]
    for player in player_list:
        transform_player_data(player)
