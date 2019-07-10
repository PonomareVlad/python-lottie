import re
from xml.etree import ElementTree
from .. import objects
from ..utils.nvector import NVector


ns_map = {
    "dc": "http://purl.org/dc/elements/1.1/",
    "cc": "http://creativecommons.org/ns#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "svg": "http://www.w3.org/2000/svg",
    "sodipodi": "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
    "inkscape": "http://www.inkscape.org/namespaces/inkscape",
}

for n, u in ns_map.items():
    ElementTree.register_namespace(n, u)

element_parsers = {}

color_table = {
    "black": [0, 0, 0, 1],
    "red": [1, 0, 0, 1],
    "lime": [0, 1, 0, 1],
    "yellow": [1, 1, 0, 1],
    "blue": [0, 0, 1, 1],
    "magenta": [1, 0, 1, 1],
    "cyan": [0, 1, 1, 1],
    "white": [1, 1, 1, 1],

    "green": [0, 0.8, 0, 1],
    "purple": [0.5, 0, 0.5, 1],
    "lightgrey": [0.8, 0.8, 0.8, 1],

    "pink": [1, 0.5, 0.5, 1],
}

nocolor = {"none", "transparent"}


def element_parser(name):
    def deco(func):
        element_parsers[name] = func
        return func
    return deco


def _qualified(ns, name):
    return "{%s}%s" % (ns_map[ns], name)


def _simplified(name):
    for k, v in ns_map.items():
        name = name.replace("{%s}" % v, k+":")
    return name


def _unqualified(name):
    return name.split("}")[-1]


def _parse_color(color):
    if re.match("^#[0-9a-fA-F]{6}$", color):
        return [int(color[1:3], 16) / 0xff, int(color[3:5], 16) / 0xff, int(color[5:7], 16) / 0xff, 1]
    if re.match("^#[0-9a-fA-F]{3}$", color):
        return [int(color[1], 16) / 0xf, int(color[2], 16) / 0xf, int(color[3], 16) / 0xf, 1]

    match = re.match("^rgba\s*\(\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9.eE]+)\s*\)$", color)
    if match:
        return [int(match[1])/255, int(match[2])/255, int(match[3])/255, float(match[4])]

    match = re.match("^rgb\s*\(\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*\)$", color)
    if match:
        return [int(match[1])/255, int(match[2])/255, int(match[3])/255, 1]

    # TODO more formats hsv() etc
    return color_table[color]


def _add_shapes(element, shapes, shape_parent):
    if "style" in element.attrib:
        style = dict(map(lambda x: x.split(":"), element.attrib["style"].split(";")))
    else:
        style = {}
    # TODO inherit style
    group = objects.Group()
    shape_parent.shapes.insert(0, group)
    for shape in shapes:
        group.add_shape(shape)

    # TODO opacity:
    fill_color = style.get("fill", element.attrib.get("fill", "black"))
    if fill_color not in nocolor:
        color = _parse_color(fill_color)
        fill = group.add_shape(objects.Fill(color[:3]))
        fill.opacity.value = color[3] * 100

    stroke_color = style.get("stroke", element.attrib.get("stroke", "none"))
    if stroke_color not in nocolor:
        stroke = objects.Stroke()
        group.add_shape(stroke)
        color = _parse_color(stroke_color)
        stroke.color.value = color[:3]
        stroke.opacity.value = color[3] * 100
        stroke.width.value = float(style.get("stroke-width", 1))
        linecap = style.get("stroke-linecap")
        if linecap == "round":
            stroke.line_cap = objects.shapes.LineCap.Round
        elif linecap == "butt":
            stroke.line_cap = objects.shapes.LineCap.Butt
        elif linecap == "square":
            stroke.line_cap = objects.shapes.LineCap.Square
        linejoin = style.get("stroke-linejoin")
        if linejoin == "round":
            stroke.line_cap = objects.shapes.LineJoin.Round
        elif linejoin == "bevel":
            stroke.line_cap = objects.shapes.LineJoin.Bevel
        elif linejoin in {"miter", "arcs", "miter-clip"}:
            stroke.line_cap = objects.shapes.LineJoin.Miter
        stroke.miter_limit = float(style.get("stroke-miterlimit", 0))
    # TODO transform
    return group


def _add_shape(element, shape, shape_parent):
    return _add_shapes(element, [shape], shape_parent)


@element_parser("g")
def parse_g(element, shape_parent):
    group = objects.Group()
    shape_parent.add_shape(group)
    group.name = element.attrib.get(_qualified("inkscape", "label"), element.attrib.get("id"))
    parse_svg_element(element, group)


@element_parser("ellipse")
def parse_ellipse(element, shape_parent):
    ellipse = objects.Ellipse()
    ellipse.position.value = [
        float(element.attrib["cx"]),
        float(element.attrib["cy"])
    ]
    ellipse.size.value = [
        float(element.attrib["rx"]),
        float(element.attrib["ry"])
    ]
    _add_shape(element, ellipse, shape_parent)


@element_parser("circle")
def parse_circle(element, shape_parent):
    ellipse = objects.Ellipse()
    ellipse.position.value = [
        float(element.attrib["cx"]),
        float(element.attrib["cy"])
    ]
    r = float(element.attrib["r"])
    ellipse.size.value = [r, r]
    _add_shape(element, ellipse, shape_parent)


@element_parser("line")
def parse_line(element, shape_parent):
    line = objects.Shape()
    line.vertices.value.add_point([
        float(element.attrib["x1"]),
        float(element.attrib["y1"])
    ])
    line.vertices.value.add_point([
        float(element.attrib["x2"]),
        float(element.attrib["y2"])
    ])
    _add_shape(element, line, shape_parent)


@element_parser("polyline")
def parse_line(element, shape_parent):
    line = objects.Shape()
    points = element.attrib["points"].split()
    for point in points:
        line.vertices.value.add_point(
            list(map(float, point.split(",")))
        )
    _add_shape(element, line, shape_parent)


class PathDParser:
    def __init__(self, d_string):
        self.path = objects.properties.Bezier()
        self.paths = [self.path]
        self.p = NVector(0, 0)
        self.la = None
        self.la_type = None
        self.tokens = list(map(self.d_subsplit, re.findall("[a-zA-Z]|[-+.0-9eE,]+", d_string)))
        self.add_p = True
        self.implicit = "M"

    def d_subsplit(self, tok):
        if tok.isalpha():
            return tok
        if "," in tok:
            return NVector(*map(float, tok.split(",")))
        return float(tok)

    def next_token(self):
        if self.tokens:
            self.la = self.tokens.pop(0)
            if isinstance(self.la, str):
                self.la_type = 0
            elif isinstance(self.la, NVector):
                self.la_type = 2
            else:
                self.la_type = 1
        else:
            self.la = None
        return self.la

    def parse(self):
        self.next_token()
        while self.la:
            if self.la_type == 0:
                parser = "_parse_" + self.la
                self.next_token()
                getattr(self, parser)()
            else:
                parser = "_parse_" + self.implicit
                getattr(self, parser)()
            self.next_token()

    def _push_path(self):
        self.path = objects.properties.Bezier()
        self.paths.append(self.path)

    def _parse_M(self):
        if self.la_type != 2:
            self.next_token()
            return
        self.p = self.la
        self.implicit = "L"
        if not self.add_p:
            self._push_path()
        self.add_p = True

    def _parse_m(self):
        if self.la_type != 2:
            self.next_token()
            return
        self.p += self.la
        self.implicit = "l"
        if not self.add_p:
            self._push_path()
        self.add_p = True

    def _rpoint(self, point, rel=None):
        return (point - (rel or self.p)).to_list() if point is not None else [0, 0]

    def _do_add_p(self, outp=None):
        if self.add_p:
            self.path.add_point(self.p.to_list(), [0, 0], self._rpoint(outp))
            self.add_p = False
        elif outp:
            rp = NVector(*self.path.vertices[-1])
            self.path.out_point[-1] = self._rpoint(outp, rp)

    def _parse_L(self):
        if self.la_type != 2:
            self.next_token()
            return
        self._do_add_p()
        self.p = self.la
        self.path.add_point(self.p.to_list(), NVector(0, 0), NVector(0, 0))
        self.implicit = "L"

    def _parse_l(self):
        if self.la_type != 2:
            self.next_token()
            return
        self._do_add_p()
        self.p += self.la
        self.path.add_point(self.p.to_list(), [0, 0], [0, 0])
        self.implicit = "l"

    def _parse_H(self):
        if self.la_type != 1:
            self.next_token()
            return
        self._do_add_p()
        self.p[0] = self.la
        self.path.add_point(self.p.to_list(), [0, 0], [0, 0])
        self.implicit = "H"

    def _parse_h(self):
        if self.la_type != 1:
            self.next_token()
            return
        self._do_add_p()
        self.p[0] += self.la
        self.path.add_point(self.p.to_list(), [0, 0], [0, 0])
        self.implicit = "h"

    def _parse_V(self):
        if self.la_type != 1:
            self.next_token()
            return
        self._do_add_p()
        self.p[1] = self.la
        self.path.add_point(self.p.to_list(), [0, 0], [0, 0])
        self.implicit = "V"

    def _parse_v(self):
        if self.la_type != 1:
            self.next_token()
            return
        self._do_add_p()
        self.p[1] += self.la
        self.path.add_point(self.p.to_list(), [0, 0], [0, 0])
        self.implicit = "v"

    def _parse_C(self):
        if self.la_type != 2:
            self.next_token()
            return
        pout = self.la
        self._do_add_p(pout)
        pin = self.next_token()
        self.p = self.next_token()
        self.path.add_point(
            self.p.to_list(),
            (pin - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "C"

    def _parse_c(self):
        if self.la_type != 2:
            self.next_token()
            return
        pout = self.p + self.la
        self._do_add_p(pout)
        pin = self.p + self.next_token()
        self.p += self.next_token()
        self.path.add_point(
            self.p.to_list(),
            (pin - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "c"

    def _parse_S(self):
        if self.la_type != 2:
            self.next_token()
            return
        pin = self.la
        self._do_add_p()
        handle = NVector(*self.path.in_point[-1])
        self.path.out_point[-1] = (-handle).to_list()
        self.p = self.next_token()
        self.path.add_point(
            self.p.to_list(),
            (pin - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "S"

    def _parse_s(self):
        if self.la_type != 2:
            self.next_token()
            return
        pin = self.la + self.p
        self._do_add_p()
        handle = NVector(*self.path.in_point[-1])
        self.path.out_point[-1] = (-handle).to_list()
        self.p += self.next_token()
        self.path.add_point(
            self.p.to_list(),
            (pin - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "s"

    def _parse_Q(self):
        if self.la_type != 2:
            self.next_token()
            return
        self._do_add_p()
        pin = self.la
        self.p = self.next_token()
        self.path.add_point(
            self.p.to_list(),
            (pin - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "Q"

    def _parse_q(self):
        if self.la_type != 2:
            self.next_token()
            return
        self._do_add_p()
        pin = self.p + self.la
        self.p += self.next_token()
        self.path.add_point(
            self.p.to_list(),
            (pin - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "q"

    def _parse_T(self):
        if self.la_type != 2:
            self.next_token()
            return
        self._do_add_p()
        handle = -(NVector(*self.path.in_point[-1]) - self.p) + self.p
        self.p = self.la
        self.path.add_point(
            self.p.to_list(),
            (handle - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "T"

    def _parse_t(self):
        if self.la_type != 2:
            self.next_token()
            return
        self._do_add_p()
        handle = -NVector(*self.path.in_point[-1]) + self.p
        self.p += self.la
        self.path.add_point(
            self.p.to_list(),
            (handle - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "t"

    def _parse_A(self):
        if self.la_type != 2:
            self.next_token()
            return
        self._do_add_p()
        rx = self.la
        ry = self.next_token()
        large = self.next_token()
        sweep = self.next_token()
        self.p = self.next_token()
        # TODO
        self.path.add_point(
            self.p.to_list(),
            [0, 0],
            [0, 0]
        )
        self.implicit = "A"

    def _parse_a(self):
        if self.la_type != 2:
            self.next_token()
            return
        self._do_add_p()
        rx = self.la
        ry = self.next_token()
        large = self.next_token()
        sweep = self.next_token()
        self.p += self.next_token()
        # TODO
        self.path.add_point(
            self.p.to_list(),
            [0, 0],
            [0, 0]
        )
        self.implicit = "a"

    def _parse_Z(self):
        self.path.close()
        self._push_path()

    def _parse_z(self):
        self.path.close()
        self._push_path()


@element_parser("path")
def parse_path(element, shape_parent):
    d_parser = PathDParser(element.attrib.get("d", ""))
    d_parser.parse()
    paths = []
    for path in d_parser.paths:
        p = objects.Shape()
        p.vertices.value = path
        paths.append(p)
    _add_shapes(element, paths, shape_parent)


def parse_svg_element(element, shape_parent):
    for child in element:
        tag = _unqualified(child.tag)
        if tag in element_parsers:
            element_parsers[tag](child, shape_parent)


def parse_svg_etree(etree):
    animation = objects.Animation()
    svg = etree.getroot()
    if "width" in svg.attrib and "height" in svg.attrib:
        animation.width = int(svg.attrib["width"])
        animation.height = int(svg.attrib["height"])
    else:
        _, _, animation.width, animation.height = map(int, svg.attrib["viewBox"].split(" "))
    animation.name = svg.attrib.get(_qualified("sodipodi", "docname"), svg.attrib.get("id"))
    layer = objects.ShapeLayer()
    animation.add_layer(layer)
    parse_svg_element(svg, layer)
    return animation


def parse_svg_file(file):
    return parse_svg_etree(ElementTree.parse(file))