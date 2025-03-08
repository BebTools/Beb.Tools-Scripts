import bpy

# Get the scene
scene = bpy.context.scene

# Collect names of all collections except the Scene Collection
collection_names_to_delete = [coll.name for coll in bpy.data.collections if coll != scene.collection]

# Move objects to Scene Collection and delete collections one by one
for coll_name in collection_names_to_delete[:]:  # Use a copy to avoid iteration issues
    if coll_name in bpy.data.collections:  # Check if it still exists
        coll = bpy.data.collections[coll_name]
        # Move all objects to Scene Collection
        for obj in coll.objects[:]:  # Use a copy of objects
            if obj.name not in scene.collection.objects:
                scene.collection.objects.link(obj)
                print(f"Moved {obj.name} to Scene Collection from {coll_name}")
            coll.objects.unlink(obj)
        # Delete the collection
        bpy.data.collections.remove(coll)
        print(f"Deleted collection: {coll_name}")

if not collection_names_to_delete:
    print("No user-created collections found to delete!")
else:
    print("All user-created collections deleted, objects preserved in Scene Collection!")