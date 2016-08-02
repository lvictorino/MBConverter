import os
from os import path
import glob
import sys
import json
from shutil import copyfile, rmtree

# MBConverter is an utility tool to reorder `MBTiles` files into X;Y hierarchy.
# Start MBConverter passing in your `MBTiles` directory and the output directory.
# The output directory (created if needed) will contain sub directories representing zoom levels.
# Every zoom level directory will contain files named **XXX_YYY.png** with `X:0` and `Y:0` placed on the bottom left.
# A JSON files `mapprops.json` containing the zoom levels, sizes, and properties will be created in the output directory.

####################################################################
# Extracted from http://demo.business-geografic.com/osm/tilemap.xml
# Distance in meter by zoom levels for every tile pixels.
zoom_upp = [ 156543.033928, # 0
             78271.516964,  # 1
             39135.758482,  # 2
             19567.879241,  # 3
             9783.939621,   # 4
             4891.969810,   # 5
             2445.984905,   # 6
             1222.992453,   # 7
             611.496226,    # 8
             305.748113,    # 9
             152.874057,    # 10
             76.4370282714844, # 11
             38.2185141357422, # 12
             19.1092570678711, # 13
             9.55462853393555, # 14
             4.77731426696777, # 15
             2.38865713348389, # 16
             1.19432856674194, # 17
             0.59716428337097, # 18
             0.29858214169741 ]# 19
# OSM World Origin
osm_origin = { 'x': -20037508.34, 'y': 20037508.34 }
####################################################################

tile_size = 256

# Returned a directory list, sorted alphabetically, for a given path
def get_sorted_directories(p=''):
    if p is '':
        p = os.getcwd() + '/'
        
    directories=sorted([path.normpath(d) for d in glob.glob(p + '/*') if path.isdir(d)])
    return directories
    
# Convert the tile index (x,y) into world coordinates (in meter)
def compute_world_position(z, x, y):
    upp = zoom_upp[z] * tile_size
    world_x = osm_origin['x'] + upp * x + upp / 2
    world_y = osm_origin['y'] - upp * y - upp / 2 # Y coords are inverted 0 is top left
    return { 'coord_x': world_x, 'coord_y': world_y, 'offset': upp }

def save_zoom_props(p, props):
    with open(p,'w') as f:
        f.write( json.dumps(props) )
    
# ----------------------------------------------------------------------------

if len(sys.argv) < 3:
    print 'Error: not enough arguments.'
    print 'Usage: mbconverter.py mbtiles_dir destination_dir'
    sys.exit(0)

src_dir = sys.argv[1] + '/'
dst_dir = sys.argv[2] + '/'
    
# Delete destination directory if needed
if path.exists(dst_dir) :
    rmtree(dst_dir)
os.mkdir(dst_dir)

total = 0

mapdict = { 'layers': [], 'zooms': [] }
for zoom_dir in get_sorted_directories(src_dir):
    dir_name = path.basename(zoom_dir)
    os.mkdir(dst_dir + dir_name)
    print 'operating on zoom level ' + dir_name
    x = 0

    
    for tile_dir in get_sorted_directories(zoom_dir):

        # Keep only png files
        png_files = sorted([f for f in os.listdir(tile_dir) if f.endswith('.png')])

        y = len(png_files) - 1
        for f in png_files:
            x_str = '%03d' % x
            y_str = '%03d' % y

            # Copy and rename original file to destination directory
            copyfile( path.normpath(tile_dir + '/' + f), path.normpath(dst_dir + dir_name + '/' + x_str + "_" + y_str + ".png") )

            # Use the first tile to compute world position
            if x == 0 and y == 0:
                world_pos = compute_world_position(int(dir_name), int(path.basename(tile_dir)), int(path.splitext(f)[0]))
            
            y = y - 1
        x = x + 1

    # Add layer props to mapdict
    mapdict['layers'].append(dict( { 'zoom': int(dir_name), 'count_x': x, 'count_y': len(png_files) }.items() + world_pos.items() ) )
    mapdict['zooms'].append(int(dir_name))

    # Update file_count and print
    file_count = x * len(png_files)
    print '> ' + str( file_count ) + ' files written.'
    total += file_count

# Write mapdict as a JSON file in destination directory
with open(dst_dir + 'mapprops.json','w') as f:
    f.write( json.dumps(mapdict) )

print '----------------'
print 'Total: ' + str(total) + ' files written.'


