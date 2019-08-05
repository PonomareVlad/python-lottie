import os
import sys
import math
from dataclasses import dataclass

sys.path.append(os.path.dirname(__file__))
import tgs
from tgs import NVector

import bpy
import bpy_extras
import mathutils


@dataclass
class RenderOptions:
    scene: bpy.types.Scene
    line_width: float = 0
    camera_angles: NVector = NVector(0, 0, 0)

    @property
    def camera(self):
        return scene.camera

    def vector_to_camera_norm(self, vector):
        return NVector(*bpy_extras.object_utils.world_to_camera_view(
            self.scene,
            self.scene.camera,
            vector
        ))

    def vpix3d(self, vector):
        v3d = self.vector_to_camera_norm(vector)
        v3d.x *= self.scene.render.resolution_x
        v3d.y *= -self.scene.render.resolution_y
        return v3d

    def vpix(self, vector):
        v2d = self.vpix3d(vector)
        v2d.components.pop()
        return v2d

    def v_relative(self, obj, vector):
        return (
            self.vpix3d(obj.matrix_world @ vector) -
            self.vpix3d(obj.matrix_world @ mathutils.Vector([0, 0, 0]))
        )

    def get_xyz(self, vector):
        x = 0
        y = 1
        z = 2
        # TODO handle this properly
        if round(self.camera_angles.x) == 90:
            y, z = z, y
        return NVector(vector[x], vector[y], vector[z])

    def get_xy(self, vector):
        return NVector(*self.get_xyz(vector).components[:2])


def curve_to_shape(obj, parent, ro):
    g = parent.add_shape(tgs.objects.Group())
    g.name = obj.name

    for spline in obj.data.splines:
        sh = tgs.objects.Path()
        g.add_shape(sh)
        bez = sh.shape.value = tgs.objects.Bezier()
        bez.closed = spline.use_cyclic_u
        if spline.type == "BEZIER":
            for point in spline.bezier_points:
                vert = point.co
                in_t = point.handle_left - vert
                out_t = point.handle_right - vert
                #vert = ro.v_relative(obj, point.co)
                #in_t = ro.v_relative(obj, point.handle_left) - vert
                #out_t = ro.v_relative(obj, point.handle_right) - vert
                bez.add_point(NVector(*vert[:]), NVector(*in_t[:]), NVector(*out_t[:]))
        else:
            for point in spline.points:
                #bez.add_point(ro.v_relative(obj, point.co[:]))
                bez.add_point(NVector(*point.co[:]))

    if obj.data.fill_mode != "NONE":
        fillc = obj.active_material.diffuse_color
        fill = tgs.objects.Fill(NVector(*fillc[:-1]))
        fill.opacity.value = fillc[-1] * 100
        g.add_shape(fill)

    if ro.line_width > 0:
        strokec = obj.active_material.line_color
        stroke = tgs.objects.Stroke(NVector(*strokec[:-1]), ro.line_width)
        stroke.opacity.value = fillc[-1] * 100
        g.add_shape(stroke)
    return g


def object_to_shape(obj, parent, ro):
    g = None

    if obj.type == "CURVE":
        g = curve_to_shape(obj, parent, ro)

    if g:
        g.transform.position.value = ro.get_xy(obj.location)
        #g.transform.position.value = ro.vpix(obj.location)
        g.transform.scale.value = ro.get_xy(obj.scale) * 100
        g.transform.rotation.value = -ro.get_xyz(obj.rotation_euler).z/math.pi*180


def collection_to_group(collection, parent, ro: RenderOptions):
    g = tgs.objects.Group()
    parent.add_shape(g)
    g.name = collection.name

    # TODO sort by z
    for obj in collection.children:
        collection_to_group(obj, g, ro)

    for obj in collection.objects:
        object_to_shape(obj, g, ro)

    return g


def scene_to_tgs(scene):
    animation = tgs.objects.Animation()
    animation.in_point = scene.frame_start
    animation.out_point = scene.frame_end
    animation.framerate = scene.render.fps
    animation.width = scene.render.resolution_x
    animation.height = scene.render.resolution_y
    animation.name = scene.name
    layer = animation.add_layer(tgs.objects.ShapeLayer())

    ro = RenderOptions(scene)
    if scene.render.use_freestyle:
        ro.line_width = scene.render.line_thickness
    else:
        ro.line_width = 0
    ro.camera_angles = NVector(*scene.camera.rotation_euler) * 180 / math.pi

    view_frame = scene.camera.data.view_frame(scene=scene)
    camera_p1 = NVector(*view_frame[0][:-1])
    camera_size = camera_p1 - NVector(*view_frame[2][:-1])

    g = collection_to_group(scene.collection, layer, ro)

    layer.transform.scale.value.x *= scene.render.resolution_x / (camera_size.x or 1)
    layer.transform.scale.value.y *= -scene.render.resolution_y / (camera_size.y or 1)
    layer.transform.position.value.y += animation.height
    layer.transform.position.value += ro.vpix(mathutils.Vector([0, 0, 0]))

    return animation