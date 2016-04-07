import os
import sys
import json
from shutil import copyfile, rmtree

def get_sorted_directories(path=''):
    complete_path = os.getcwd() + '/'
    if path is not '':
        complete_path = complete_path + '/' + path + '/'
    
    directories=sorted([d for d in os.listdir(complete_path) if os.path.isdir(complete_path + d) and d != 'dump' ])
    return directories

def add_zero(val):
    val_str = str(val)
    if val < 10:
        val_str = '00' + str(val)
    elif val < 100:
        val_str = '0' + str(val)
    return val_str
    

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
            y = y - 1
        x = x + 1

    # Write props (x;y) as json file.
    f = open('dump/'+zoom_dir+'/props.json', 'w')
    f.write( json.dumps({'x': str(x), 'y': len(png_files)}) )
    f.close()
    file_count = x * len(png_files)
    print str( file_count ) + ' files written.'
    total += file_count

print '----------------'
print 'Total: ' + str(total) + ' files written.'


