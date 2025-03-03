import bpy
import mathutils

def create_bbox_for_object(obj):
    if obj.type != 'MESH' or not obj.data:
        return None
    
    # Store the original collections the object is in
    original_collections = list(obj.users_collection)
    
    # Enable Texture Space (temporarily)
    obj.show_texture_space = True

    # Get Texture Space bounding box from mesh data
    tex_space_loc = mathutils.Vector(obj.data.texspace_location)  # Center
    tex_space_size = mathutils.Vector(obj.data.texspace_size)  # Half extents

    # Correct the size by doubling the extents
    bbox_size = tex_space_size * 2  # Full size of the bounding box

    # Create Empty Cube at the correct position
    bpy.ops.object.empty_add(type='CUBE', align='WORLD', location=tex_space_loc)
    empty_cube = bpy.context.object

    # Scale empty to match the bounding box
    empty_cube.scale = bbox_size / 2  # Empty scale is half the full size

    # Name it based on the object
    empty_cube.name = f"{obj.name}_BBox"

    # Store the mesh's original world matrix
    original_matrix = obj.matrix_world.copy()

    # Deselect all and select the objects for parenting
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    empty_cube.select_set(True)
    bpy.context.view_layer.objects.active = empty_cube  # Set empty as active

    # Use Blender's built-in parent operator to mimic manual parenting
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

    # Restore the mesh's world matrix to ensure no transform change
    obj.matrix_world = original_matrix

    # Disable Texture Space display after processing
    obj.show_texture_space = False

    # Restore the mesh to its original collections
    current_collections = list(obj.users_collection)
    for coll in current_collections:
        if coll not in original_collections:
            coll.objects.unlink(obj)  # Remove from any new collections
    for coll in original_collections:
        if obj.name not in coll.objects:  # Use object name for check
            coll.objects.link(obj)  # Re-link to original collections

    # Link the empty cube to the same collections as the mesh
    empty_current_collections = list(empty_cube.users_collection)
    for coll in empty_current_collections:
        coll.objects.unlink(empty_cube)  # Remove from default (e.g., scene collection)
    for coll in original_collections:
        if empty_cube.name not in coll.objects:  # Use object name for check
            coll.objects.link(empty_cube)  # Add to mesh's original collections

    return empty_cube

# First, apply transforms to ALL objects in the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.select_all(action='DESELECT')

# Then create bounding boxes for mesh objects
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        empty_cube = create_bbox_for_object(obj)

print("Transforms applied to all objects, bounding box empties created for meshes, meshes parented with correct size and returned to original collections, and texture space turned off!")