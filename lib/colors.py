import numpy as _np

def clist(num=100):
  """ returns a colorlist of len=35*repeat (default is 300),
 for every value of repeat, the 35 colors repeat in case you
 need more than 185 colors, use repeat > 5"""
  rng = _np.linspace(.3,1,5)
  ptrns = _np.array([[0.,0.,0.], 
      [1.,0.,0.], [0.,0.,1.], [0.,1.,0.],
      [0.,1.,1.], [1.,0.,1.], [0.9,0.9,0]])
  colors = []
  for x in xrange(num/len(ptrns) + num % len(ptrns)):
    for c in rng[::-1]:
      for p in ptrns: 
        colors.append(tuple(p*c))
  return _np.array(colors)
    

