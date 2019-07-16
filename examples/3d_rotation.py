import sys
import os
import math
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.utils import animation as anutils
from tgs import NVector

an = objects.Animation(120)

layer = objects.ShapeLayer()
an.add_layer(layer)

# Build a sphere out of circles
balls = []
axes = [
    NVector(1, 0),
    NVector(0, 1),
]
for i in range(20):
    a = i/20 * math.pi * 2
    for axis in axes:
        g = layer.add_shape(objects.Group())
        b = g.add_shape(objects.Ellipse())
        b.size.value = NVector(20, 20)
        xz = axis * math.sin(a)*128
        pos = NVector(256+xz[0], 256+math.cos(a)*128, xz[1])
        b.position.value = pos
        balls.append(b)
        g.add_shape(objects.Fill(NVector(0, 1, 0)))

# Animate the circles using depth rotation
dr = anutils.DepthRotationDisplacer(NVector(256, 256, 0), 0, 120, 10, NVector(0, 2, -1))
for b in balls:
    dr.animate_point(b.position)

exporters.multiexport(an, "/tmp/3d_rotation")