#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 20:17:40 2023

@author: rick
"""

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
    return geom2.difference(geom1)


def clip_geometries(hi_geom, lo_geom):
    """clips the `lo_geom` to the `hi-geom` and handles Multipolygon
    issues. Returns the updated geometry for `lo_geom`.
    """
    # breakpoint()
    if not type(hi_geom) == MP and not type(lo_geom) == MP:
        new = clipGeoms(hi_geom, lo_geom)
        return snap(hi_geom, new, 1) , new
    if not type(hi_geom) == MP and type(lo_geom) == MP:
        polys = []
        for g in lo_geom.geoms:
            polys.append(clipGeoms(hi_geom, g))
        new = MultiPolygon(polys)
        return snap(hi_geom, new, 1) , new
    if type(hi_geom) == MP and not type(lo_geom) == MP:
        # clip by every geometry in the MultiPolygon
        for g in hi_geom.geoms:
            lo_geom = clipGeoms(g, lo_geom)
        new = lo_geom
        return snap(hi_geom, new, 1) , new
    if type(hi_geom) == MP and type(lo_geom) == MP:
        polys = []
        # clip each geom in the `lo_geom` by each geom in the `hi_geom`
        for g in lo_geom.geoms:
            for gg in hi_geom.geoms:
                g = clipGeoms(gg, g)
            polys.append(g)
        new = MultiPolygon(polys)
        return snap(hi_geom, new, 1) , new
        


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
        hi_clip, lo_clip = clip_geometries(greater, lesser)
        shp.loc[[l_idx], "geometry"] = lo_clip
        shp.loc[[h_idx], "geometry"] = hi_clip
    for h_idx, l_idx in overlaps:
        greater = shp.loc[h_idx].geometry
        lesser = shp.loc[l_idx].geometry
        shp.loc[[h_idx], "geometry"] = snap(greater, lesser, 1)
        shp.loc[[l_idx], "geometry"] = snap(lesser, greater, 1)
    return shp


if __name__ == "__main__":

    loc = "/home/rick/dev/overlapTopoTool"
    # fn = f"{loc}/niwo010_treepolys/niwo010_treepolys.shp"
    # fn = f"{loc}/circles.shp"
    fn = f"{loc}/original_shapes.gpkg"
    # column = "WEIGHT"
    column = "weight"
    out = fixOverlap(fn, column)
    out.to_file(f"{loc}/test5.gpkg", driver="GPKG")

