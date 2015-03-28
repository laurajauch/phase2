from Transition import *
from Form import *
from PyCamellia import *

class RefineNS:
   def prompt(self):
      self.form = Form.Instance().get()
      print "refine Navier Stokes"
      return "Would you like h-auto, p-auto, h-manual or p-manual refinement? \n> "

   def handle(self, selection):
      mesh = self.form.solution().mesh()
      maxSteps = 10

      if selection == 'h-auto':
         print "Automatically refining in h..."
         self.form.hRefine()
         nonlinearSolve(maxSteps, self.form)
         energyError = self.form.solutionIncrement().energyErrorTotal()
         elementCount = mesh.numActiveElements()
         globalDofCount = mesh.numGlobalDofs()
        
      elif selection == 'p-auto':
         print "Automatically refining in p..."
         self.form.pRefine()
         nonlinearSolve(maxSteps, self.form)
         energyError = self.form.solutionIncrement().energyErrorTotal()
         elementCount = mesh.numActiveElements()
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
         print refineCell
         self.form.solution().mesh().hRefine(refineCell)
         nonlinearSolve(maxSteps, self.form)
         energyError = self.form.solutionIncrement().energyErrorTotal()
         elementCount = mesh.numActiveElements()
         globalDofCount = mesh.numGlobalDofs()
      
      elif selection == 'p-manual':
         cellIDs = mesh.getActiveCellIDs()
         print "Your active cells are: "
         print cellIDs
         refineCell = raw_input("Which cells would you like to refine? (Ex. 1 2 4) \n> ")
         if refineCell == 'exit':
            return 0
         refineCell = refineCell.split() #convert input to list
         refineCell = map(int, refineCell)
         self.form.solution().mesh().pRefine(refineCell)
         nonlinearSolve(maxSteps, self.form)
         energyError = self.form.solutionIncrement().energyErrorTotal()
         elementCount = mesh.numActiveElements()
         globalDofCount = mesh.numGlobalDofs()
      
      else:
         print "Input not understood"
         return self

      print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
      print("Energy error after refinement: %0.3f" % (energyError))
      
      return Transition()


   def nonlinearSolve(maxSteps, form):
       normOfIncrement = 1
       stepNumber = 0
       nonlinearThreshold = 1e-3
       while normOfIncrement > nonlinearThreshold and stepNumber < maxSteps:
           form.solveAndAccumulate()
           normOfIncrement = form.L2NormSolutionIncrement()
           print("L^2 norm of increment: %0.3f" % normOfIncrement)
           stepNumber += 1
