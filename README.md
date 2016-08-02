# MBConverter

MBConverter is an utility tool to reorder `MBTiles` files into X;Y hierarchy.

Start MBConverter passing in your `MBTiles` directory and the output directory.

The output directory (created if needed) will contain sub directories representing zoom levels.

Every zoom level directory will contain files named **XXX_YYY.png** with `X:0` and `Y:0` placed on the bottom left.

A JSON files `mapprops.json` containing the zoom levels, sizes, and properties will be created in the output directory.
