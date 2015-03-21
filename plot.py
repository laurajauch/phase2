
from main import *
from solver import *

class plot: #So to get the info to plot, refine we pass in the form object from above...?
   
   def prompt(self):
         return "What would you like to plot (u1, u2, p, stream function, mesh or error)? \n>"
   
   def handle(self, selection): 
      print "Plotting %s..." % selection

      # we NEED to get a hold of the form

      refCellVertexPoints = [[-1.,-1.],[1.,-1.],[1.,1.],[-1.,1.]] #update these based on the size
      activeCellIDs = mesh.getActiveCellIDs()
      mesh = form.solution().mesh()

      if selecion == 'u1':
          u1_soln = Function.solution(form.u(1), form.solution())
          for cellID in activeCellIDs:
              (values, points) = u1_soln.getCellValues(mesh, cellID,refCellVertexPoints)
      if selection == 'u2': 
          u2_soln = Function.solution(form.u(2), form.solution())
          for cellID in activeCellIDs:
              (values, points) = u2_soln.getCellValues(mesh, cellID,refCellVertexPoints)

      if selection == 'p':
          pass

      if selection == 'stream function':
          pass

      if selection == 'mesh':
          pass

      if selection == 'error':
          pass

#returns a tuple (value -list of floats, physical points)
      #matplotlib it! - pcolor or pcolormesh?
