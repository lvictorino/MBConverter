import os
import sys
import json
from shutil import copyfile, rmtree

#Extracted from http://demo.business-geografic.com/osm/tilemap.xml
zoom_upp = [ 156543.033928,
             78271.516964,
             39135.758482,
             19567.879241,
             9783.939621,
             4891.969810,
             2445.984905,
             1222.992453,
             611.496226,
             305.748113,
             152.874057,
             76.4370282714844,
             38.2185141357422,
             19.1092570678711,
             9.55462853393555,
             4.77731426696777,
             2.38865713348389,
             1.19432856674194,
             0.59716428337097,
             0.29858214169741 ]

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
    world_x = upp * x + upp / 2
    world_y = upp * y + upp / 2
    return { 'zoom': z, 'coord_x': world_x, 'coord_y': world_y, 'offset': upp }

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
    save_json('dump/'+zoom_dir+'/props.json', dict( { 'count_x': x, 'count_y': len(png_files) }.items() + world_pos.items() ) )
    file_count = x * len(png_files)
    print str( file_count ) + ' files written.'
    total += file_count

print '----------------'
print 'Total: ' + str(total) + ' files written.'


