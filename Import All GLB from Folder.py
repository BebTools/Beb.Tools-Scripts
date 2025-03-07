import bpy
import os
from bpy.types import Operator
from bpy.props import StringProperty

class BEBTOOLS_OT_ImportAllGLB(Operator):
    bl_idname = "bebtools.import_all_glb"
    bl_label = "Import All GLB Files"
    bl_description = "Import all .glb files from a directory and its subfolders"

    # Property for the directory path
    directory: StringProperty(
        name="Directory",
        description="Path to the directory containing .glb files",
        subtype='DIR_PATH',
        default=""
    )

    def execute(self, context):
        """Import all .glb files from the selected directory and its subfolders."""
        if not self.directory:
            self.report({'ERROR'}, "No directory selected!")
            print("No directory selected!")
            return {'CANCELLED'}
        
        glb_files = []
        # Recursively walk through directory and subfolders
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.lower().endswith('.glb'):
                    glb_files.append(os.path.join(root, file))
        
        if not glb_files:
            self.report({'WARNING'}, f"No .glb files found in {self.directory} or its subfolders!")
            print(f"No .glb files found in {self.directory} or its subfolders!")
            return {'FINISHED'}
        
        # Import each .glb file
        for glb_file in glb_files:
            print(f"Importing: {glb_file}")
            try:
                bpy.ops.import_scene.gltf(filepath=glb_file)  # GLB uses the same importer as GLTF
                print(f"Successfully imported: {glb_file}")
            except Exception as e:
                print(f"Error importing {glb_file}: {str(e)}")
        
        self.report({'INFO'}, f"Imported {len(glb_files)} .glb files from {self.directory}")
        print(f"Imported {len(glb_files)} .glb files from {self.directory} and subfolders!")
        return {'FINISHED'}

    def invoke(self, context, event):
        """Open the file browser for directory selection."""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Register the operator
bpy.utils.register_class(BEBTOOLS_OT_ImportAllGLB)

# Execute with file browser
bpy.ops.bebtools.import_all_glb('INVOKE_DEFAULT')