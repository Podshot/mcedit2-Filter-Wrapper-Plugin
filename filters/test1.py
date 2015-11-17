#from plugins.wrapper import wrapper_api

displayName = "Test Filter"

inputs = (
          ("Int", (0, -5, 5)),
          ("String", "string"),
          ("Boolean", True),
          ("Float", (0.0, -10.0, 10.0)),
          ("Label", "label")
         )

def perform(level, box, options):
    print "---Filter Printing---"
    print options["Boolean"]
    print options["String"]
    print level.blockAt(box.minx, box.miny, box.minz)
    level.setBlockAt(box.maxx, box.maxy, box.maxz, 24)
    print "Success? " + str(level.blockAt(box.maxx, box.maxy, box.maxz) == 24)
    for (chunk, slices, point) in level.getChunkSlices(box):
        print dir(chunk)
        break;
    pass