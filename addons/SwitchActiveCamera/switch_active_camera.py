from re import S
import bpy
from bpy.types import Operator

bl_info = {
    "name": "SwitchActiveCamera",
    "author": "minatty",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "location": "View3D > Camera",
    "description": "Switches active camera in a scene",
    "warning": "",
    "doc_url": "",
    "category": "Scene camera",
}

addon_keymaps = []

class UI_PT_Panel(bpy.types.Panel):
    bl_label = "Switch Active Camera"
    bl_category = "View"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.operator("switch_camera.forward")
        layout.operator("switch_camera.backward")

class SwitchSceneCameraForward(bpy.types.Operator):
    """シーンカメラを切り替える(順巡)"""

    bl_idname = "switch_camera.forward"
    bl_label = "order (Alt + Num3)"
    bl_description = "Switch active camera (forward)"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        switch_camera(self, 1)
        return {"FINISHED"}

class SwitchSceneCameraBackward(bpy.types.Operator):
    """シーンカメラを切り替える(逆巡)"""

    bl_idname = "switch_camera.backward"
    bl_label = "reverse (Alt + Num1)"
    bl_description = "Switch active camera (backward)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        switch_camera(self, -1)
        return {"FINISHED"}

def switch_camera(self, direction):
    cams = [obj for obj in bpy.data.objects if obj.type == "CAMERA" ]
    if len(cams) <= 0:
        self.report({'INFO'}, "There is no camera in a scene.")
        return
    camsSorted = sorted(cams, key=lambda x: x.name)
    curr_cam_name = bpy.context.scene.camera.name
    curr_cam_idx = 0
    for idx, cam in enumerate(camsSorted):
        if cam.name == curr_cam_name:
            curr_cam_idx = idx
            break
    bpy.context.scene.camera = cams[(curr_cam_idx + direction) % len(camsSorted)]

classes = (
    SwitchSceneCameraForward,
    SwitchSceneCameraBackward,
    UI_PT_Panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    key_assign_list = [
        (SwitchSceneCameraForward.bl_idname, "NUMPAD_3", "PRESS", False, True, False),
        (SwitchSceneCameraBackward.bl_idname, "NUMPAD_1", "PRESS", False, True, False),
    ]
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        for (idname, key, event, ctrl, alt, shift) in key_assign_list:
            kmi = km.keymap_items.new(
                idname, key, event, ctrl=ctrl, alt=alt, shift=shift
            )
            addon_keymaps.append((km, kmi))
    print("SwitchActiveCamera is registered.")

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    print("SwitchActiveCamera is unregistered.")

if __name__ == "__main__":
    register()