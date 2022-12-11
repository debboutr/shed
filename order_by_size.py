import geopandas as gpd

# if col in columns:
#     exit
len([f"{x}{y}" for x, y in combinations("ABCDEFGHIJKLMNOPQRSTUVVWXYZ", 2)])

gg = gpd.read_file("/home/rick/gisjunk/ws_0809.gpkg")

uid = "SITE_ID"

ff = gg.iloc[:1000].copy()
gg = ff.copy()

# simpler geometry...easier compute
gg.geometry = gg.geometry.convex_hull

# find polys that intersect one another
# there will always be a match on itself
laid = gg.overlay(gg, how="intersection")

# retain the rows that are independent
keep = laid.loc[laid[f"{uid}_1"] == laid[f"{uid}_2"]][f"{uid}_1"]

# filter out the ones that are duplicates of themselves
diff = laid.loc[laid[f"{uid}_1"] != laid[f"{uid}_2"]].copy()

diff["g_area"] = diff.geometry.area * 1e-6
diff.sort_values("g_area", ascending=False, inplace=True)
diff["check_string"] = diff.apply(
    lambda x: "".join(sorted([x[f"{uid}_1"], x[f"{uid}_2"]])), axis=1
)
diff.drop_duplicates("check_string", inplace=True)

diff.groupby(f"{uid}_1", sort=False).size().max()
diff.groupby(f"{uid}_2").size().max()
# TODO groupby poly to assign values
# start with the smallest...decrement value for each group by one

# start with the largest

diff.groupby(f"{uid}_1").first()

diff[["SITE_ID_1", "SITE_ID_2", "g_area"]].head()
# sort=False will retain the sort_values order used above
diff.groupby(f"{uid}_1", sort=False).size()
diff.groupby(f"{uid}_2", sort=False).size()
# what do I have...a GDF that holds all of the polygons that intersect one
# another. If I start with the biggest I can look at the area in each group
diff.groupby(f"{uid}_1", sort=False).first()

"FW08LA182" in diff.groupby(f"{uid}_1", sort=False).groups.keys()


for name, grp in diff.groupby(f"{uid}_1", sort=False):
    print(grp[["SITE_ID_1", "SITE_ID_2", "g_area"]])
    ff = gg.loc[gg[f"{uid}"].isin(grp[f"{uid}_2"])]
    check = ff.overlay(ff, how="intersection")
    break
    check["g_area"] = check.geometry.area * 1e-6
    check.sort_values("g_area", ascending=False, inplace=True)
    check["check_string"] = check.apply(
        lambda x: "".join(sorted([x[f"{uid}_1"], x[f"{uid}_2"]])), axis=1
    )
    check.drop_duplicates("check_string", inplace=True)
    check.groupby(f"{uid}_1", sort=False).size().max()

    check10.groupby(f"{uid}_1", sort=False).size().max()

trite = {}
# subsetting, take out the largest and drill down, seems recursive
hold = True
while hold:
    print(len(check10))
    for ix, (name, grp) in enumerate(check19.groupby(f"{uid}_1", sort=False)):
        pp = gg.loc[gg[f"{uid}"].isin(grp[f"{uid}_2"])]
        check10 = pp.overlay(pp, how="intersection")
        check10["g_area"] = check10.geometry.area * 1e-6
        check10.sort_values("g_area", ascending=False, inplace=True)
        check10["check_string"] = check10.apply(
            lambda x: "".join(sorted([x[f"{uid}_1"], x[f"{uid}_2"]])), axis=1
        )
        check19 = check10.drop_duplicates("check_string")
        hold = len(check19) != 1
        print(f"{name}: ", len(check19))
        break

        check10.groupby(f"{uid}_1", sort=False).size().max()

"""
--add ID uniq
**LOOP
    --find count of intersecting..apply()
    --sort by that field
    --apply lowest value to zeros
    --slice(intersected->1)
    --run overlay=intersect
    --when resulting cols flipped, apply 0 to one 1 to the other
    --slice out all that have been found so far
    start with 1 on the next loop ++ to 2 ... and, so on.
**LOOP
"""


order = {}
num = 0


def get_intersect(x, uid=uid):
    item = gg.loc[gg.rowid == x[uid]]
    others = gg.loc[gg.rowid != x[uid]]
    yy = item.overlay(others, how="intersection")
    return len(yy)


order = {}
num = 0
# START HERE...get number of intersecting polys
gg["intersect"] = gg.apply(get_intersect, axis=1)
"""
** Below done with groupby **
--zeros go directly into level one continue
--check ones against themselves and throw the larger ones in w/ zeros
--add remaining to level +1
--sort by area and 
--increment num

AGAIN
-- find intersect + isolate zeros to max -> 4_000_000 <- use intersect.unique to find
-- order by AREA desc
-- set val of largest to 0 | isolate | overlay with rest
-- find intersect again |
"""
gg["rowid"].is_unique
gg["intersect"].min()
gg["intersect"].isnull().sum()
gg.loc[gg["intersect"] < 2]
# remove zeros
zeros = gg.loc[gg["intersect"] == 0]
z_list = zeros["rowid"].tolist()

ones = gg.loc[gg["intersect"] == 1]
# overlay with itself to find polys that can be cancelled out in this iteration
ovr = ones.overlay(ones, how="intersection")
# remove identities
ovr = ovr.loc[ovr[f"{uid}_1"] != ovr[f"{uid}_2"]]
ovr[f"{uid}_1"].is_unique
ovr[f"{uid}_2"].is_unique
catch = []

"""We need to run the apply here again! not what I'm doing!"""


ovr[["intersect", "intersect_1", "intersect_2"]]
ovr[["rowid_1", "rowid_2"]]


ovr["check_string"] = ovr.apply(
    lambda x: "".join(sorted([str(x[f"{uid}_1"]), str(x[f"{uid}_2"])])), axis=1
)
check19 = ovr.drop_duplicates("check_string")


gg.loc[gg.rowid != 1]

# gg.columns.tolist()

gg = gpd.read_file("/home/rick/gisjunk/ws_0809.gpkg")
gg["area"] = gg.geometry.area
gg = gg.sort_values("area", ascending=False).reset_index(names="work")
gg = gg[["work", "area", "geometry"]]
gg["order"] = 0
hh = gg.copy()
for row in gg.itertuples():
    print(row.Index)
    gg.drop(row.Index, inplace=True)
    touched = gg.intersects(row.geometry)
    if touched.any():
        selected = gg.loc[touched, "work"]
        hh.loc[hh["work"].isin(selected), "order"] += 1

    break
