import bpy

# Delete all lights in the scene
for obj in bpy.data.objects:
    if obj.type == 'LIGHT':
        bpy.data.objects.remove(obj, do_unlink=True)

print("All lights deleted from the scene!")