import bpy

def create_mesh_collections(scene=None):
    # Use provided scene or fall back to bpy.context.scene
    if scene is None:
        scene = bpy.context.scene
    print(f"Current scene: {scene.name}")
    
    parent_meshes = []
    print("All objects in scene:")
    for obj in scene.objects:
        print(f" - {obj.name}, Type: {obj.type}, Parent: {obj.parent}")
        if obj.type == 'MESH' and obj.parent is None:
            parent_meshes.append(obj)
            print(f"   Added as parent mesh: {obj.name}")
    
    print(f"Found {len(parent_meshes)} parent mesh objects")
    if not parent_meshes:
        print("No top-level mesh objects found in the scene!")
        return
    
    for mesh_obj in parent_meshes:
        print(f"Processing mesh: {mesh_obj.name}")
        collection_name = f"{mesh_obj.name}"
        new_collection = bpy.data.collections.new(collection_name)
        print(f"Created collection: {collection_name}")
        
        scene.collection.children.link(new_collection)
        print(f"Linked {collection_name} to scene")
        
        current_collections = list(mesh_obj.users_collection)
        print(f"Current collections for {mesh_obj.name}: {[coll.name for coll in current_collections]}")
        
        if current_collections:
            for coll in current_collections:
                coll.objects.unlink(mesh_obj)
                print(f"Unlinked {mesh_obj.name} from {coll.name}")
        else:
            print(f"{mesh_obj.name} was not in any collections")
        
        new_collection.objects.link(mesh_obj)
        print(f"Linked {mesh_obj.name} to {collection_name}")

bpy.ops.object.select_all(action='DESELECT')
create_mesh_collections(bpy.context.scene)
print("Mesh objects organized into collections complete!")