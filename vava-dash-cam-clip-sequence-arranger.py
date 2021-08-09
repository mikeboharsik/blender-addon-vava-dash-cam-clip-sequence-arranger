bl_info = {
    "name": "Arrange VAVA Dash Cam Clips",
    "blender": (2, 93, 2),
    "category": "Object",
}

import bpy

def deleteRedundantAudioStrips(stripNames):
    sed = bpy.data.scenes[0].sequence_editor
    
    for name in stripNames:
        if name.find("R.001") != -1:
            strip = sed.sequences_all.get(name)
            strip.select = True
    bpy.ops.sequencer.delete()
    
def moveFrontStripsToChannel3(stripNames):
    sed = bpy.data.scenes[0].sequence_editor
    
    for name in stripNames:
        if name.find("F.MP4") != -1:
            strip = sed.sequences_all.get(name)
            strip.channel = 3
            strip.blend_type = "OVER_DROP"
            strip.transform.offset_y = 360
            strip.transform.scale_x = 0.25
            strip.transform.scale_y = 0.25

def getStripsInChannel(channel):
    sed = bpy.data.scenes[0].sequence_editor
    
    strips = []
    for strip in sed.sequences_all:
        if strip.channel == channel:
            strips.append(strip)
    return strips

def removeStripGaps():
    sed = bpy.data.scenes[0].sequence_editor
    
    channel2Strips = getStripsInChannel(2)
    for strip in channel2Strips:
        strip.frame_start = strip.frame_start - strip.frame_duration
    bpy.ops.sequencer.gap_remove(all=True)
    
def updateEndFrame():
    sed = bpy.data.scenes[0].sequence_editor
    
    maxEndFrame = 0
    for strip in sed.sequences_all:
        cur = strip.frame_final_end
        if cur > maxEndFrame:
            maxEndFrame = cur
    bpy.data.scenes[0].frame_end = maxEndFrame

def boostAudioVolume():
    sed = bpy.data.scenes[0].sequence_editor
    
    for strip in sed.sequences_all:
        if isinstance(strip, bpy.types.SoundSequence):
            strip.volume = 3.0

class ArrangeVavaDashCamClips(bpy.types.Operator):
    """Arrange VAVA Dash Cam Clips"""
    bl_idname = "object.arrange_vava_dash_cam_clips"
    bl_label = "Arrange VAVA Dash Cam Clips"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # ensure we have nothing selected
        bpy.ops.sequencer.select_all(action="DESELECT")

        sed = bpy.data.scenes[0].sequence_editor

        # get the list of all the strips currently in the editor
        stripNames = sed.sequences_all.keys()
        stripNames.sort()

        deleteRedundantAudioStrips(stripNames)
        moveFrontStripsToChannel3(stripNames)
        removeStripGaps()
        updateEndFrame()
        #boostAudioVolume()

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.row().separator()
    self.layout.operator(ArrangeVavaDashCamClips.bl_idname)

def register():
    bpy.utils.register_class(ArrangeVavaDashCamClips)
    bpy.types.SEQUENCER_MT_strip.append(menu_func)

def unregister():
    bpy.utils.unregister_class(ArrangeVavaDashCamClips)

if __name__ == "__main__":
    register()