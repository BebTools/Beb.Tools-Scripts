import bpy

def get_all_children(obj):
    """Recursively get all children of an object."""
    children = []
    for child in obj.children:
        children.append(child)
        children.extend(get_all_children(child))
    return children

def create_light_collections(scene=None):
    # Use provided scene or fall back to bpy.context.scene
    if scene is None:
        scene = bpy.context.scene
    print(f"Current scene: {scene.name}")
    
    parent_lights = []
    print("All objects in scene:")
    for obj in scene.objects:
        print(f" - {obj.name}, Type: {obj.type}, Parent: {obj.parent}")
        if obj.type == 'LIGHT' and obj.parent is None:
            # Check if the light is only in the Scene Collection
            current_collections = list(obj.users_collection)
            if len(current_collections) == 1 and current_collections[0] == scene.collection:
                parent_lights.append(obj)
                print(f"   Added as parent light: {obj.name}")
            else:
                print(f"   Skipped {obj.name}: already in a custom collection")

    print(f"Found {len(parent_lights)} parent light objects to process")
    if not parent_lights:
        print("No top-level light objects found needing collections!")
        return
    
    for light_obj in parent_lights:
        print(f"Processing light: {light_obj.name}")
        collection_name = f"{light_obj.name}_Collection"
        new_collection = bpy.data.collections.new(collection_name)
        print(f"Created collection: {collection_name}")
        
        scene.collection.children.link(new_collection)
        print(f"Linked {collection_name} to scene")
        
        # Move the light and all its children to the new collection
        objects_to_move = [light_obj] + get_all_children(light_obj)
        for obj in objects_to_move:
            current_collections = list(obj.users_collection)
            print(f"Current collections for {obj.name}: {[coll.name for coll in current_collections]}")
            
            if current_collections:
                for coll in current_collections:
                    coll.objects.unlink(obj)
                    print(f"Unlinked {obj.name} from {coll.name}")
            else:
                print(f"{obj.name} was not in any collections")
            
            new_collection.objects.link(obj)
            print(f"Linked {obj.name} to {collection_name}")

bpy.ops.object.select_all(action='DESELECT')
create_light_collections(bpy.context.scene)
print("Light objects and their children organized into collections complete!")