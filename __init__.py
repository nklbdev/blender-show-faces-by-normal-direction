bl_info = {
	"name": "Show faces by normal direction",
	"description": "Show faces by normal direction",
	"author": "Nikolay Lebedev aka nklbdev",
	"version": (0, 1),
	"blender": (3, 6, 4),
	"category": "3D View"
}

import bpy

def show_only_faces_by_normal_direction(context, back):
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type="FACE")
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.ops.object.mode_set(mode="OBJECT")
    mesh = context.object.data
    camera_pos = bpy.context.space_data.region_3d.view_matrix.inverted().translation
    if back:
        for p in mesh.polygons:
            p.hide = (p.center - camera_pos).dot(p.normal) >= 0
    else:
        for p in mesh.polygons:
            p.hide = (p.center - camera_pos).dot(p.normal) <= 0
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="DESELECT")
    return {"FINISHED"}

class ShowOnlyFrontFaces(bpy.types.Operator):
    """Show only front faces"""
    bl_idname = "mesh.show_only_front_faces"
    bl_label = "Show only front faces"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return show_only_faces_by_normal_direction(context, True)

class ShowOnlyBackFaces(bpy.types.Operator):
    """Show only back faces"""
    bl_idname = "mesh.show_only_back_faces"
    bl_label = "Show only back faces"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return show_only_faces_by_normal_direction(context, False)

def menu_func(self, context):
    self.layout.operator(ShowOnlyFrontFaces.bl_idname)
    self.layout.operator(ShowOnlyBackFaces.bl_idname)

keymap = None
addon_keymaps = []

def register():
    bpy.utils.register_class(ShowOnlyFrontFaces)
    bpy.utils.register_class(ShowOnlyBackFaces)
    bpy.types.VIEW3D_MT_edit_mesh_showhide.append(menu_func)
    window_manager = bpy.context.window_manager
    if window_manager.keyconfigs.addon:
        keymap = window_manager.keyconfigs.active.keymaps["Mesh"]
        addon_keymaps.append(keymap.keymap_items.new(ShowOnlyFrontFaces.bl_idname, type="H", value="PRESS", ctrl=True, alt=False, shift=True))
        addon_keymaps.append(keymap.keymap_items.new(ShowOnlyBackFaces.bl_idname, type="H", value="PRESS", ctrl=True, alt=True, shift=True))

def unregister():
    bpy.utils.unregister_class(ShowOnlyFrontFaces)
    bpy.utils.unregister_class(ShowOnlyBackFaces)
    window_manager = bpy.context.window_manager
    keyconfig = window_manager.keyconfigs.addon
    if keyconfig:
        for keymap_item in addon_keymaps:
            keymap.keymap_items.remove(keymap_item)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
