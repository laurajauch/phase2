from PyCamellia import *
from Form import *


class RefineS:
   def prompt(self):
      self.form = Form.Instance().get()
      return "Would you like h-auto, p-auto, h-manual or p-manual refinement? \n> "
   
   def handle(self, selection): 
      energyError = self.form.solution().energyErrorTotal() 
      mesh = self.form.solution().mesh()
   
      if selection == 'h-auto':
         print "Automatically refining in h..."
         self.form.hRefine() 
         self.form.solve() 
         energyError = self.form.solution().energyErrorTotal()
         elementcount = mesh.numActiveElements()
         globalDofCount = mesh.numGlobalDofs()
                 
      elif selection == 'p-auto':
         print "Automatically refining in p..."
         self.form.pRefine()
         self.form.solve() 
         energyError = self.form.solution().energyErrorTotal()
         elementcount = mesh.numActiveElements()
         globalDofCount = mesh.numGlobalDofs()
      
      elif selection == 'h-manual':
         cellIDs = mesh.getActiveCellIDs()
         print "Your active cells are: "
         print cellIDs
         refineCell = raw_input("Which cells would you like to refine? (Ex. 1 2 4) \n> ")
         if refineCell == 'exit':
            return 0
         refineCell = refineCell.split()
         refineCell = map(int, refineCell)
         self.form.solution().mesh().hRefine(refineCell) 
         self.form.solve() 
         energyError = self.form.solution().energyErrorTotal()
         elementcount = mesh.numActiveElements()
         globalDofCount = mesh.numGlobalDofs()
        
      elif selection == 'p-manual':
         cellIDs = mesh.getActiveCellIDs()
         print "Your active cells are: "
         print cellIDs
         refineCell = raw_input("Which cells would you like to refine? (Ex. 1 2 4) \n> ")
         if refineCell == 'exit':
            return 0
         refineCell = refineCell.split()
         refineCell = map(int, refineCell)
         self.form.solution().mesh().pRefine(refineCell) 
         self.form.solve() 
         energyError = self.form.solution().energyErrorTotal()
         elementcount = mesh.numActiveElements()
         globalDofCount = mesh.numGlobalDofs()
      
      else:
         print "Input not understood"
         return self
      
      print("Mesh has %i elements and %i degrees of freedom." % (elementcount, globalDofCount))
      print("Energy error after refinement: %0.3f" % (energyError))
     
      from Transition import Transition
      return Transition()
