###
### GIMP - The GNU Image Manipulation Program
### Copyright (C) 1995 Spencer Kimball and Peter Mattis
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

from imagescaler.utils import get_rgba, CLAMP


def interpolate_nearest_gimp(src_region, src_layer, sx, sy, xfrac, yfrac, gamma, cache_exp2linear):
    x = CLAMP(sx if (xfrac <= 0.5) else sx + 1, 0, src_region.w - 1)
    y = CLAMP(sy if (yfrac <= 0.5) else sy + 1, 0, src_region.h - 1)
    return get_rgba(x, y, gamma, src_region, src_layer, cache_exp2linear)
