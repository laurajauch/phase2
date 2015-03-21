from solver import *
from plot import *

class main:  #this class is partially contained in the main method below

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
         print ("load not yet implemented")
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
      elif(selection == "navier-stokes"): # I believe that NS is steady state only...
         return solver(True)
      else:
         print ("Input not understood")
         return self
   
class refine:
   def prompt(self):
      return "Would you like p or h-auto refinement? \n>"
   
   def handle(self, selection): 
      # we need the form. Also I don't actually know what this code does.
      energyError = form.solution().energyErrorTotal()
      mesh = form.solution().mesh()
      elementCount = mesh.numActiveElements()
      globalDofCount = mesh.globalDofs()
      refinementNumber = 0

      if selection == 'h-auto':
     #while energyError > threshold and refinement <= 8: This guard needs to be updated
         #Dr. Roberts said the interior of this loop should do what we want for h-auto
         #form.hRefine() for each cellID - does hRefine take an argument?
         #form.solve() 
         #energyError = form.solution().energyErrorTotal()
         #refinementNumber += 1
         #elementcount = mesh.numActiveElements()
         #globalDofCount = mesh.numGlobalDofs()
         #print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
         #print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount)       
         pass

      if selection == 'p':
         cellIDs = mesh.getActiveCellIDs()
         print "Your active cells are: "
         print cellIDs
         refineCell = raw_input("Which cells would you like to refine? (Ex. 1 2 4) \n>")
         if refineCell == 'exit':
            return 0
         refineCell = refineCell.split() #convert input to list
         #feed list through hRefine() and/or pRefine()...?
       


class load:

   def prompt(self):
      return "Filename: \n> "

   def handle(self, selection):
      filename = selection
      file = open(filename, 'rb')
      form = pickle.load(file)
      file.close()
      #set everything to what was read from file

class save:

   def prompt(self):
      return "Name a file to save to: \n> "

   def handle(self, selection):
      filename = selection
      file = open(filename, 'wb')
      pickle.dump(form, file)
      file.close()
      print "Saved Successfully!"

def start():
   #self.state = initial()
   state = main()
   selection = ""
   while selection != "exit":
      if isinstance(self.state, int): #if state is a number, quit
         break
         selection = raw_input(self.state.prompt())
         if(selection != "exit"):
            self.state = self.state.handle(selection.lower())
   print ("Exiting")
   
   #fails to exit if we remove the selfs which are producing warnings.
   

if __name__ == "__main__":
   start()
