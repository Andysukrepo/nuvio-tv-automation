import json
import os
from datetime import datetime

INPUT_FILE = "nuvio_config.json"
OUTPUT_FILE = "nuvio_config_automated.json"

# --- PERSONAL TRACKING CONFIGURATION OVERLAYS ---
# Your master compressed configuration hash strings mapped directly to your slot sequence
TRAKT_MUMS_LIST = "aiolists-H4sIAAAAAAAAA7VYbVPbOBD-L_qcpJJsyy_fQhO4cDgpjSmYTqcjW3Is8EtOtglJh_9-I8dAIZTobkKGmYTdZ_fRvlhe6RegS_E3XwMPNGSx2tzL5T2RyZqtrVW-wZDflBD0gFyyaPgIrGE_kZz3lRD0QJ2z6IhTyWVQ3vICeICvT9PoJBYzcTq52EzQVJy6AyVkl-dKmF6fXNxP83Nzdnlh-PnE8IPQmo6ymzD4ms-C8SrE12l4c5TO5pNqklviWkyIH8RwOlpsZqPz9XRuWn5wu_JHw_uzz6cbdjkRMzHBs9Fw5V-G97NgsQk319k0CI1ww25nwbfb6clYKGyI3dX1lS9mWSXCq6PllXGahZfn4mq-Eiz_to5xdhcpvis4uD8-7Qd-fJcH5CyZXMGTaFRYV8efb7J_8GyTXv8VJGXCT47n6UWXiDmvKlEWEwY8YLlOQm0TRg6LbJogYqDEcanNE24bpgsJxsghdtyZDuO4bIpamRJiugZ2tvKLisuC5hx44IZGEZcIYQx6IOc1ZbSm87KRsdLGouBK2Pk7o8WioQulURJJb-thHPOq6spUNFnWyb_yRPIq3VWM75dC8mpYv5D-tiJasHUUx80t6IFMVPVMMi6B9x1QUar_qz5CyDGs_hj0Xsps8kpmmdBEL2UrWsep-tm_7IL6-SR6FCT0rpSi5hX40QMZreqLJaM1VwXAEJM-dPrYDBD2sOEZ1sAyrOturZXfZRB4v97m9H6BlFZ-eSd4BbyEZhXvKck8LVcV8GrZ8C3n55THt-9zPvTeyMlHErQJ_jACgl2D9M9eEWz9PfvvCN8iMPvYDpDlWYaH4QA6xi6Bbe4Q_IcI9hIYELqHJ3jVpXu8v58gFEDbU3_GAFv2s_vnnj-Ue8NAO-khGB2-wO0G8rOWvGCiWPystm4OUwJMHPVscylLeczrOBXFonO3y5x3bIcJDxN3L_WyXDYZlQeO2cZ7if_Uja-j1ee0tIM9cJptey_zDU-Sql_f9Q-aZ8sge5kjXqcfwby_qxllH0Bs7yfOm_zwxATCvcSSx2We84LRWpRFdeA-c_7HCg6YAjRw8Xvttjs0HfQ9_9ADqWCMF2eKBHjff_SA5Hl5x9mj5O156UcPxE1Vl7mCTWneFuRBjapy8WSrBFuUz5mgwXrJf4OKfFnKmrMhY2XRyapS1l8kT7jkRbwtsgEdW30rFfAA4wltMjUTltsBFNAqVq8bA9tIC0ccrIPDFnZNPaCFtVZo2tjVolZASwdomwQTHaBDbEsrOwqotUYFNHSBWsEooHYwWglXQEcX6GoCiW4eiWYeXUOrzRyXmHpRu8TUCgZBBxGohWxPMbpIW6uKCNuupRV5i9Rjxw7UexZbpFZvtEi9fGIH6tWyRWpHZGhHZOpVUyG1urhFaj3lLVI7dr1GbpHaNdLseexASztLevsRwg7W2xVapF6WDIj0NmJkYtvVi90kSLOapmvpvYGQBU2oF1F7j6CLtDV9qpO9JpJgrRq9OELtA79x6upMalFn_E8Gu8cHHaud0V_HaGds1zHaPVi9Z_XQA0xUNMr4CS8kPxZZrZTdaMoLpflKC7YdFo85rRvJn_Sy1fijI6V8vG9sB09FXoucm4iAHlhQuY4lXSWlZIu4vdgraLVspChEBXogZe2UqibTilMZp9vb0tbT7_elKsDuRlFhtwPr_LXFo5oWIudb7bgNhD0tfHtB2gg1YceRibgVkRjGlhlZECKCMIoQNGOYGAaLEsOOYqYuc5tlVdMqvZAZ8EBa18vK-_SpadPXl2WzSNd9BG1iGYMOORDls9njxfvifLj90PnxcDhZxKMJDvNz0x-lN7NRiP1gAcNNbIX5NPc3Y8M_Ga9ml9MszMeGvwAP_wLn6N5KDhgAAA-B"
TRAKT_DADS_LIST = "aiolists-H4sIAAAAAAAAA7VYbVPbOBD-L_qcpJJsyy_fQhO4cDgpjSmYTqcjW3Is8EtOtglJh_9-I8dAIZTobkKGmYTdZ_fRvlhe6RegS_E3XwMPNGSx2tzL5T2RyZqtrVW-wZDflBD0gFyyaPgIrGE_kZz3lRD0QJ2z6IhTyWVQ3vICeICvT9PoJBYzcTq52EzQVJy6AyVkl-dKmF6fXNxP83Nzdnlh-PnE8IPQmo6ymzD4ms-C8SrE12l4c5TO5pNqklviWkyIH8RwOlpsZqPz9XRuWn5wu_JHw_uzz6cbdjkRMzHBs9Fw5V-G97NgsQk319k0CI1ww25nwbfb6clYKGyI3dX1lS9mWSXCq6PllXGahZfn4mq-Eiz_to5xdhcpvis4uD8-7Qd-fJcH5CyZXMGTaFRYV8efb7J_8GyTXv8VJGXCT47n6UWXiDmvKlEWEwY8YLlOQm0TRg6LbJogYqDEcanNE24bpgsJxsghdtyZDuO4bIpamRJiugZ2tvKLisuC5hx44IZGEZcIYQx6IOc1ZbSm87KRsdLGouBK2Pk7o8WioQulURJJb-thHPOq6spUNFnWyb_yRPIq3VWM75dC8mpYv5D-tiJasHUUx80t6IFMVPVMMi6B9x1QUar_qz5CyDGs_hj0Xsps8kpmmdBEL2UrWsep-tm_7IL6-SR6FCT0rpSi5hX40QMZreqLJaM1VwXAEJM-dPrYDBD2sOEZ1sAyrOturZXfZRB4v97m9H6BlFZ-eSd4BbyEZhXvKck8LVcV8GrZ8C3n55THt-9zPvTeyMlHErQJ_jACgl2D9M9eEWz9PfvvCN8iMPvYDpDlWYaH4QA6xi6Bbe4Q_IcI9hIYELqHJ3jVpXu8v58gFEDbU3_GAFv2s_vnnj-Ue8NAO-khGB2-wO0G8rOWvGCiWPystm4OUwJMHPVscylLeczrOBXFonO3y5x3bIcJDxN3L_WyXDYZlQeO2cZ7if_Uja-j1ee0tIM9cJptey_zDU-Sql_f9Q-aZ8sge5kjXqcfwby_qxllH0Bs7yfOm_zwxATCvcSSx2We84LRWpRFdeA-c_7HCg6YAjRw8Xvttjs0HfQ9_9ADqWCMF2eKBHjff_SA5Hl5x9mj5O156UcPxE1Vl7mCTWneFuRBjapy8WSrBFuUz5mgwXrJf4OKfFnKmrMhY2XRyapS1l8kT7jkRbwtsgEdW30rFfAA4wltMjUTltsBFNAqVq8bA9tIC0ccrIPDFnZNPaCFtVZo2tjVolZASwdomwQTHaBDbEsrOwqotUYFNHSBWsEooHYwWglXQEcX6GoCiW4eiWYeXUOrzRyXmHpRu8TUCgZBBxGohWxPMbpIW6uKCNuupRV5i9Rjxw7UexZbpFZvtEi9fGIH6tWyRWpHZGhHZOpVUyG1urhFaj3lLVI7dr1GbpHaNdLseexASztLevsRwg7W2xVapF6WDIj0NmJkYtvVi90kSLOapmvpvYGQBU2oF1F7j6CLtDV9qpO9JpJgrRq9OELtA79x6upMalFn_E8Gu8cHHaud0V_HaGds1zHaPVi9Z_XQA0xUNMr4CS8kPxZZrZTdaMoLpflKC7YdFo85rRvJn_Sy1fijI6V8vG9sB09FXoucm4iAHlhQuY4lXSWlZIu4vdgraLVspChEBXogZe2UqibTilMZp9vb0tbT7_elKsDuRlFhtwPr_LXFo5oWIudb7bgNhD0tfHtB2gg1YceRibgVkRjGlhlZECKCMIoQNGOYGAaLEsOOYqYuc5tlVdMqvZAZ8EBa18vK-_SpadPXl2WzSNd9BG1iGYMOORDls9njxfvifLj90PnxcDhZxKMJDvNz0x-lN7NRiP1gAcNNbIX5NPc3Y8M_Ga9ml9MszMeGvwAP_wLn6Y5KDhgAAA-A"
TRAKT_BETHS_LIST = "aiolists-H4sIAAAAAAAAA7VYbVPbOBD-L_qcpJJsyy_fQhO4cDgpjSmYTqcjW3Is8EtOtglJh_9-I8dAIZTobkKGmYTdZ_fRvlhe6RegS_E3XwMPNGSx2tzL5T2RyZqtrVW-wZDflBD0gFyyaPgIrGE_kZz3lRD0QJ2z6IhTyWVQ3vICeICvT9PoJBYzcTq52EzQVJy6AyVkl-dKmF6fXNxP83Nzdnlh-PnE8IPQmo6ymzD4ms-C8SrE12l4c5TO5pNqklviWkyIH8RwOlpsZqPz9XRuWn5wu_JHw_uzz6cbdjkRMzHBs9Fw5V-G97NgsQk319k0CI1ww25nwbfb6clYKGyI3dX1lS9mWSXCq6PllXGahZfn4mq-Eiz_to5xdhcpvis4uD8-7Qd-fJcH5CyZXMGTaFRYV8efb7J_8GyTXv8VJGXCT47n6UWXiDmvKlEWEwY8YLlOQm0TRg6LbJogYqDEcanNE24bpgsJxsghdtyZDuO4bIpamRJiugZ2tvKLisuC5hx44IZGEZcIYQx6IOc1ZbSm87KRsdLGouBK2Pk7o8WioQulURJJb-thHPOq6spUNFnWyb_yRPIq3VWM75dC8mpYv5D-tiJasHUUx80t6IFMVPVMMi6B9x1QUar_qz5CyDGs_hj0Xsps8kpmmdBEL2UrWsep-tm_7IL6-SR6FCT0rpSi5hX40QMZreqLJaM1VwXAEJM-dPrYDBD2sOEZ1sAyrOturZXfZRB4v97m9H6BlFZ-eSd4BbyEZhXvKck8LVcV8GrZ8C3n55THt-9zPvTeyMlHErQJ_jACgl2D9M9eEWz9PfvvCN8iMPvYDpDlWYaH4QA6xi6Bbe4Q_IcI9hIYELqHJ3jVpXu8v58gFEDbU3_GAFv2s_vnnj-Ue8NAO-khGB2-wO0G8rOWvGCiWPystm4OUwJMHPVscylLeczrOBXFonO3y5x3bIcJDxN3L_WyXDYZlQeO2cZ7if_Uja-j1ee0tIM9cJptey_zDU-Sql_f9Q-aZ8sge5kjXqcfwby_qxllH0Bs7yfOm_zwxATCvcSSx2We84LRWpRFdeA-c_7HCg6YAjRw8Xvttjs0HfQ9_9ADqWCMF2eKBHjff_SA5Hl5x9mj5O156UcPxE1Vl7mCTWneFuRBjapy8WSrBFuUz5mgwXrJf4OKfFnKmrMhY2XRyapS1l8kT7jkRbwtsgEdW30rFfAA4wltMjUTltsBFNAqVq8bA9tIC0ccrIPDFnZNPaCFtVZo2tjVolZASwdomwQTHaBDbEsrOwqotUYFNHSBWsEooHYwWglXQEcX6GoCiW4eiWYeXUOrzRyXmHpRu8TUCgZBBxGohWxPMbpIW6uKCNuupRV5i9Rjxw7UexZbpFZvtEi9fGIH6tWyRWpHZGhHZOpVUyG1urhFaj3lLVI7dr1GbpHaNdLseexASztLevsRwg7W2xVapF6WDIj0NmJkYtvVi90kSLOapmvpvYGQBU2oF1F7j6CLtDV9qpO9JpJgrRq9OELtA79x6upMalFn_E8Gu8cHHaud0V_HaGds1zHaPVi9Z_XQA0xUNMr4CS8kPxZZrZTdaMoLpflKC7YdFo85rRvJn_Sy1fijI6V8vG9sB09FXoucm4iAHlhQuY4lXSWlZIu4vdgraLVspChEBXogZe2UqibTilMZp9vb0tbT7_elKsDuRlFhtwPr_LXFo5oWIudb7bgNhD0tfHtB2gg1YceRibgVkRjGlhlZECKCMIoQNGOYGAaLEsOOYqYuc5tlVdMqvZAZ8EBa18vK-_SpadPXl2WzSNd9BG1iGYMOORDls9njxfvifLj90PnxcDhZxKMJDvNz0x-lN7NRiP1gAcNNbIX5NPc3Y8M_Ga9ml9MszMeGvwAP_wLn6N5KDhgAAA-B"

# Your standard MdbList parameters remain safe right below
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
                    
        # --- 2. AUTOMATION MODULE: TRAKT DYNAMIC HASH INJECTIONS ---
        elif "Our Shows" in title:
            print(" -> Injecting live compressed AIO tracking hashes into profile nodes...")
            for folder in folders:
                folder_title = folder.get("title", "").lower()
                sources = folder.get("sources", [])
                cat_sources = folder.get("catalogSources", [])
                
                # Match folders to target live server configuration overrides
                target_hash = None
                if "mum" in folder_title:
                    target_hash = TRAKT_MUMS_LIST
                elif "dad" in folder_title:
                    target_hash = TRAKT_DADS_LIST
                elif "beth" in folder_title:
                    target_hash = TRAKT_BETHS_LIST
                
                if target_hash:
                    print(f"   -> Overwriting tracking strings for loop folder: {folder.get('title')}")
                    for src in sources + cat_sources:
                        if src.get("addonId") == "org.stremio.aiolists":
                            src["catalogId"] = target_hash
                    
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

        # --- 3. AUTOMATION MODULE: TRAKT/MDBLIST AUTOMATED SYNC MODIFICATIONS ---
        # If you have specific external tracker lists to swap out dynamically, 
        # you can target individual rows here using code logic filters.
        elif "Awards & Festivals" in title:
            print(" -> Verifying automated track feeds for Awards collection...")
            # Code parameters can check and update active catalog tracking IDs here

    # Save the finalized, fully-optimized configurations out to your workspace disk
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"\n[SUCCESS] Custom files updated and written to disk: '{OUTPUT_FILE}'")

if __name__ == "__main__":
    run_advanced_automation()
