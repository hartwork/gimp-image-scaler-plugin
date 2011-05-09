###
### imagescaler - Gamma-correct image scaler
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


# Eric Brasseur: Gamma error in picture scaling
# http://www.4p8.com/eric.brasseur/gamma.html


def exp2linear(pixel, gamma):
    return ((pixel / 255.0)**float(gamma)) * 255


def linear2exp(linear, gamma):
    return ((linear / 255.0)**(1.0 / gamma)) * 255


def rgb2s(rgb, gamma):
    return ''.join(chr(linear2exp(e, gamma)) for e in rgb)


def rgba2s(rgba, gamma):
    return ''.join(chr(linear2exp(e, gamma)) for e in rgba)


def s2rgba(s, gamma):
    num = [ord(c) for c in s]
    if len(num) == 3:
        num.append(255)
    return [exp2linear(c, gamma) for c in num]


def CLAMP(v, _min, _max):
    return max(_min, min(v, _max))


def set_rgba(x, y, rgba, gamma, region, layer):
    if layer.has_alpha:
        region[x, y] = rgba2s(rgba, gamma)
    else:
        region[x, y] = rgb2s(rgba[0:3], gamma)


def get_rgba(x, y, gamma, region, layer):
    x = CLAMP(x, 0, region.w - 1)
    y = CLAMP(y, 0, region.h - 1)
    return s2rgba(region[x, y], gamma)
