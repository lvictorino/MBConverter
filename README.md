# MBConverter

MBConverter is an utility tool to reorder `MBTiles` files into **X/Y** hierarchy.

Start MBConverter in your `MBTiles` directory. A 'dump' directory will be created containing sub directories representing zoom levels. Every zoom directory will contain files named **XXX_YYY.png** with `X:0` and `Y:0` on the bottom left. A JSON files named `props.json` which contains the zoom level size will also be created in every zoom directory.
