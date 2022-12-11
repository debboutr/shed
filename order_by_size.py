"""
  ___  ____  ____  _____ ____      _____    ___ _   _ ____  _______  __
 / _ \|  _ \|  _ \| ____|  _ \    |__  /   |_ _| \ | |  _ \| ____\ \/ /
| | | | |_) | | | |  _| | |_) |____ / /_____| ||  \| | | | |  _|  \  /
| |_| |  _ <| |_| | |___|  _ <_____/ /|_____| || |\  | |_| | |___ /  \
 \___/|_| \_\____/|_____|_| \_\   /____|   |___|_| \_|____/|_____/_/\_\
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
