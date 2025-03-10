import bpy

# Move all camera objects to location (0, 0, 0)
for obj in bpy.data.objects:
    if obj.type == 'CAMERA':
        obj.location = (0.0, 0.0, 0.0)

print("All camera object locations set to (0, 0, 0)!")