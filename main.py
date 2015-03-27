from solver import *
from plot import *
from Form import *
import cPickle as pickle

class main: 

   def __init__(self):
      self.state = initial()
      selection = ""
      while selection != "exit":
         if isinstance(self.state, int): #if state is a number, quit
            break
         selection = raw_input(self.state.prompt())
         if(selection != "exit"):
            self.state = self.state.handle(selection.lower())
            
      print ("Exiting")

class initial:

   def prompt(self):
      return "You can now: create or load \n> "

   def handle(self, selection):
      if(selection == "create"):
         return solver_type()
      elif(selection == "load"):
         return load() #this should be whatever state handles loading
      else:
         print ("Input not understood")
         return self

class solver_type:

   def prompt(self):
      return "Would you like to solve Stokes or Navier-Stokes? \n> "

   def handle(self, selection):
      #determines what type of problem
      if(selection == "stokes"):
         return solver(False)
      elif(selection == "navier-stokes"):
         return solver(True)
      else:
         print ("Input not understood")
         return self
   
class refineNS:
   def prompt(self):
      self.form = Form.Instance().get()
      return "Would you like h-auto, p-auto, h-manual or p-manual refinement? \n>"

   def handle(self, selection):
      energyError = self.form.solutionIncrement().energyErrorTotal()
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
         refineCell = raw_input("Which cells would you like to refine? (Ex. 1 2 4) \n>")
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
         refineCell = raw_input("Which cells would you like to refine? (Ex. 1 2 4) \n>")
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
         return refineNS()

      print("Energy error after refinement: %0.3f" % (energyError))
      print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
      nextAction = raw_input("You can now: plot, refine, save, load, or exit. \n>")
      while nextAction != 'exit':
      #change state to next action
         if nextAction == 'plot':
            return plot()
         elif nextAction == 'refine':
            return self
         elif nextAction == 'save':
            return save()
         elif nextAction == 'load':
            return load()
         else:
            print "Input not understood."
            nextAction = raw_input("You can now: plot, refine, save, load, or exit. \n>")
      return 0 #exit the program

class refineS:
   def prompt(self):
      self.form = Form.Instance().get()
      return "Would you like h-auto, p-auto, h-manual or p-manual refinement? \n>"
   
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
         refineCell = raw_input("Which cells would you like to refine? (Ex. 1 2 4) \n>")
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
         refineCell = raw_input("Which cells would you like to refine? (Ex. 1 2 4) \n>")
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
         return refineS()

      print("Energy error after refinement: %0.3f" % (energyError))
      print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))

      nextAction = raw_input("You can now: plot, refine, save, load, or exit. \n>")
      while nextAction != 'exit':
      #change state to next action
         if nextAction == 'plot':
            return plot()
         elif nextAction == 'refine':
            return self
         elif nextAction == 'save':
            return save()
         elif nextAction == 'load':
            return load()
         else:
            print "Input not understood."
            nextAction = raw_input("You can now: plot, refine, save, load, or exit. \n>")
      return 0 #exit the program


class load:

   def prompt(self):
      return "Filename: \n> "

   def handle(self, selection):
      filename = selection + ".data"
      data = pickle.load(open(filename, 'rb'))

      s_type = data[0]
      polyOrder = data[1]
      Re = data[2]
      delta_k =1
      spaceDim = 2
      useConformingTraces = True
      mu = 1.0
      
      if s_type == 'Stokes':
         form = StokesVGPFormulation(spaceDim, useConformingTraces, mu)
         form.initializeSolution(selection, polyOrder, delta_k)
         

      elif s_type == 'Navier-Stokes':
         form = NavierStokesVGPFormulation(selection, spaceDim, Re, polyOrder, delta_k)
      
      print "Loaded."
      Form.Instance().setData(data)
      Form.Instance().setForm(form)
      
      nextAction = raw_input("You can now: plot, refine, save, load, or exit. \n>")
      #change state to next action
      if nextAction == 'plot':
         return plot()
      elif nextAction == 'refine':
          if s_type:
             return refineNS()
          else:
             return refineS()
      elif nextAction == 'save':
         return save()
      elif nextAction == 'load':
         return load()
      elif nextAction == 'exit':
         return 0
      else:
         print "Input not understood"
         return 0

class save:

   def prompt(self):
      return "Name a file to save to: \n> "

   def handle(self, selection):
      data = Form.Instance().getData()

      pickle.dump(data, open(selection +".data", 'wb'))

      print("Saving to "+ selection)
      Form.Instance().get().save(selection)
      print "...saved."
      self.state = initial()


def nonlinearSolve(maxSteps, form):
            normOfIncrement = 1
            stepNumber = 0
            nonlinearThreshold = 1e-3
            while normOfIncrement > nonlinearThreshold and stepNumber < maxSteps:
               form.solveAndAccumulate()
               normOfIncrement = form.L2NormSolutionIncrement()
               print("L^2 norm of increment: %0.3f" % normOfIncrement)
               stepNumber += 1


def start():
   state = main()

if __name__ == "__main__":
   start()
