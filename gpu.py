import bpy
bpy.context.scene.cycles.device = 'GPU'
bpy.ops.render.render(True)