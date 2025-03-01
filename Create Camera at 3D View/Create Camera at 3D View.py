import bpy
import mathutils

def add_camera_from_view():
    # Ensure we’re in a 3D View context
    if not bpy.context.area or bpy.context.area.type != 'VIEW_3D':
        print("Error: Must be run from a 3D View context!")
        return
    
    # Get the 3D viewport’s region data
    region_3d = bpy.context.region_data
    if not region_3d:
        print("Error: No 3D region data available!")
        return
    
    # Get view location, rotation, and distance
    view_loc = region_3d.view_location  # Target point (pivot)
    view_rot = region_3d.view_rotation  # Quaternion rotation
    view_dist = region_3d.view_distance  # Distance from pivot
    
    # Calculate camera position
    view_dir = mathutils.Vector((0, 0, -1))  # Default forward direction in view space
    view_dir.rotate(view_rot)  # Rotate to match viewport
    cam_loc = view_loc - view_dir * view_dist  # Position camera back along view direction
    
    # Add the camera
    bpy.ops.object.camera_add(location=cam_loc, rotation=view_rot.to_euler())
    camera = bpy.context.object
    camera.name = "Camera_From_View"
    
    # Match viewport lens (approximate focal length)
    camera.data.lens = region_3d.view_camera_zoom if region_3d.view_perspective == 'CAMERA' else 50  # Default to 50mm if not in camera view
    print(f"Added camera {camera.name} at {cam_loc} with rotation {camera.rotation_euler}")
    
    # Optional: Set as active camera (uncomment if desired)
    # bpy.context.scene.camera = camera
    
    print("Camera added matching current viewport view!")

# Run the function
add_camera_from_view()