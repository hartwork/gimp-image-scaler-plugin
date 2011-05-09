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


def weighted_sum(dx, dy, s00, s10, s01, s11):
    return ((1 - dy) * ((1 - dx) * s00 + dx * s10) + dy * ((1 - dx) * s01 + dx * s11))


def interpolate_bilinear_gimp(src_region, src_layer, sx, sy, xfrac, yfrac, gamma):
    # TODO Pixel positions translated correctly?
    p1 = get_rgba(sx,     sy,     gamma, src_region, src_layer)
    p2 = get_rgba(sx + 1, sy,     gamma, src_region, src_layer)
    p3 = get_rgba(sx    , sy + 1, gamma, src_region, src_layer)
    p4 = get_rgba(sx + 1, sy + 1, gamma, src_region, src_layer)

    pixel = [0, 0, 0, 0]

    if src_layer.has_alpha:
        alphasum = weighted_sum(xfrac, yfrac, p1[3], p2[3], p3[3], p4[3])
        if alphasum > 0:
            for b in xrange(0, 3):
                sum = weighted_sum(xfrac, yfrac,
                        p1[b] * p1[3], p2[b] * p2[3],
                        p3[b] * p3[3], p4[b] * p4[3])
                sum = sum / float(alphasum);
    
                pixel[b] = CLAMP(sum, 0, 255)
    
            pixel[3] = CLAMP(alphasum, 0, 255)
    else:
        for b in xrange(0, 3):
            sum = weighted_sum(xfrac, yfrac, p1[b], p2[b], p3[b], p4[b])
            pixel[b] = CLAMP(sum, 0, 255)
        pixel[3] = 255
    
    return pixel
