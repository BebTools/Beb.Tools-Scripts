import bpy
import os
from bpy.types import Operator
from bpy.props import StringProperty

class BEBTOOLS_OT_ImportAllOBJ(Operator):
    bl_idname = "bebtools.import_all_obj"
    bl_label = "Import All OBJ Files"
    bl_description = "Import all .obj files from a directory and its subfolders"

    # Property for the directory path
    directory: StringProperty(
        name="Directory",
        description="Path to the directory containing .obj files",
        subtype='DIR_PATH',
        default=""
    )

    def execute(self, context):
        """Import all .obj files from the selected directory and its subfolders."""
        if not self.directory:
            self.report({'ERROR'}, "No directory selected!")
            print("No directory selected!")
            return {'CANCELLED'}
        
        obj_files = []
        # Recursively walk through directory and subfolders
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.lower().endswith('.obj'):
                    obj_files.append(os.path.join(root, file))
        
        if not obj_files:
            self.report({'WARNING'}, f"No .obj files found in {self.directory} or its subfolders!")
            print(f"No .obj files found in {self.directory} or its subfolders!")
            return {'FINISHED'}
        
        # Import each .obj file
        for obj_file in obj_files:
            print(f"Importing: {obj_file}")
            try:
                bpy.ops.wm.obj_import(filepath=obj_file)  # Blender 4.2's OBJ importer
                print(f"Successfully imported: {obj_file}")
            except Exception as e:
                print(f"Error importing {obj_file}: {str(e)}")
        
        self.report({'INFO'}, f"Imported {len(obj_files)} .obj files from {self.directory}")
        print(f"Imported {len(obj_files)} .obj files from {self.directory} and subfolders!")
        return {'FINISHED'}

    def invoke(self, context, event):
        """Open the file browser for directory selection."""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Register the operator
bpy.utils.register_class(BEBTOOLS_OT_ImportAllOBJ)

# Execute with file browser
bpy.ops.bebtools.import_all_obj('INVOKE_DEFAULT')