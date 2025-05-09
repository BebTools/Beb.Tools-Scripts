import bpy

# Create an empty at (0,0,0) and parent all mesh objects to it
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0.0, 0.0, 0.0))
new_empty = bpy.context.active_object
new_empty.name = "All_Objects_Parent"

for obj in bpy.data.objects:
    # Skip the new empty itself and only process mesh objects
    if obj != new_empty and obj.type == 'MESH':
        # Clear existing parent if any
        if obj.parent:
            obj.matrix_parent_inverse = obj.matrix_world
            obj.parent = None
        # Parent to new empty
        obj.parent = new_empty
        # Keep current transform
        obj.matrix_parent_inverse = new_empty.matrix_world.inverted()

print("All mesh objects parented to new empty at (0, 0, 0)!")