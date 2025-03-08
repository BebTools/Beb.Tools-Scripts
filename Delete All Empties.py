import bpy

# Deletes all empty objects from the scene
for obj in bpy.context.scene.objects:
    if obj.type == 'EMPTY':
        bpy.data.objects.remove(obj, do_unlink=True)

print("All empties deleted from the scene.")