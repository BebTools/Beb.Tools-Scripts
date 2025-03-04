import bpy

def get_all_children(obj):
    """Recursively get all children of an object."""
    children = []
    for child in obj.children:
        children.append(child)
        children.extend(get_all_children(child))
    return children

def create_empty_collections(scene=None):
    # Use provided scene or fall back to bpy.context.scene
    if scene is None:
        scene = bpy.context.scene
    print(f"Current scene: {scene.name}")
    
    parent_empties = []
    print("All objects in scene:")
    for obj in scene.objects:
        print(f" - {obj.name}, Type: {obj.type}, Parent: {obj.parent}")
        if obj.type == 'EMPTY' and obj.parent is None:
            # Check if the empty is only in the Scene Collection
            current_collections = list(obj.users_collection)
            if len(current_collections) == 1 and current_collections[0] == scene.collection:
                parent_empties.append(obj)
                print(f"   Added as parent empty: {obj.name}")
            else:
                print(f"   Skipped {obj.name}: already in a custom collection")

    print(f"Found {len(parent_empties)} parent empty objects to process")
    if not parent_empties:
        print("No top-level empty objects found needing collections!")
        return
    
    for empty_obj in parent_empties:
        print(f"Processing empty: {empty_obj.name}")
        collection_name = f"{empty_obj.name}_Collection"
        new_collection = bpy.data.collections.new(collection_name)
        print(f"Created collection: {collection_name}")
        
        scene.collection.children.link(new_collection)
        print(f"Linked {collection_name} to scene")
        
        # Move the empty and all its children to the new collection
        objects_to_move = [empty_obj] + get_all_children(empty_obj)
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
create_empty_collections(bpy.context.scene)
print("Empty objects and their children organized into collections complete!")