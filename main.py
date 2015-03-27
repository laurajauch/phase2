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
   
class refine:
   def prompt(self):
      self.form = Form.Instance().get()
      return "Would you like p or h-auto refinement? \n>"
   
   def handle(self, selection): 
      # we need the form. Also I don't actually know what this code does.
      energyError = self.form.solution().energyErrorTotal() #SEG FAULT - b/c no boundary conditions??
      mesh = self.form.solution().mesh()
      elementCount = mesh.numActiveElements()
      globalDofCount = mesh.globalDofs()
      refinementNumber = 0

      if selection == 'h-auto':
         while energyError > threshold and refinement <= 8: #This guard needs to be updated
         #Dr. Roberts said the interior of this loop should do what we want for h-auto
            form.hRefine() #for each cellID #- does hRefine take an argument?
            form.solve() 
            energyError = form.solution().energyErrorTotal()
            refinementNumber += 1
            elementcount = mesh.numActiveElements()
            globalDofCount = mesh.numGlobalDofs()
            print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
            print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))       
                 
      elif selection == 'p':
         cellIDs = mesh.getActiveCellIDs()
         print "Your active cells are: "
         print cellIDs
         refineCell = raw_input("Which cells would you like to refine? (Ex. 1 2 4) \n>")
         if refineCell == 'exit':
            return 0
         refineCell = refineCell.split() #convert input to list
         #feed list through hRefine() and/or pRefine()...
       


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
         return refine()
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



def start():
   state = main()

if __name__ == "__main__":
   start()
