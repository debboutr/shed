from itertools import combinations

import click
import geopandas as gpd
from shapely.ops import snap
from shapely.geometry import MultiPolygon

MP = type(MultiPolygon())


def find_overlaps(gdf):
    """Returns a list of tuples identifying the geometries
    that overlap one another.
    """
    # breakpoint()
    overlaps = []
    for x, y in combinations(gdf.index.tolist(), 2):
        x_geom = gdf.loc[x].geometry.exterior
        y_geom = gdf.loc[y].geometry.exterior
        if x_geom.crosses(y_geom):
            overlaps.append((x, y))
    return overlaps


def clipGeoms(geom1, geom2):
    """Returns a clipped version of geom2"""
    glo = geom2.difference(geom1)
    ghi = snap(geom1, glo, 1)
    return ghi, glo

        
def iterate_overlaps(gdf, overlaps):
    for hi, lo in overlaps:
        yield (hi, gdf.loc[hi].geometry), (lo, gdf.loc[lo].geometry)

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
    for (hi, greater), (lo, lesser) in iterate_overlaps(shp, overlaps):
        hi_clip, lo_clip = clipGeoms(greater, lesser)
        shp.loc[[lo], "geometry"] = lo_clip
        shp.loc[[hi], "geometry"] = hi_clip
    for (hi, greater), (lo, lesser) in iterate_overlaps(shp, overlaps):
        shp.loc[[hi], "geometry"] = snap(greater, lesser, 1)
        shp.loc[[lo], "geometry"] = snap(lesser, greater, 1)
    return shp


if __name__ == "__main__":

    loc = "/home/rick/dev/overlapTopoTool"
    # fn = f"{loc}/niwo010_treepolys/niwo010_treepolys.shp"
    # fn = f"{loc}/circles.shp"
    fn = f"{loc}/original_shapes.gpkg"
    # column = "WEIGHT"
    column = "weight"
    out = fixOverlap(fn, column)
    out.to_file(f"{loc}/test7.gpkg", driver="GPKG")
