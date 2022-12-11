from itertools import combinations

import geopandas as gpd
from shapely.geometry import MultiPolygon

MP = type(MultiPolygon())


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


def clipGeoms(geom1, geom2):
    """Returns a clipped version of geom2"""
    return geom2.difference(geom1)


def clip_geometries(hi_geom, lo_geom):
    """clips the `lo_geom` to the `hi-geom` and handles Multipolygon
    issues. Returns the updated geometry for `lo_geom`.
    """
    if not type(hi_geom) == MP and not type(lo_geom) == MP:
        return clipGeoms(hi_geom, lo_geom)
    if not type(hi_geom) == MP and type(lo_geom) == MP:
        polys = []
        for g in lo_geom:
            polys.append(clipGeoms(hi_geom, g))
        return MultiPolygon(polys)
    if type(hi_geom) == MP and not type(lo_geom) == MP:
        # clip by every geometry in the MultiPolygon
        for g in hi_geom:
            lo_geom = clipGeoms(g, lo_geom)
        return lo_geom
    if type(hi_geom) == MP and type(lo_geom) == MP:
        polys = []
        # clip each geom in the `lo_geom` by each geom in the `hi_geom`
        for g in lo_geom:
            for gg in hi_geom:
                g = clipGeoms(gg, g)
            polys.append(g)
        return MultiPolygon(polys)


def fixOverlap(f, col):
    """Clips out overlapping geometries within a shapefile
    ranked by an attribute.
    """
    shp = gpd.read_file(f)
    shp = shp.loc[~shp.geometry.duplicated()]
    # shp.geometry.drop_duplicates(inplace=True)
    shp.sort_values(by=col, axis=0, ascending=False, inplace=True)
    shp.reset_index(drop=True, inplace=True)
    overlaps = find_overlaps(shp)
    for h_idx, l_idx in overlaps:
        greater = shp.loc[h_idx].geometry
        lesser = shp.loc[l_idx].geometry
        clipped_geometry = gpd.GeoSeries([clip_geometries(greater, lesser)])
        shp.loc[[l_idx], "geometry"] = clipped_geometry.values
    return shp


if __name__ == "__main__":

    loc = "/home/rick/dev/overlapTopoTool"
    # fn = f"{loc}/niwo010_treepolys/niwo010_treepolys.shp"
    fn = f"{loc}/circles.shp"
    column = "WEIGHT"
    out = fixOverlap(fn, column)
    out.to_file(f"{loc}/test.shp")
