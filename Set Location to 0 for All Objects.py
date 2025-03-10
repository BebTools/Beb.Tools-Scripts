import bpy

# Move all mesh objects to location (0, 0, 0)
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.location = (0.0, 0.0, 0.0)

print("All mesh object locations set to (0, 0, 0)!")