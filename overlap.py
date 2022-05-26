from itertools import combinations

import geopandas as gpd
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
    greater, lesser = tup
    clip = gdf.loc[lesser]
    # dc = t_dict(clip.drop("geometry").to_dict())
    a = gdf.loc[greater].geometry
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
    gdf.loc[lesser, 'geometry'] = clipd


def fixOverlap(f, col):
    """Clips out overlapping geometries within a shapefile
    ranked by an attribute.
    """
    shp = gpd.read_file(f)
    shp.sort_values(by=col, axis=0, ascending=False, inplace=True)
    shp.reset_index(drop=True, inplace=True)
    overlaps = find_overlaps(shp)
    for overlap in overlaps:
        mashGeoms(shp, overlap)
    return shp


if __name__ == "__main__":

    loc = "/home/rick/dev/overlapTopoTool"
    fn = f"{loc}/circles.shp"
    column = "WEIGHT"
    out = fixOverlap(fn, column)
    out.to_file(f"{loc}/test.shp")
