import geopandas as gpd
from shapely.geometry import MultiPolygon

def x_index(gdf):
    """Returns a list of tuples idntifying the geometries
    that overlap one another.
    """
    xidxs = []
    for x in gdf.index.tolist()[:-1]:
        for y in range(x+1,len(gdf)):
            a = gdf.ix[x].geometry.exterior
            b = gdf.ix[y].geometry.exterior
            if a.crosses(b): # crosses returns True even if the geoms only 
                xidxs.append((x,y)) # share 1 point in common..15/4
    return xidxs

def t_dict(d):
    """Creates a dictionary to pass to the GeoDataFrame instantiation 
    """
    g = {}
    for k in d:
        g[k] = [d[k]]
    return g

def clipGeoms(geom1,geom2):
    """Returns a clipped version of geom 2
    """
    return geom2.difference(geom1)

def mashGeoms(gdf,tup):
    """Modifies the overlapping geometries within the GeoDataFrame
    at the indexes passed into tup.
    """
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
        for n in a:
            b = clipGeoms(n,b)
        clipd = b
    if tt1 and tt2:    
        polys = []
        for m in b:
            for n in a:
                m = clipGeoms(n,m)
            polys.append(m)          
        clipd = MultiPolygon(polys)
    gdf.drop(tup[1],inplace=True)  
    new = gpd.GeoDataFrame(dc,index=[tup[1]],geometry=[clipd],crs=gdf.crs)     
    return gdf.append(new).sort_index()

def fixOverlap(f,col):
    """Clips out overlapping geometries within a shapefile
    ranked by an attribute.
    """
    shp = gpd.read_file(f)
    shp.sort_values(col,0,False,True)
    shp.reset_index(drop=True,inplace=True)
    iss = x_index(shp)
    for x in iss:
        shp = mashGeoms(shp,x)
    return shp

if __name__ == '__main__':
    
    loc ='/path/to/shapefile'
    fn = '%s/overlapping.shp' % loc
    column = 'NUM_IMAGES'
    out = fixOverlap(fn,column)
    out.to_file('%s/test.shp' % loc)
