
.. module:: color

*******************
Module :mod:`color`
*******************


Color models
============

PostScript provides different color models. They are available to PyX by
different color classes, which just pass the colors down to the PostScript
level. This implies, that there are no conversion routines between different
color models available. However, some color model conversion routines are
included in Python's standard library in the module ``colorsym``. Furthermore
also the comparison of colors within a color model is not supported, but might
be added in future versions at least for checking color identity and for
ordering gray colors.

There is a class for each of the supported color models, namely ``gray``,
``rgb``, ``cmyk``, and ``hsb``. The constructors take variables appropriate for
the color model. Additionally, a list of named colors is given in appendix
:ref:`colorname`.


Example
=======

   ::

      from pyx import *

      c = canvas.canvas()

      c.fill(path.rect(0, 0, 7, 3), [color.gray(0.8)])
      c.fill(path.rect(1, 1, 1, 1), [color.rgb.red])
      c.fill(path.rect(3, 1, 1, 1), [color.rgb.green])
      c.fill(path.rect(5, 1, 1, 1), [color.rgb.blue])

      c.writeEPSfile("color")


The file ``color.eps`` is created and looks like:

.. _fig_color:
.. figure:: color.*
   :align:  center

   Color example


Color gradients
===============

The color module provides a class ``gradient`` for continous transitions between
colors. A list of named gradients is available in appendix :ref:`gradientname`.


.. class:: gradient(min=0, max=1)

   This class provides the methods for the ``gradient``. Different initializations
   can be found in ``lineargradient`` and ``functiongradient``.

   *min* and *max* provide the valid range of the arguments for ``getcolor``.


   .. function:: getcolor(parameter)

      Returns the color that corresponds to *parameter* (must be between *min* and
      *max*).


   .. function:: select(index, n_indices)

      When a total number of *n_indices* different colors is needed from the gradient,
      this method returns the *index*-th color.


.. class:: lineargradient(startcolor, endcolor, min=0, max=1)

   This class provides a linear transition between two given colors. The linear
   interpolation is performed on the color components of the specific color model.

   *startcolor* and *endcolor* must be colors of the same color model.


.. class:: functiongradient(functions, type, min=0, max=1)

   This class provides an arbitray transition between colors of the same color
   model.

   *type* is a string indicating the color model (one of ``"cmyk"``, ``"rgb"``,
   ``"hsb"``, ``"grey"``)

   *functions* is a dictionary that maps the color components onto given functions.
   E.g. for ``type="rgb"`` this dictionary must have the keys ``"r"``, ``"g"``, and
   ``"b"``.


Transparency
============


.. class:: transparency(value)

   Instances of this class will make drawing operations (stroking, filling) to
   become partially transparent. *value* defines the transparency factor in the
   range ``0`` (opaque) to ``1`` (transparent).

   Transparency is available in PDF output only since it is not supported by
   PostScript. However, for certain ghostscript devices (for example the pdf
   backend as used by ps2pdf) proprietary PostScript extension allows for
   transparency in PostScript code too. PyX creates such PostScript proprietary
   code, but issues a warning when doing so.

