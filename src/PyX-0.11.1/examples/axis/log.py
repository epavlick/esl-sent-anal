import math
from pyx import *
from pyx.graph import axis

# we here use parters and texters which are explained in the examples below
log2parter = axis.parter.log([axis.parter.preexp([axis.tick.rational(1)], 4),
                              axis.parter.preexp([axis.tick.rational(1)], 2)])
log2texter = axis.texter.exponential(nomantissaexp=r"{2^{%s}}",
                                     mantissamax=axis.tick.rational(2))

g = graph.graphxy(width=10,
    x=axis.log(min=1, max=1024),
    y=axis.log(min=1, max=1024, parter=log2parter),
    y2=axis.log(min=1, max=1024, parter=log2parter, texter=log2texter))

g.writeEPSfile("log")
g.writePDFfile("log")
