class LevelWrapper:
    
    def getChunkSlices(self, box):
        chunks = []
        for (cx, cz) in box.chunkPositions():
            chunk = self.worldEditor.adapter.readChunk(cx, cz, "")
            chunks.append((chunk, None, None))
        return chunks
    
    def blockAt(self, x, y, z):
        return self.editorSession.currentDimension.getBlockID(x,y,z)
    
    def blockDataAt(self, x, y, z):
        return self.editorSession.currentDimension.getBlockData(x,y,z)
    
    def setBlockAt(self, x, y, z, block_id):
        self.editorSession.currentDimension.setBlockID(x,y,z,block_id)
        
    def setBlockDataAt(self, x, y, z, data):
        self.editorSession.currentDimension.setBlockData(x,y,z,data)
        
    def __init__(self, worldEditor, editorSession):
        self.worldEditor = worldEditor
        self.editorSession = editorSession
        print "WorldEditor Adapter: " + str(dir(self.worldEditor.adapter))
        #print type(self.worldEditor.adapter.EntityRef)
        self.displayName = self.worldEditor.displayName
        #print dir(self.worldEditor.adapter.chunkPositions("Overworld"))
        #chunks = self.worldEditor.adapter.chunkPositions("Overworld")
        '''
        chunk = chunks.next()
        #    chunk = self.worldEditor.adapter.readChunk(x, z, "Overworld")
        print dir(chunk)
        print "===="
        '''