from main import *
from solver import *
from Form import *
from matplotlib import *
from numpy import *
import matplotlib.pyplot as plt

class plot: #So to get the info to plot, refine we pass in the form object from above...?
   
   def prompt(self):
      self.form = Form.Instance().get()
      return "What would you like to plot (u1, u2, p, stream function, mesh or error)? \n>"
   
   def handle(self, selection): 
      print "Plotting %s..." % selection
      mesh = self.form.solution().mesh()
      refCellVertexPoints = [[-1.,-1.],[1.,-1.],[1.,1.],[-1.,1.]] #update these based on the size
      aCIDs = mesh.getActiveCellIDs()

      if selection == 'u1':
         u1_soln = Function.solution(form.u(1), form.solution())
         for cellID in aCIDs:
            (values, points) = u1_soln.getCellValues(mesh, cellID,refCellVertexPoints)
      if selection == 'u2': 
         u2_soln = Function.solution(form.u(2), form.solution())
         for cellID in aCIDs:
            (values, points) = u2_soln.getCellValues(mesh, cellID,refCellVertexPoints)

      if selection == 'p':
         p_soln = Function.solution(form.p(), form.solution())
         for cellID in aCIDs:
            (values, points) = p_soln.getCellValues(mesh, cellID,refCellVertexPoints) 

      if selection == 'stream function':
         pass

      if selection == 'mesh':
         meshX = []
         meshY = []
         tempCell = []
         #for each active cell
         for cellID in aCIDs:
            tempCell = mesh.verticesForCell(cellID)
            #for each separate vertex of the cell
            for vert in tempCell:
               meshX.append(vert[0]) #get the x value for the vertex
               meshY.append(vert[1])
               
         #dummy color values for the plot as to be 0
         colA = zeros((len(meshX)-1, len(meshY)-1))

         c = plt.pcolormesh(array(meshX), array(meshY), colA, edgecolors='k', linewidths=2, 
                           cmap='bwr', vmin='-100', vmax='100') 

         plt.title('---The Mesh---')
         plt.xticks(meshX)
         plt.yticks(meshY)
         plt.show()

      if selection == 'error':
         pass

#returns a tuple (values -list of floats, physical points)
      #matplotlib it! - pcolor or pcolormesh?
      return transition()
