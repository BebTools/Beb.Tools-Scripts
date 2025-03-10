import bpy

# Create an empty at (0,0,0) and parent all lights to it
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0.0, 0.0, 0.0))
new_empty = bpy.context.active_object
new_empty.name = "All_Lights_Parent"

for obj in bpy.data.objects:
    if obj.type == 'LIGHT':
        # Clear existing parent if any
        if obj.parent:
            obj.matrix_parent_inverse = obj.matrix_world
            obj.parent = None
        # Parent to new empty
        obj.parent = new_empty
        # Keep current transform
        obj.matrix_parent_inverse = new_empty.matrix_world.inverted()

print("All lights parented to new empty at (0, 0, 0)!")