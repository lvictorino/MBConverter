import os
import sys
import json
from shutil import copyfile, rmtree

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
def get_sorted_directories(path=''):
    complete_path = os.getcwd() + '/'
    if path is not '':
        complete_path = complete_path + '/' + path + '/'
    
    directories=sorted([d for d in os.listdir(complete_path) if os.path.isdir(complete_path + d) and d != 'dump' ])
    return directories

# Convert int to string and add up to two zeros before if needed
# 42 will become '042', 7 will become '007'... etc.
def add_zero(val):
    val_str = str(val)
    if val < 10:
        val_str = '00' + str(val)
    elif val < 100:
        val_str = '0' + str(val)
    return val_str
    
# Convert the tile index (x,y) into world coordinates (in meter)
def compute_world_position(z, x, y):
    upp = zoom_upp[z] * tile_size
    world_x = osm_origin['x'] + upp * x + upp / 2
    world_y = osm_origin['y'] - upp * y - upp / 2 # Y coords are inverted 0 is top left
    return { 'coord_x': world_x, 'coord_y': world_y, 'offset': upp }

# Convert a dictionary to JSON and write it into a file at a given path
def save_json(path, props):
    f = open(path, 'w')
    f.write( json.dumps(props) )
    f.close()





if os.path.exists('dump') :
    rmtree('dump')
os.mkdir('dump')

total = 0

for zoom_dir in get_sorted_directories():
    os.mkdir('dump/' + zoom_dir)
    print 'operating on zoom level ' + zoom_dir
    x = 0
    for tile_dir in get_sorted_directories(zoom_dir):
        path = os.getcwd() + '/' + zoom_dir + '/' + tile_dir + '/'
        # Keep only png files
        png_files = sorted([f for f in os.listdir(path) if f.endswith('.png')])
        y = len(png_files) - 1
        for f in png_files:
            x_str = add_zero(x)
            y_str = add_zero(y)
            # Copy and rename original file to dump directory
            copyfile( path + f, 'dump/' + zoom_dir + '/' + x_str + "_" + y_str + ".png" )
            if x == 0 and y == 0:
                world_pos = compute_world_position(int(zoom_dir), int(tile_dir), int(os.path.splitext(f)[0]))
            y = y - 1
        x = x + 1

    # Write props (x;y) as json file.
    save_json('dump/'+zoom_dir+'/props.json', dict( { 'zoom': int(zoom_dir), 'count_x': x, 'count_y': len(png_files) }.items() + world_pos.items() ) )
    file_count = x * len(png_files)
    print str( file_count ) + ' files written.'
    total += file_count

print '----------------'
print 'Total: ' + str(total) + ' files written.'


