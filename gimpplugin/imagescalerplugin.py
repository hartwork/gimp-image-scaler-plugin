###
### Gimp-Python - allows the writing of Gimp plugins in Python.
### Copyright (C) 1997 James Henstridge <james@daa.com.au>
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

from gimpfu import PF_STRING, PF_IMAGE, PF_INT, PF_OPTION, PF_FLOAT, register, gimp, main

from imagescaler.main import scale_image, AVALIABLE_ALGORITHMS, DEFAULT_ALGORITHM
from imagescaler.env import GimpEnv


PROC_NAME = 'python-fu-imagescaler'


def process(dummy, img, width, height, interpol, gamma):
    img.undo_group_start()
    scale_image(img, width, height, interpol, gamma, GimpEnv())
    img.undo_group_end()


register(
    PROC_NAME,
    "Scale Image keeping Gamma",
    "",
    "Sebastian Pipping <sebastian@pipping.org>",
    "Sebastian Pipping <sebastian@pipping.org>",
    "2011-05-09",
    "Scale Image _keeping Gamma...",
    "RGB*, GRAY*",
    [
        (PF_STRING, "dummy",    "DUMMY",         None),
        (PF_IMAGE,  "image",    "Target Image",  None),
        (PF_INT,    "width",    "Width",         100),
        (PF_INT,    "height",   "Height",        100),
        (PF_OPTION, "interplo", "Interpolation", DEFAULT_ALGORITHM, AVALIABLE_ALGORITHMS),
        (PF_FLOAT,  "gamma",    "Gamma",         gimp.gamma()),
    ],
    [],
    process,
    menu="<Image>/Image",
    domain=("gimp20-python", gimp.locale_directory))

main()
