import pandas as pd
import os
from utils import load_config, ensure_dir

def load_combined_data(players):
    dfs = []
    for player in players:
        name = player["name"]
        file_path = f"data/processed/{name.lower().replace(' ', '_')}_processed.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df["player"] = name
            dfs.append(df)
        else:
            print(f"❌ Processed file not found: {file_path}")
    
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    players = load_config()
    df_all = load_combined_data(players)
    
    if not df_all.empty:
        # Urut alfabet berdasarkan nama pemain
        df_all = df_all.sort_values(by="player").reset_index(drop=True)
        
        # Tambah kolom 'index' manual
        df_all.insert(0, "index", range(len(df_all)))
        
        ensure_dir("data/final")
        df_all.to_csv("data/final/all_players_data.csv", index=False)  # jangan simpan index pandas
        
        print("✅ Combined data saved to data/final/all_players_data.csv (sorted by name + custom index)")
    else:
        print("❌ No processed data to combine.")

