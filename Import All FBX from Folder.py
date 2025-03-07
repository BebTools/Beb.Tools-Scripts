import bpy
import os
from bpy.types import Operator
from bpy.props import StringProperty

class BEBTOOLS_OT_ImportAllFBX(Operator):
    bl_idname = "bebtools.import_all_fbx"
    bl_label = "Import All FBX Files"
    bl_description = "Import all .fbx files from a directory and its subfolders"

    # Property for the directory path
    directory: StringProperty(
        name="Directory",
        description="Path to the directory containing .fbx files",
        subtype='DIR_PATH',
        default=""
    )

    def execute(self, context):
        """Import all .fbx files from the selected directory and its subfolders."""
        if not self.directory:
            self.report({'ERROR'}, "No directory selected!")
            print("No directory selected!")
            return {'CANCELLED'}
        
        fbx_files = []
        # Recursively walk through directory and subfolders
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.lower().endswith('.fbx'):
                    fbx_files.append(os.path.join(root, file))
        
        if not fbx_files:
            self.report({'WARNING'}, f"No .fbx files found in {self.directory} or its subfolders!")
            print(f"No .fbx files found in {self.directory} or its subfolders!")
            return {'FINISHED'}
        
        # Import each .fbx file
        for fbx_file in fbx_files:
            print(f"Importing: {fbx_file}")
            try:
                bpy.ops.import_scene.fbx(filepath=fbx_file)
                print(f"Successfully imported: {fbx_file}")
            except Exception as e:
                print(f"Error importing {fbx_file}: {str(e)}")
        
        self.report({'INFO'}, f"Imported {len(fbx_files)} .fbx files from {self.directory}")
        print(f"Imported {len(fbx_files)} .fbx files from {self.directory} and subfolders!")
        return {'FINISHED'}

    def invoke(self, context, event):
        """Open the file browser for directory selection."""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Register the operator (runs when script is loaded by Beb.Tools)
bpy.utils.register_class(BEBTOOLS_OT_ImportAllFBX)

# When called from Beb.Tools "Apply", this executes the operator
bpy.ops.bebtools.import_all_fbx('INVOKE_DEFAULT')