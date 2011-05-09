###
### imagescaler - Scale image keeping Gamma
### Copyright (C) 2011 Sebastian Pipping <sebastian@pipping.org>
###
### This program is free software; you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation; either version 2 of the License, or
### (at your option) any later version.
###
### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
###
### You should have received a copy of the GNU General Public License
### along with this program; if not, write to the Free Software
### Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
###

from imagescaler.utils import set_rgba
from imagescaler.algorithms.bilinear_gimp import interpolate_bilinear_gimp
from imagescaler.algorithms.nearest_gimp import interpolate_nearest_gimp
from imagescaler.algorithms.cubic_gimp import interpolate_cubic_gimp


algorithm_data = (
    (interpolate_nearest_gimp, "None (Gimp)"),
    (interpolate_bilinear_gimp, "Bi-linear (Gimp)"),
    (interpolate_cubic_gimp, "Cubic (Gimp)"),
)

AVALIABLE_ALGORITHMS = [name for i, (f, name) in enumerate(algorithm_data)]

DEFAULT_ALGORITHM = 2


def scale_copy_layer(dst_layer, src_layer, interpol, gamma, env, layer_index, layer_count):

    def region(layer):
        dirty = True
        shadow = False
        return layer.get_pixel_rgn(0, 0, layer.width, layer.height, dirty, shadow)

    src_region = region(src_layer)
    dst_region = region(dst_layer)

    scaley = float(src_region.h) / float(dst_region.h)
    scalex = float(src_region.w) / float(dst_region.w)

    f, name = algorithm_data[interpol]

    n_todo = dst_region.h * dst_region.w
    n_done = 0
    for y in xrange(0, dst_region.h):
        for x in xrange(0, dst_region.w):
            yfrac = (y + 0.5) * scaley - 0.5
            sy = int(yfrac)
            yfrac = yfrac - sy

            xfrac = (x + 0.5) * scalex - 0.5
            sx = int(xfrac)
            xfrac = xfrac - sx

            rgba = f(src_region, src_layer, sx, sy, xfrac, yfrac, gamma)
            set_rgba(x, y, rgba, gamma, dst_region, dst_layer)

            n_done = n_done + 1
            percent = n_done * 100.0 / n_todo * (layer_index + 1 / float(layer_count) * 0.98)
            env.progress_update(percent / 100.0)


def scale_image(img, width, height, interpol, gamma, env):
    layer_backups = [l.copy() for l in img.layers]

    env.progress_init("Resizing image container")
    img.resize(width, height, 0, 0)
    
    env.progress_update(0)
    layer_count = len(img.layers)
    for i, dst_layer in enumerate(img.layers):
        env.progress_init("Resizing layer container")
        dst_layer.resize(width, height, 0, 0)

        env.progress_init("Scaling layer %d of %d" % (i + 1, layer_count))
        scale_copy_layer(dst_layer, layer_backups[i], interpol, gamma, env, i, layer_count)
        dst_layer.flush()
        
        env.delete(layer_backups[i])

    env.progress_update(98)

    for i, layer in enumerate(img.layers):
        layer.update(0, 0, layer.width, layer.height)

    env.progress_update(100)
