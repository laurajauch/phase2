from plot import *
from RefineS import *
from RefineNS import *
from Save import *
from Load import *
from Form import *


class Transition:
   def prompt(self):
      return "You can now: plot, refine, save, load, or exit. \n> "
   
   def handle(self, selection):
      if selection == 'plot':
         return Plot()
      elif selection == 'refine':
         print Form.Instance().getData()[0]
         if Form.Instance().getData()[0] == 'Stokes':
            return RefineS()
         else:
            return RefineNS()
      elif selection == 'save':
         return Save()
      elif selection == 'load':
         return Load()
      else:
         print "Input not understood."
      return self
