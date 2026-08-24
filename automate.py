import json
import os
from datetime import datetime

INPUT_FILE = "nuvio_config.json"
OUTPUT_FILE = "nuvio_config_automated.json"

# --- PERSONAL TRACKING CONFIGURATION OVERLAYS ---
# Swapping layout parameters with your precise MdbList direct numerical IDs
TRAKT_MUMS_LIST = "mdblist.ext_111876"
TRAKT_DADS_LIST = "mdblist.ext_111835"
TRAKT_BETHS_LIST = "mdblist.ext_154041"

# Keep your standard trending rows running safely underneath
MDBLIST_TRENDING_MOVIES = "mdblist.13914" 
MDBLIST_TRENDING_SERIES = "mdblist.13963"


def run_advanced_automation():
    print("Initializing Cloud Automation Sync Engine...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"\n[ERROR] Missing File: Could not find '{INPUT_FILE}' in repository.")
        return

    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"\n[ERROR] Formatting Issue: Could not read your JSON data: {e}")
        return

    # Fetch current calendar tracking variables dynamically
    current_month = datetime.now().month
    print(f"File loaded perfectly! Processing calendar rules for month index: {current_month}")

    for collection in data:
        title = collection.get("title", "").strip()
        folders = collection.get("folders", [])
        
        # --- 1. AUTOMATION MODULE: HOLIDAY SPECIALS SEASONAL SORTING ---
        if "Holiday Specials" in title:
            print(" -> Processing Holiday Specials seasonal priority queue...")
            seasonal_priority = {
                10: "Halloween",
                11: "Thanksgiving",
                12: "Christmas",
                2: "Valentine's Day",
                3: "St. Patrick's Day"
            }
            
            target_folder_name = seasonal_priority.get(current_month)
            if target_folder_name:
                target_idx = next((i for i, f in enumerate(folders) if f.get("title") == target_folder_name), None)
                if target_idx is not None:
                    print(f"   -> Active season detected! Shifting '{target_folder_name}' to slot position 1.")
                    active_folder = folders.pop(target_idx)
                    folders.insert(0, active_folder)
                    
        # --- 2. AUTOMATION MODULE: TRAKT DYNAMIC INJECTIONS ---
        elif "Our Shows" in title:
            print(" -> Injecting live tracking paths into profile nodes...")
            for folder in folders:
                folder_title = folder.get("title", "").lower()
                sources = folder.get("sources", [])
                cat_sources = folder.get("catalogSources", [])
                
                # Match folders to target live server configurations
                target_id = None
                if "mum" in folder_title:
                    target_id = TRAKT_MUMS_LIST
                elif "dad" in folder_title:
                    target_id = TRAKT_DADS_LIST
                elif "beth" in folder_title:
                    target_id = TRAKT_BETHS_LIST
                
                if target_id:
                    print(f"   -> Updating tracking strings for loop folder: {folder.get('title')}")
                    for src in sources + cat_sources:
                        if src.get("addonId") == "org.stremio.aiolists":
                            src["catalogId"] = target_id
                    
        # --- 3. AUTOMATION MODULE: STREAMING PLATFORM VERIFICATION ---
        elif "Streaming Platforms" in title:
            has_peacock = any(f.get("title") == "Peacock" for f in folders)
            if not has_peacock:
                print(" -> Appending missing dynamic Peacock platform node.")
                folders.append({
                    "id": "folder-983a0505",
                    "title": "Peacock",
                    "sources": [{"type": "All Movies on Peacock", "genre": "", "addonId": "aio-metadata", "provider": "addon", "catalogId": "streaming.pcp_movie"}],
                    "hideTitle": True,
                    "tileShape": "LANDSCAPE",
                    "titleLogoUrl": "https://r2.dev",
                    "coverImageUrl": "https://r2.dev",
                    "catalogSources": [{"type": "All Movies on Peacock", "genre": "", "addonId": "aio-metadata", "catalogId": "streaming.pcp_movie"}],
                    "focusGifEnabled": False,
                    "heroBackdropUrl": "https://r2.dev"
                })

    # Save the finalized configurations out to your disk
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"\n[SUCCESS] Custom files updated and written to disk: '{OUTPUT_FILE}'")

if __name__ == "__main__":
    run_advanced_automation()
    
