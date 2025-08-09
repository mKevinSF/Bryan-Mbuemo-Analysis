import pandas as pd
import glob
import os
from utils import ensure_dir

RAW_DIR = "data/raw/understat"
PROCESSED_DIR = "data/processed/understat"

def transform_shots_understat():
    ensure_dir(PROCESSED_DIR)

    # Cari semua file shots.csv
    shots_files = glob.glob(os.path.join(RAW_DIR, "*_shots.csv"))

    for file_path in shots_files:
        # Ambil nama player dari filename
        player_name = os.path.basename(file_path).replace("_shots.csv", "").replace("_", " ").title()
        print(f"🔄 Processing {player_name} shots...")

        # Baca raw shots
        df = pd.read_csv(file_path)

        # Buang penalti
        df = df[df['situation'] != 'Penalty']

        # Ambil kolom penting saja
        df_processed = pd.DataFrame({
            "minute": df["minute"],
            "player": df["player"],
            "x": df["X"],
            "y": df["Y"],
            "xG": df["xG"],
            "outcome": df["result"]
        })

        # Simpan processed file
        out_path = os.path.join(PROCESSED_DIR, f"{player_name.lower().replace(' ', '_')}_shots_processed.csv")
        df_processed.to_csv(out_path, index=False)
        print(f"✅ Saved processed shot data → {out_path}")

if __name__ == "__main__":
    transform_shots_understat()
