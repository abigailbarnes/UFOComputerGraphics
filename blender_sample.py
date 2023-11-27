import os
import numpy as np
import bpy
import bmesh
from mathutils import Vector, Euler
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from interpolation import BSpline

# Example calling this file from the command line:
# /Applications/Blender.app/Contents/MacOS/blender /Users/abigailbarnes/cmsc23700/final_project/blank.blend --background --python blender_sample.py
# 

class TriangleMesh():
    def __init__(self, obj_file):
        # render mesh with/without edges (True for with edges)
        self.use_freestyle = False
        bpy.data.scenes['Scene'].render.use_freestyle = self.use_freestyle
        if self.use_freestyle:
            bpy.data.linestyles["LineStyle"].thickness = 0.8 # line thickness
        bpy.data.scenes['Scene'].use_nodes = True

        # load in the mesh object
        self.mesh = self.load_obj(obj_file)

        # initialize mesh postion, rotation and material
        self.mesh_settings(self.mesh)


    def load_obj(self, obj_file):
        bpy.ops.import_scene.obj(filepath=obj_file, axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl", use_edges=True,
                                 use_smooth_groups=True, use_split_objects=False, use_split_groups=False,
                                 use_groups_as_vgroups=False, use_image_search=True, split_mode='ON')
        ob = bpy.context.selected_objects[0]
        if self.use_freestyle:
            self.__mark_all_edges_freestyle(ob)
        return ob
    

    def __mark_all_edges_freestyle(self, mesh):
        for edge in mesh.data.edges:
            edge.use_freestyle_mark = True


    def mesh_settings(self, mesh):
        # apply scale
        mesh.scale = [1,1,1]
        # apply rotations
        mesh.rotation_euler.x = 1.57
        mesh.rotation_euler.y = 0
        mesh.rotation_euler.z = -1.65

        # shift bottom vertex to sit on zero (puts the mesh on the ground plane, you may remove if you want)
        mesh.data.update()
        bpy.context.view_layer.update()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        vertices = np.array([(mesh.matrix_world @ v.co) for v in mesh.data.vertices])
        mesh.location = Vector((0, 0, mesh.location.z - min(vertices[:, 2])))
        
        # further translate mesh position
        mesh.location.x += 0
        mesh.location.y += 0
        mesh.location.z += 0

        # hard code color and alpha values
        r, g, b, a = 0.537, 0.812, 0.941, 1

        #pick three different colors, bspline for red, blue, and green values
        #get value for bspline for frame one, two, three, etc
        #knots are going to be time and control points based on the values that you want

        # now add material
        mat = bpy.data.materials["Default OBJ"]
        mesh.data.materials.pop()
        # set color
        principled = mat.node_tree.nodes["Principled BSDF"]
        principled.inputs["Base Color"].default_value = (r, g, b, a)
        # update material
        mesh.data.materials.append(mat)


class Camera():
    def __init__(self):
        self.cam = self.render_settings()
        

    def render_settings(self):
        # hard code camera and lighting settings
        
        bpy.context.scene.cycles.device = "CPU"
        # bpy.data.scenes['Scene'].render.engine = self.cfg["engine"]
        bpy.context.scene.cycles.samples = 10

        # camera settings
        cam = bpy.data.scenes["Scene"].objects['Camera']
        cam.rotation_euler.x = 1.36
        cam.rotation_euler.y = 0
        cam.rotation_euler.z = 1.157
        cam.location.x = 6.6
        cam.location.y = -3
        cam.location.z = 2.49
        #cam.location.x = 5
        bpy.context.view_layer.update()

        # lighting
        objs = [x.name for x in bpy.data.objects]
        if 'light' in objs:
            bpy.data.objects['light'].data.materials['Material'].node_tree.nodes['Emission'].inputs['Strength'].default_value = 1.8
            bpy.data.objects['light'].data.materials['Material'].node_tree.nodes['Emission'].inputs['Color'].default_value = [0.8, 0.77, 0.8, 1]
            bpy.data.objects['light'].scale = bpy.data.objects['light'].scale * 1.5
            bpy.data.objects['light'].location.x = 6

        return cam

def select_obj(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

def setup_animation_keyframes(object_to_move, locations, rotations, n_frames):
        """
        insert keyframes along path
        """
        select_obj(object_to_move)
        bpy.data.scenes["Scene"].frame_end = int(n_frames - 1)
        f = 1

        '''if f == 10:
            object_to_move.edgeFlip'''

        for loc, rot in zip(locations, rotations):
            # put object at location
            object_to_move.location[0] = loc[0]
            object_to_move.location[1] = loc[1]
            object_to_move.location[2] = loc[2]

            # rotations
            object_to_move.rotation_euler[0] = rot[0]
            object_to_move.rotation_euler[1] = rot[1]
            object_to_move.rotation_euler[2] = rot[2]

            bpy.data.scenes["Scene"].frame_current = f
            object_to_move.keyframe_insert(data_path='location', frame=f)
            object_to_move.keyframe_insert(data_path="rotation_euler", frame=f)
            f += 1

if __name__ == "__main__":
    # Main code
    # set obj file to spot.obj in the data directory
    obj_file1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spot_edge_flipped.obj')
    obj_file2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'UFO.obj')
    #obj_file3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'cone.obj')
    print(f"obj file: {obj_file1}")
    print(f"obj file: {obj_file2}")
    #print(f"obj file: {obj_file3}")

    # set camera parameters
    cam = Camera()

    # load in obj file and get mesh object
    mesh1 = TriangleMesh(obj_file1)
    mesh2 = TriangleMesh(obj_file2)
    #mesh3 = TriangleMesh(obj_file3)

    # ---------- Render Mesh ---------- #
    # setup output file path
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'renders', 'spot_edge_flipped.png') # edit output path as needed
    bpy.data.scenes['Scene'].render.filepath = output_path

    # debug flag
    debug = False

    # animate flag
    animate = True

    # hard code locations
    n_frames = 500
    #n_frames = 100

    # example animations (moving either cam or mesh)
    # example camera animation
    # locations = zip([6.6]*n_frames, np.linspace(-6, 3, n_frames), [2.49]*n_frames)
    # rotations = zip([1.36]*n_frames, [0]*n_frames, [1.157]*n_frames)

    # example mesh animation
    #locations1 = zip([0]*n_frames, np.linspace(0, -3, n_frames), [0.7521]*n_frames)
    #locations1 = zip([-15.1739]*n_frames, np.linspace(0, 6.38438, n_frames), np.linspace(0, 2, n_frames))
    #rotations1 = zip([1.36]*n_frames, [0]*n_frames, np.linspace(1.157, 4, n_frames))
    #locations1 = zip([-15.1739]*n_frames, [6.38438]*n_frames, np.linspace(-3, 2, n_frames))

    #original code: locations1 = zip([0]*n_frames, np.linspace(0, -3, n_frames), [0.7521]*n_frames)

    #7
    #t = [0, 35, 60, 65, 75, 80, 100] # set some knots. change this.
    t = [0, 175, 300, 325, 375, 400, 500]
    #4
    #control_points = [6.38438, 6.38438, 5, 8]
    control_points = [6.38438, 6.38438, 5, 12]
    d = 2 # set the degree.5, 6.38438, 8]
    splines = BSpline(t, control_points, d)

    y = []
    for i in range(n_frames):
        y.append(splines.interp(i+1))

    rotations1 = zip([1.36]*n_frames, [0]*n_frames, np.linspace(1.157, 4, n_frames))
    #locations1 = zip([-15.1739]*n_frames, [6.38438]*n_frames, np.linspace(-3, 2, n_frames))
    locations1_x = [-15.1739]*n_frames
    locations1_z = np.linspace(-6, 2, n_frames)
    locations1 = zip(locations1_x, y, locations1_z)

    rotations2 =  zip([1.36]*n_frames, [0]*n_frames, np.linspace(1.157, 4, n_frames))
    #locations2 = [(-14.9143, 6.38438, 2) *n_frames]
    locations2_x = [-14.9143] * n_frames
    locations2_z = [2] * n_frames
    locations2= zip(locations2_x, y, locations2_z)



    #100 frames, first 70 cow -> ufo
    #last 30 

    #rotations3 = zip([1.36]*n_frames, [0]*n_frames, np.linspace(1.157, 4, n_frames))
    #locations3 = [(-14.9143, 6.38438, 2) * n_frames]

    if animate:
        # setup_animation_keyframes(cam.cam, locations, rotations, n_frames) # for camera
        setup_animation_keyframes(mesh1.mesh, locations1, rotations1, n_frames) # for mesh
        setup_animation_keyframes(mesh2.mesh, locations2, rotations2, n_frames)
        #setup_animation_keyframes(mesh3.mesh, locations3, rotations3, n_frames)
        Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output/animation_renders')).mkdir(parents=True, exist_ok=True)
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output/animation_renders', 'spot_edge_flipped.png') # edit output path as needed
        bpy.data.scenes['Scene'].render.filepath = output_path

    # render
    if not debug:
        bpy.ops.render.render(write_still=not animate, animation=animate)
    else:
        print('debugging...')
        bpy.ops.wm.save_as_mainfile(filepath='/tmp/debug.blend')
        # To debug, run the following code. This will open up the debug file in blender.
        # path/to/blender /tmp/debug.blend
        # For me this looks like:
        # /Applications/Blender.app/Contents/MacOS/blender /tmp/debug.blend
