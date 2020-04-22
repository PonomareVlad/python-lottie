Python Lottie
=============

A Python framework to work with Lottie files and Telegram animated stickers.


Scripts
-------

* `bin/lottie_convert.py`

  Script that can convert between several formats passing through lottie (see table under Supported Formats)

* `bin/lottie_cat.py`

  Prints the given lottie file into a human-readable format

* `bin/lottie_diff.py`

  Shows a side-by-side diff of the human-readable rendition of two lottie files

* `bin/raster_palette.py`

  Shows the palette of a raster image, to use with `bin/lottie_convert.py`

* `bin/lottie_color.py`

  Converts a CSS color into a normalized array, as used in lottie

* `bin/jsoncat.py`

  Pretty prints a JSON file (useful to debug / diff lottie files)

* `bin/jsondiff.py`

  Pretty prints two JSON files side by side, highlighting differences (useful to debug / diff lottie files)

* `bin/lottie_cat.py`

  Pretty prints a lottie file with more readable annotations (useful to debug / diff lottie files)

* `bin/lottie_diff.py`

  Pretty prints two lottie files side by side, highlighting differences (useful to debug / diff lottie files)

* `bin/tgs_check.py`

  Checks a lottie or tgs file to see if it's compatible with telegram stickers


Installation
------------


### Synfig

There's a Synfig studio plugin to export telegram stickers.
To install, just copy (or symlink) ./addons/synfig/tgs-exporter
into the synfig plugin directory.
You might have to copy ./lib/lottie in there as well.

You can download a zipfile from http://mattia.basaglia.gitlab.io/python-lottie/downloads.html


### Inkscape

There are some import/export extensions for inkscape.

Just copy (or symlink) the files under ./addons/inkscape to the inkscape extension
directory.
On my system that's ~/.config/inkscape/extensions/ but you can double check from
Inkscape: Edit > Preferences... > System > User extensions

Note that the extensions require Python 3.
If they are run with a python 2 interpreter, they will try to run themselves using `python3`.

They also need the lottie framework to be in the python path, otherwise you can manually
set the path on the import/export dialogues.

See also https://inkscape.org/~mattia.basaglia/%E2%98%85tgslottie-importexport

You can download a zipfile from http://mattia.basaglia.gitlab.io/python-lottie/downloads.html


### Blender

There are some export addons for blender.

Copy (or symlink) the files under ./addons/blender to the Blender extension
directory.

On my system that's ~/.config/blender/2.80/scripts/addons/ you can check available
paths through the Blender Python console:

    import addon_utils; print(addon_utils.paths())

You can also install the addon from Blender using the zipfile created by `make`.

You can download a zipfile from http://mattia.basaglia.gitlab.io/python-lottie/downloads.html


### Pip

You can install from pypi:

    pip install lottie

from git:

    pip install git+https://gitlab.com/mattia.basaglia/python-lottie.git@master

for the source directory:

    pip install /path/to/the/sources # this is the path where setup.py is located


Requirements
------------

Python 3.


### Optional Requirements

In order to provide lean installations, this framework doesn't have dependencies
for its core functionality.

To add support for extra formats or advanced functionality, you can install
additional packages.

These requirements are declared as extra in the Pypi package,
follows a table listing dependencies and features


| Packages                                      | Extra | Feature                                                   |
|-----------------------------------------------|-------|-----------------------------------------------------------|
| `pillow`                                      | images| To load image assets                                      |
| `cairosvg`                                    | PNG   | To export PNG / PDF / PS                                  |
| `cairosvg`, `pillow`                          | GIF   | To export GIF and animated WebP                           |
| `fonttools`                                   | text  | To render text as shapes                                  |
| `grapheme`                                    | emoji | Adding emoji support to text rendering                    |
| `cairosvg`, `numpy`, Python OpenCV 2          | video | To export video                                           |
| `pillow`, `pypotrace>=0.2`, `numpy`, `scipy`  | trace | To convert raster images into vectors                     |
| `coverage`                                    |       | To show unit test coverage, used optionally by `test.sh`  |


If intalling from pip, you can install optional requirements like so:

    pip install lottie[GIF]

The above example will ensure `cairosvg` and `pillow` are installed.
For more details see https://pip.pypa.io/en/latest/reference/pip_install/#examples.

For convenience, an additional extra requirements is defined,
so you can install all dependencies at once:

    pip install lottie[all]


Features
--------

Here is a list of features of the lottie python framework:

* Loading compressed TGS and uncompressed lottie JSON
* Manipulation of lottie objects
* Simple animation presets (eg: shake, linear bounce)
* Bezier path animations (eg: follow path, making paths appear and disappear)
* Wave distortion animation (eg: for flags)
* Pseudo-3D rotations
* Animation easing functions
* Inverse Kinematic solver
* Pretty printing and comparison of lottie files
* Rendering text as shapes


## Supported Formats

| Format    | Import    | Import Animated   | Export    | Export Animated   |
|-----------|-----------|-------------------|-----------|-------------------|
| lottie    | 👍        | 👍                | 👍        | 👍                |
| tgs       | 👍        | 👍                | 👍        | 👍                |
| SVG       | 👍        | 👍                | 👍        | ⛔️                |
| SVGz      | 👍        | 👍                | 👍        | ⛔️                |
| PNG       | 👍        | 👍[^frames]       | 👍        | ⛔️                |
| Synfig    | 👍        | 👍                | 👍        | 👍                |
| WebP      | 👍        | 👍                | 👍        | 👍                |
| dotLottie | 👍        | 👍                | 👍        | 👍                |
| PostScript| ⛔️        | ⛔️                | 👍        | ⛔️                |
| PDF       | ⛔️        | ⛔️                | 👍        | ⛔️                |
| BMP       | 👍        | 👍[^frames]       | ⛔️        | ⛔️                |
| GIF       | 👍        | 👍                | 👍        | 👍                |
| TIFF      | 👍        | 👍                | 👍        | 👍                |
| MP4       | ⛔️        | ⛔️                | 👍        | 👍                |
| AVI       | ⛔️        | ⛔️                | 👍        | 👍                |
| WebM      | ⛔️        | ⛔️                | 👍        | 👍                |
| HTML      | ⛔️        | ⛔️                | 👍        | 👍                |
| Blender   | 👍[^blend]| 👍[^blend]        | ⛔️        | ⛔️                |

[^frames]: Importing multiple images as frames

[^blend]: Conversion available as a Blender addon


Telegram Animated Stickers
--------------------------

I had to reverse engineer the format because Telegram couldn't be bothered
providing the specs.

A TGS file is a gzip compressed JSON, the JSON data is described here:
https://mattia.basaglia.gitlab.io/python-lottie/group__Lottie.html#lottie_json

### Making your own exporters converters

#### Lottie format

If you can get the source image into lottie format, that's 90% of the work done.

I've created Python classes based the format schema and after effects documentation, which
output the correct json. Eg:

    foo = lottie.Animation()
    # ...
    json.dump(foo.to_dict(), output_file)

I'm also creating a proper documentation for the format, see:
https://mattia.basaglia.gitlab.io/tgs/group__Lottie.html#details

#### TGS changes

Nothing major, just ensure the root JSON object has `tgs: 1`

#### Gzipping

The tgs file is the JSON described above compressed into a gzip,
and renamed to .tgs


License
-------

AGPLv3+ https://www.gnu.org/licenses/agpl-3.0.en.html


Credits
-------

Copyright 2019 (C) Mattia Basaglia


Links
-----

### Documentation

http://mattia.basaglia.gitlab.io/python-lottie/index.html

### Code

https://gitlab.com/mattia.basaglia/python-lottie/

### Chat

https://t.me/tgs_stuff

### Download

http://mattia.basaglia.gitlab.io/python-lottie/downloads.html

Here you can download packages for pip, blender, and inkscape before they are released.
These packages always have the latest features but they might be unstable.


Supported After Effects Features
--------------------------------

Compare with http://airbnb.io/lottie/#/supported-features

### Legend

 * 👍 Supported
 * ❔ Unknown / untested
 * ⛔️ Not supported
 * **python-lottie** refers to this framework in general
 * **Telegram** refers to features supported by telegram animated stickers
 * **SVG** refers to the exported SVG images from this framework,
 features supported here will also reflect on other formats (such as video, png, and similar)


Telegram doesn't support everything in the Lottie format.
https://core.telegram.org/animated_stickers lists some things that are unsupported
but what is listed there isn't correct.

There are several things marked as unsupported in telegram animated stickers that are actually supported.



| **Shapes**                       | **python-lottie** | **Telegram**     | **SVG** |
|----------------------------------|-------------------|------------------|---------|
| Shape                            | 👍                | 👍               | 👍      |
| Ellipse                          | 👍                | 👍               | 👍      |
| Rectangle                        | 👍                | 👍               | 👍      |
| Rounded Rectangle                | 👍                | 👍               | 👍      |
| Polystar                         | 👍                | 👍[^unsuported]  | 👍      |
| Group                            | 👍                | 👍               | 👍      |
| Trim Path (individually)         | 👍                | 👍               | 👍      |
| Trim Path (simultaneously)       | 👍                | 👍               | 👍      |
| **Fills**                        | **python-lottie** | **Telegram**     | **SVG** |
| Color                            | 👍                | 👍               | 👍      |
| Opacity                          | 👍                | 👍               | 👍      |
| Radial Gradient                  | 👍                | 👍               | 👍      |
| Linear Gradient                  | 👍                | 👍               | 👍      |
| Fill Rule                        | 👍                | 👍               | 👍      |
| **Strokes**                      | **python-lottie** | **Telegram**     | **SVG** |
| Color                            | 👍                | 👍               | 👍      |
| Opacity                          | 👍                | 👍               | 👍      |
| Width                            | 👍                | 👍               | 👍      |
| Line Cap                         | 👍                | 👍               | 👍      |
| Line Join                        | 👍                | 👍               | 👍      |
| Miter Limit                      | 👍                | 👍               | 👍      |
| Dashes                           | 👍                | 👍               | 👍      |
| Gradient                         | 👍                | 👍[^unsuported]  | 👍      |
| **Transforms**                   | **python-lottie** | **Telegram**     | **SVG** |
| Position                         | 👍                | 👍               | 👍      |
| Position (separated X/Y)         | 👍                | 👍               | 👍      |
| Scale                            | 👍                | 👍               | 👍      |
| Rotation                         | 👍                | 👍               | 👍      |
| Anchor Point                     | 👍                | 👍               | 👍      |
| Opacity                          | 👍                | 👍               | 👍      |
| Parenting                        | 👍                | 👍               | 👍      |
| Skew                             | 👍                | ⛔️[^bug]         | 👍      |
| Auto Orient                      | 👍                | 👍[^unsuported]  | 👍      |
| **Interpolation**                | **python-lottie** | **Telegram**     | **SVG** |
| Linear Interpolation             | 👍                | 👍               | 👍      |
| Bezier Interpolation             | 👍                | 👍               | 👍      |
| Hold Interpolation               | 👍                | 👍               | 👍      |
| Spatial Bezier Interpolation     | 👍                | 👍               | 👍      |
| Rove Across Time                 | ⛔️                | ⛔️[^untested]    | ⛔️      |
| **Masks**                        | **python-lottie** | **Telegram**     | **SVG** |
| Mask Path                        | 👍                | 👍[^unsuported]  | 👍      |
| Mask Opacity                     | 👍                | 👍[^unsuported]  | 👍      |
| Add                              | 👍                | 👍[^unsuported]  | ⛔️      |
| Subtract                         | 👍                | 👍[^unsuported]  | ⛔️      |
| Intersect                        | 👍                | 👍[^unsuported]  | 👍      |
| Lighten                          | 👍                | 👍[^unsuported]  | ⛔️      |
| Darken                           | 👍                | 👍[^unsuported]  | ⛔️      |
| Difference                       | 👍                | 👍[^unsuported]  | ⛔️      |
| Expansion                        | 👍                | 👍[^unsuported]  | ⛔️      |
| Feather                          | 👍                | 👍[^unsuported]  | ⛔️      |
| **Mattes**                       | **python-lottie** | **Telegram**     | **SVG** |
| Alpha Matte                      | 👍                | ⛔️[^dok]         | ⛔️      |
| Alpha Inverted Matte             | 👍                | ⛔️[^dok]         | ⛔️      |
| Luma Matte                       | 👍                | ⛔️[^dok]         | ⛔️      |
| Luma Inverted Matte              | 👍                | ⛔️[^dok]         | ⛔️      |
| **Merge Paths**                  | **python-lottie** | **Telegram**     | **SVG** |
| Merge                            | ⛔️                | ⛔️[^untested]    | ⛔️      |
| Add                              | ⛔️                | ⛔️[^untested]    | ⛔️      |
| Subtract                         | ⛔️                | ⛔️[^untested]    | ⛔️      |
| Intersect                        | ⛔️                | ⛔️[^untested]    | ⛔️      |
| Exclude Intersection             | ⛔️                | ⛔️[^untested]    | ⛔️      |
| **Layer Effects**                | **python-lottie** | **Telegram**     | **SVG** |
| Fill                             | 👍                | ⛔️               | ⛔️      |
| Stroke                           | 👍                | ⛔️               | ⛔️      |
| Tint                             | 👍                | ⛔️               | ⛔️      |
| Tritone                          | 👍                | ⛔️               | ⛔️      |
| Levels Individual Controls       | 👍                | ⛔️               | ⛔️      |
| **Text** [^text]                 | **python-lottie** | **Telegram**     | **SVG** |
| Glyphs                           | 👍                | ⛔️               | ⛔️      |
| Fonts                            | 👍                | ⛔️               | ⛔️      |
| Transform                        | 👍                | ⛔️               | ⛔️      |
| Fill                             | 👍                | ⛔️               | 👍      |
| Stroke                           | 👍                | ⛔️               | ⛔️      |
| Tracking                         | ⛔️                | ⛔️               | ⛔️      |
| Anchor point grouping            | ⛔️                | ⛔️               | ⛔️      |
| Text Path                        | ⛔️                | ⛔️               | ⛔️      |
| Per-character 3D                 | ⛔️                | ⛔️               | ⛔️      |
| Range selector (Units)           | ⛔️                | ⛔️               | ⛔️      |
| Range selector (Based on)        | ⛔️                | ⛔️               | ⛔️      |
| Range selector (Amount)          | ⛔️                | ⛔️               | ⛔️      |
| Range selector (Shape)           | ⛔️                | ⛔️               | ⛔️      |
| Range selector (Ease High)       | ⛔️                | ⛔️               | ⛔️      |
| Range selector (Ease Low)        | ⛔️                | ⛔️               | ⛔️      |
| Range selector (Randomize order) | ⛔️                | ⛔️               | ⛔️      |
| expression selector              | ⛔️                | ⛔️               | ⛔️      |
| **Other**                        | **python-lottie** | **Telegram**     | **SVG** |
| Expressions                      | ⛔️                | ⛔️[^untested]    | ⛔️      |
| Images                           | 👍                | ⛔️               | 👍      |
| Precomps                         | 👍                | 👍               | 👍      |
| Time Stretch                     | 👍                | ⛔️               | ⛔️      |
| Time remap                       | 👍                | ⛔️[^dok]         | 👍      |
| Markers                          | ⛔️                | ⛔️[^untested]    | ⛔️      |
| 3D Layers                        | 👍                | ⛔️[^untested]    | ⛔️      |
| Repeaters                        | 👍                | 👍[^unsuported]  | 👍      |
| Solids                           | 👍                | 👍[^unsuported]  | 👍      |

[^text]: Note that **python-lottie** offers an alternative to lottie text layers, and can render
text as shapes, so that is supported everywhere

[^untested]: Marked as unsuported but I haven't tested it

[^bug]: Not listed as unsupported, maybe a bug?

[^dok]: Works on telegram desktop

[^unsuported]: Marked as unsupported
