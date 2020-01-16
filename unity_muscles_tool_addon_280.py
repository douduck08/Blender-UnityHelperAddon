import bpy

bl_info = {
    "name": "Unity Muscles Tool",
    "author": "douduck",
    # "description": "",
    "blender": (2, 80, 0),
    # "version": (0, 0, 1),
    # "location": "",
    # "warning": "",
    "category": "Rigging"
}

PI = 3.1415926

# bone_name: [min_x, max_x, min_y, max_y, min_z, max_z]
rotation_limit = {
    'UpperArm.L': [-140, 20, -90, 90, -100, 100],
    'UpperArm.R': [-140, 20, -90, 90, -100, 100],
    'LowerArm.L': [-90, 90, -90, 90, -160, 0],
    'LowerArm.R': [-90, 90, -90, 90, 0, 160]
}


def remove_constraint(bone):
    copyLocConstraints = [c for c in bone.constraints if c.type == 'LIMIT_ROTATION']
    for c in copyLocConstraints:
        bone.constraints.remove(c)


def set_constraint(bone, min_x=0, max_x=0, min_y=0, max_y=0, min_z=0, max_z=0):
    # print(bone.name)
    remove_constraint(bone)
    c = bone.constraints.new('LIMIT_ROTATION')
    c.owner_space = 'LOCAL'
    c.use_transform_limit = True

    c.use_limit_x = True
    if (c.use_limit_x):
        c.min_x = min_x / 180 * PI
        c.max_x = max_x / 180 * PI

    c.use_limit_y = True
    if (c.use_limit_y):
        c.min_y = min_y / 180 * PI
        c.max_y = max_y / 180 * PI

    c.use_limit_z = True
    if (c.use_limit_z):
        c.min_z = min_z / 180 * PI
        c.max_z = max_z / 180 * PI


class SetUnityMusclesConstraint(bpy.types.Operator):
    """Set Unity Muscles Constraint"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "rigidbody.set_unity_muscles"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Set Unity Muscles"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # execute() is called when running the operator.
    def execute(self, context):
        context = bpy.context
        rig = context.active_object

        if rig.type == 'ARMATURE':
            # print("Found Armature Object: " + context.active_object.name)
            for bone in rig.pose.bones:
                if (bone.name in rotation_limit):
                    degrees = rotation_limit[bone.name]
                    set_constraint(bone, degrees[0], degrees[1], degrees[2], degrees[3], degrees[4], degrees[5])

        return {'FINISHED'}


class ClearUnityMusclesConstraint(bpy.types.Operator):
    """Clear Unity Muscles Constraint"""
    bl_idname = "rigidbody.clear_unity_muscles"
    bl_label = "Clear Unity Muscles"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context = bpy.context
        rig = context.active_object

        if rig.type == 'ARMATURE':
            for bone in rig.pose.bones:
                remove_constraint(bone)

        return {'FINISHED'}


class UnityMusclesHelperPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_unity_muscles_helper"
    bl_label = "Unity Muscles Helper"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "bone_constraint"

    def draw(self, context):
        layout = self.layout
        layout.operator("rigidbody.set_unity_muscles")
        layout.operator("rigidbody.clear_unity_muscles")


def register():
    bpy.utils.register_class(SetUnityMusclesConstraint)
    bpy.utils.register_class(ClearUnityMusclesConstraint)
    bpy.utils.register_class(UnityMusclesHelperPanel)


def unregister():
    bpy.utils.unregister_class(SetUnityMusclesConstraint)
    bpy.utils.unregister_class(ClearUnityMusclesConstraint)
    bpy.utils.unregister_class(UnityMusclesHelperPanel)


if __name__ == "__main__":
    register()
