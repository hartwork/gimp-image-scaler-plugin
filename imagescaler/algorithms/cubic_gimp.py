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


def cubic_spline_fit(dx, pt0, pt1, pt2, pt3):
    return float((((( -pt0 + 3 * pt1 - 3 * pt2 + pt3 ) * dx +
            ( 2 * pt0 - 5 * pt1 + 4 * pt2 - pt3 ) ) * dx +
            ( -pt0 + pt2 ) ) * dx + (pt1 + pt1) ) / 2.0)


def interpolate_cubic_gimp(src_region, src_layer, sx, sy, xfrac, yfrac, gamma):
    # TODO Pixel positions translated correctly?
    rows = list()
    for ry in xrange(0, 4):
        rows.append(list())
        for rx in xrange(0, 4):
            rgba = get_rgba(sx - 1 + rx, sy - 1 + ry, gamma, src_region, src_layer)   
            rows[ry].extend(rgba)
    s0, s1, s2, s3 = rows

    p0 = cubic_spline_fit(xfrac, s0[3], s0[7], s0[11], s0[15])
    p1 = cubic_spline_fit(xfrac, s1[3], s1[7], s1[11], s1[15])
    p2 = cubic_spline_fit(xfrac, s2[3], s2[7], s2[11], s2[15])
    p3 = cubic_spline_fit(xfrac, s3[3], s3[7], s3[11], s3[15])

    alphasum = cubic_spline_fit(yfrac, p0, p1, p2, p3)

    pixel = [0, 0, 0, 0]

    if alphasum > 0:
        for b in xrange(0, 3):
            p0 = cubic_spline_fit(xfrac,
                                    s0[0 + b] * s0[ 3], s0[ 4 + b] * s0[7],
                                    s0[8 + b] * s0[11], s0[12 + b] * s0[15])
            p1 = cubic_spline_fit(xfrac,
                                    s1[0 + b] * s1[ 3], s1[ 4 + b] * s1[7],
                                    s1[8 + b] * s1[11], s1[12 + b] * s1[15])
            p2 = cubic_spline_fit(xfrac,
                                    s2[0 + b] * s2[ 3], s2[ 4 + b] * s2[7],
                                    s2[8 + b] * s2[11], s2[12 + b] * s2[15])
            p3 = cubic_spline_fit(xfrac,
                                    s3[0 + b] * s3[ 3], s3[ 4 + b] * s3[7],
                                    s3[8 + b] * s3[11], s3[12 + b] * s3[15])

            sum = cubic_spline_fit(yfrac, p0, p1, p2, p3) / alphasum

            pixel[b] = CLAMP(sum, 0, 255);

        pixel[3] = CLAMP(alphasum, 0, 255);

    return pixel
