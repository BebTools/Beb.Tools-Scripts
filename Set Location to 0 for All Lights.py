import bpy

# Move all light objects to location (0, 0, 0)
for obj in bpy.data.objects:
    if obj.type == 'LIGHT':
        obj.location = (0.0, 0.0, 0.0)

print("All light object locations set to (0, 0, 0)!")