#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 25 00:41:33 2017

@author: rick
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import MultiPolygon

def getMax(a,b):
    if a.NUM_IMAGES > b.NUM_IMAGES:
        return (a.name, b.name)
    else:
        return (b.name, a.name)

def t_dict(d):
    g = {}
    for k in p:
        g[k] = [d[k]]
    return g

shp = gpd.read_file('/home/rick/projects/AdjacentBoundaryTool/overlapping/overlapping.shp')
shp['dissolve'] = [i+100 for i in shp.index]
count = len(shp)
loop = shp.index.tolist()[:-1]
for x in loop:
    for y in range(x+1,len(shp)):
        if shp.ix[x].geometry.exterior.crosses(shp.ix[y].geometry.exterior):
            k,c = getMax(shp.ix[x],shp.ix[y])
            df = t_dict(shp.ix[c].drop('geometry').to_dict())
            geom = shp.ix[c].geometry.difference(shp.ix[k].geometry)
            add = gpd.GeoDataFrame()            
            if type(geom) == MultiPolygon():
                for g in geom: 
                    add = pd.concat([add,gpd.GeoDataFrame(df,index=[c],geometry=[g])])
            else:
                add = pd.concat([add,gpd.GeoDataFrame(df,index=[c],geometry=[geom])])
            shp.drop(c,inplace=True)
            shp = pd.concat([shp,add])

type(shp.ix[c].geometry.difference(shp.ix[k].geometry))
for g in geom:
    new = gpd.GeoDataFrame(df,index=[c],geometry=[g])
ll={}
for key in p:
    ll[key] = [p[key]]


shp.ix[x].geometryx
shp.ix[y].geometry
##################################
import pandas as pd
import geopandas as gpd
from shapely.geometry import MultiPolygon

def x_index(gdf):
    # this one took me forever to figure out, 
    # but I think its' the best way to find polys
    # indexes to do operations on
    xidxs = []
    for x in gdf.index.tolist()[:-1]:
        for y in range(x+1,len(shp)):
            a = gdf.ix[x].geometry.exterior
            b = gdf.ix[y].geometry.exterior
            if a.crosses(b): # crosses returns True even if the geoms only 
                xidxs.append((x,y)) # share 1 point in common..15/4
    return xidxs

def t_dict(d):
    g = {}
    for k in d:
        g[k] = [d[k]]
    return g

def clipGeoms(geom1,geom2):
    return geom2.difference(geom1)

def mashGeoms(gdf,tup):
    clip = gdf.ix[tup[1]]
    dc = t_dict(clip.drop('geometry').to_dict())
    a = gdf.loc[tup[0]].geometry
    b = clip.geometry
    tt1 = type(a) == type(MultiPolygon())
    tt2 = type(b) == type(MultiPolygon())    
    if not tt1 and not tt2:
        clipd = clipGeoms(a,b)
    if not tt1 and tt2:
        polys = []
        for m in b:
            polys.append(clipGeoms(a,m))
        clipd = MultiPolygon(polys)
    if tt1 and not tt2:
        print 'B'
        pass
    if tt1 and tt2:    
        polys = []
        keep = None
        count = 0
        for m in b:
            area = float('inf')
            for n in a:
                m = clipGeoms(n,m)
#                if n.disjoint(m):
#                    if keep == None and count == len(a):
#                        keep = b
#                    count += 1
#                    continue
#                else:
#                    cl = clipGeoms(n,m)
#                    if cl.area < area:
#                        keep = cl

            polys.append(m)          
        clipd = MultiPolygon(polys)
    gdf.drop(tup[1],inplace=True)  
    new = gpd.GeoDataFrame(dc,index=[tup[1]],geometry=[clipd],crs=gdf.crs)     
    return pd.concat([gdf,new]).sort_index()
n=a[] 
m=b[0]   
cl1 = clipGeoms(n,m)
cl.symmetric_difference(cl1)

shp = gpd.read_file('/home/rick/projects/AdjacentBoundaryTool/overlapping/overlapping.shp')
#order by col
shp.columns
shp.sort_values('NUM_IMAGES',0,False,True)
shp.reset_index(drop=True,inplace=True)
pp = x_index(shp)
#shp.insert(1,'dissolve',[i+100 for i in shp.index])


new = mashGeoms(shp,pp[0])    
poop = mashGeoms(new,pp[1])
ho = mashGeoms(poop,pp[2])
ho.crs
fw = mashGeoms(ho,pp[3])
gro = mashGeoms(fw,pp[4])

gdf = gro.copy()
tup = pp[5]

toy.to_file('/home/rick/projects/AdjacentBoundaryTool/overlapping/test2.shp')
toy = mashGeoms(gro,pp[5])

chk = toy.ix[3]
len(chk.geometry)

gdf = ho.copy()

def mashGeoms(gdf,tup):
    clip = gdf.ix[tup[1]]
    dc = t_dict(clip.drop('geometry').to_dict())
    a = gdf.loc[tup[0]].geometry
    b = clip.geometry
    tt1 = type(a) == type(MultiPolygon())
    tt2 = type(b) == type(MultiPolygon())    
    if not tt1 and not tt2:
        clipd = clipGeoms(a,b)
    if not tt1 and tt2:
        polys = []
        for m in b:
            polys.append(clipGeoms(a,m))
        clipd = MultiPolygon(polys)
    if tt1 and not tt2:
        print 'B'
        pass
    if tt1 and tt2:    
        polys = []
        keep = None
        count = 0
        for m in b:
            area = float('inf')
            for n in a:
                if n.disjoint(m):
                    if keep == None and count == len(a):
                        keep = b
                    continue
                else:
                    cl = clipGeoms(n,m)
                    if cl.area < area:
                        keep = cl
            polys.append(keep)          
        clipd = MultiPolygon(polys)
    gdf.drop(tup[1],inplace=True)  
    new = gpd.GeoDataFrame(dc,index=[tup[1]],geometry=[clipd],crs=gdf.crs)     
    return pd.concat([gdf,new]).sort_index()



def getMax(a,b):
    if a.NUM_IMAGES > b.NUM_IMAGES:
        return (a.name, b.name)
    else:
        return (b.name, a.name)



def clipGeoms(gdf, ls):
    add = gpd.GeoDataFrame(crs=c)
    for x,y in dd:
        keep,clip = getMax(gd
    c = gdf.crsf.ix[x],gdf.ix[y])
        dk = t_dict(shp.ix[keep].drop('geometry').to_dict())
        dc = t_dict(shp.ix[clip].drop('geometry').to_dict())
        a = shp.ix[keep].geometry
        b = shp.ix[clip].geometry
        gA = gpd.GeoDataFrame(dk,geometry=[a.difference(b)],crs=c)
        gN = gpd.GeoDataFrame(dk,geometry=[a.intersection(b)],crs=c)
        gB = gpd.GeoDataFrame(dc,geometry=[b.difference(a)],crs=c)
        add = pd.concat([gA,gN,gB,add])
    return add

new = clipGeoms(shp, dd)
tin = gpd.GeoDataFrame()
for idx,row in new.iterrows():
    if type(row.geometry) != type(Point()):
        g = t_dict(row.drop('geometry').to_dict())
        tin = pd.concat([tin,gpd.GeoDataFrame(g,geometry=[row.geometry])])

dis = tin.dissolve(by='dissolve')
tin.crs = c  
new[type(row.geometry) != type(Point)]



add.crs = 
dd = x_index(shp)
dd
# order by photo_val
# find crossings
# if len(cross_list) > 1
# fix the first
# note: when fixing test for return of point or line in geom

# for those that aren't overlapping...
set([e for l in dd for e in l])
