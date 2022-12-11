"""
__  _______ ____  _   _ ___     _____     ____  _____ ____  ____   ___  
\ \/ / ____|  _ \| \ | |_ _|   |__  /    |  _ \| ____|  _ \|  _ \ / _ \ 
 \  /|  _| | | | |  \| || |_____ / /_____| |_) |  _| | | | | |_) | | | |
 /  \| |___| |_| | |\  || |_____/ /|_____|  _ <| |___| |_| |  _ <| |_| |
/_/\_\_____|____/|_| \_|___|   /____|    |_| \_\_____|____/|_| \_\\___/ 
                                                                        
"""

"""

-- make into click package / composable into the whole repo | gis_tools
-- parameters for desired output
-- check col names for added data | only needed if output file is being
    appended
-- also make the function importable as python package
-- docstrings
"""

import click
import geopandas as gpd

# if col in columns:
#     exit
gdf = gpd.read_file("/home/rick/gisjunk/ws_0809.gpkg")

gdf["area"] = gdf.geometry.area
gdf = gdf.sort_values("area", ascending=False).reset_index(names="work")
gdf = gdf[["work", "area", "geometry"]]
gdf["order"] = 0
upadate = gdf.copy()
for row in gdf.itertuples():
    print(row.Index)
    gdf.drop(row.Index, inplace=True)
    touched = gdf.intersects(row.geometry)
    if touched.any():
        selected = gdf.loc[touched, "work"]
        upadate.loc[update["work"].isin(selected), "order"] += 1
"""
               _                        _           _           
  ___  _ __ __| | ___ _ __     ____    (_)_ __   __| | _____  __
 / _ \| '__/ _` |/ _ \ '__|___|_  /____| | '_ \ / _` |/ _ \ \/ /
| (_) | | | (_| |  __/ | |_____/ /_____| | | | | (_| |  __/>  < 
 \___/|_|  \__,_|\___|_|      /___|    |_|_| |_|\__,_|\___/_/\_\
"""
