
from main import *
from solver import *

class plot: #So to get the info to plot, refine we pass in the form object from above...?
   
   def prompt(self):
         return "What would you like to plot (u1, u2, p, stream function, mesh or error)? \n>"
   
   def handle(self, selection): 
      print "Plotting %s..." % selection
      #use .getCellValues(mesh, cellID, refPoints) 
      #refPoints in the form [[-1,0],[1,0]...] 
      #returns a tuple (value -list of floats, physical points)
      pass
