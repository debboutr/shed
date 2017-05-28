# overlapTopoTool

![final](https://cloud.githubusercontent.com/assets/7052993/26517603/f1956e66-4250-11e7-897b-8c12e5a83e1c.png)

# Fix overlapping topologies weighted by attribute...

Remove overlapping polygons in a shapefile using python's geopandas package. Overlapping geometries will be resolved according to an attribute field. The higher value will retain it's geometry where the lower will be clipped. The image above demonstrates a before and after, images on the right show the polygons pulled apart to visualize the output geometries. Below is a table of the GeoDataFrame.

![table](https://cloud.githubusercontent.com/assets/7052993/26526064/c10a6aae-4321-11e7-9272-24b9afd76717.png)
