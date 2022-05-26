from itertools import combinations

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiPolygon


def find_overlaps(gdf):
    """Returns a list of tuples idntifying the geometries
    that overlap one another.
    """
    overlaps = []
    for x, y in combinations(gdf.index.tolist(), 2):
        x_geom = gdf.loc[x].geometry.exterior
        y_geom = gdf.loc[y].geometry.exterior
        if x_geom.crosses(y_geom):
            overlaps.append((x, y))
    return overlaps


def t_dict(d):
    """Creates a dictionary to pass to the GeoDataFrame instantiation 
    """
    g = {}
    for k in d:
        g[k] = [d[k]]
    return g


def clipGeoms(geom1, geom2):
    """Returns a clipped version of geom 2
    """
    return geom2.difference(geom1)


def mashGeoms(gdf, tup):
    """Modifies the overlapping geometries within the GeoDataFrame
    at the indexes passed into tup.
    """
    clip = gdf.loc[tup[1]]
    dc = t_dict(clip.drop("geometry").to_dict())
    a = gdf.loc[tup[0]].geometry
    b = clip.geometry
    tt1 = type(a) == type(MultiPolygon())
    tt2 = type(b) == type(MultiPolygon())
    if not tt1 and not tt2:
        clipd = clipGeoms(a, b)
    if not tt1 and tt2:
        polys = []
        for m in b:
            polys.append(clipGeoms(a, m))
        clipd = MultiPolygon(polys)
    if tt1 and not tt2:
        for n in a:
            b = clipGeoms(n, b)
        clipd = b
    if tt1 and tt2:
        polys = []
        for m in b:
            for n in a:
                m = clipGeoms(n, m)
            polys.append(m)
        clipd = MultiPolygon(polys)
    gdf.drop(tup[1], inplace=True)
    new = gpd.GeoDataFrame(dc, index=[tup[1]], geometry=[clipd], crs=gdf.crs)
    return pd.concat([gdf, new]).sort_index()


def fixOverlap(f, col):
    """Clips out overlapping geometries within a shapefile
    ranked by an attribute.
    """
    shp = gpd.read_file(f)
    shp.sort_values(by=col, axis=0, ascending=False, inplace=True)
    shp.reset_index(drop=True, inplace=True)
    iss = find_overlaps(shp)
    for x in iss:
        shp = mashGeoms(shp, x)
    return shp.reset_index(drop=True)


if __name__ == "__main__":

    loc = "."
    fn = "%s/circles.shp" % loc
    column = "WEIGHT"
    out = fixOverlap(fn, column)
    out.to_file("%s/test.shp" % loc)


# /home/rick/.miniconda3/envs/gis/lib/python3.10/site-packages/geopandas/io/file.py:362: FutureWarning: pandas.Int64Index is deprecated and will be removed from pandas in a future version. Use pandas.Index with the appropriate dtype instead.
#   pd.Int64Index,
