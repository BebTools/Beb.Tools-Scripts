import bpy

# Move all empty objects to location (0, 0, 0)
for obj in bpy.data.objects:
    if obj.type == 'EMPTY':
        obj.location = (0.0, 0.0, 0.0)

print("All empty object locations set to (0, 0, 0)!")