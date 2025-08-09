import json
import os

def load_config(config_path="config/player_config.json", key="players"):
    """
    Load JSON config file.
    
    Args:
        config_path (str): path ke config JSON
        key (str): key utama di dalam JSON (default "players")

    Returns:
        list[dict]: daftar pemain dengan atribut masing-masing
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"❌ Config file not found: {config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    if key not in config:
        raise KeyError(f"⚠️ Key '{key}' not found in {config_path}. Available keys: {list(config.keys())}")
    
    return config[key]


def ensure_dir(directory):
    """
    Pastikan folder ada, kalau belum otomatis dibuat.
    """
    os.makedirs(directory, exist_ok=True)
    return directory


def get_player_filename(name, suffix="_scout.csv", subfolder="data/raw/fbref"):
    """
    Generate filename yang rapi berdasarkan nama pemain.

    Example:
        name="Bryan Mbeumo"
        -> "data/raw/fbref/bryan_mbeumo_scout.csv"

    Bisa dipakai untuk FBRef & Understat (ubah subfolder & suffix)
    """
    clean_name = name.lower().replace(" ", "_")
    return os.path.join(subfolder, f"{clean_name}{suffix}")
