import bpy

# Delete all cameras in the scene
for obj in bpy.data.objects:
    if obj.type == 'CAMERA':
        bpy.data.objects.remove(obj, do_unlink=True)

print("All cameras deleted from the scene!")