import os
import json
import pandas as pd
from pprint import pprint
from tqdm.auto import tqdm
from datetime import datetime

DATA_DIR = "./shc_data"
KML_DIR = "KML_files/states"
states = os.listdir(os.path.join(DATA_DIR, "KML_files/states"))
OUTPUT_DIR = "YEAR_WISE_DATA"

os.makedirs(os.path.join(DATA_DIR, OUTPUT_DIR), exist_ok=True)

years = ['2023', '2024']

for state in states:
    rows = {key: [] for key in years}
    
    districts = os.listdir(os.path.join(DATA_DIR,f"{KML_DIR}/{state}"))
    for district in districts:
        if district == "getDistricts.json":
            continue

        json_path = os.path.join(DATA_DIR, f"{KML_DIR}/{state}/{district}/features.json")
        if not os.path.exists(json_path):
            continue

        try:
            feature_info = json.load(open(json_path))

        except json.JSONDecodeError:
            print(f"Error reading {json_path}")
            continue

        for feature in feature_info:
            if feature["period"] in ["2023-24", "2024-25"]:

                if "date" not in feature["properties"].keys():
                    # print("No date found in the feature")
                    continue

                dt = feature["properties"]["date"]
                dt = datetime.strptime(dt, "%m/%d/%y, %I:%M %p")
                year = dt.year
                
                # district, village, date, lat, long, [N, P, K, B, Fe, Zn, Cu, S, OC, pH, Mn, EC]
                try:
                    row = {
                        "district": district,
                        "village": feature["properties"].get("village", ""),
                        "date": feature["properties"].get("date", ""),
                        "lat": feature["latitude"],
                        "long": feature["longitude"],
                        "N": feature["properties"].get("N", ""),
                        "P": feature["properties"].get("P", ""),
                        "K": feature["properties"].get("K", ""),
                        "B": feature["properties"].get("B", ""),
                        "Fe": feature["properties"].get("Fe", ""),
                        "Zn": feature["properties"].get("Zn", ""),
                        "Cu": feature["properties"].get("Cu", ""),
                        "S": feature["properties"].get("S", ""),
                        "OC": feature["properties"].get("OC", ""),
                        "pH": feature["properties"].get("pH", ""),
                        "Mn": feature["properties"].get("Mn", ""),
                        "EC": feature["properties"].get("EC", ""),
                    }
                except KeyError:
                    pprint(feature["properties"])

                if str(year) in years:
                    rows[str(year)].append(row)

    for year in years:
        df = pd.DataFrame(rows[year])
        SAVE_DIR = os.path.join(DATA_DIR, OUTPUT_DIR, year)
        os.makedirs(SAVE_DIR, exist_ok=True)
        df.to_csv(
            os.path.join(SAVE_DIR, f"{state}_{year}.csv"),
            index=False,
            encoding="utf-8",
        )
        print(f"Saved {state}_{year}.csv with {len(df)} records")

print("All states completed")
