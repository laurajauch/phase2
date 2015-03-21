from solver import *

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
      pass
   
   def handle(self, selection):
      energyError = form.solution.energyErrorTotal()
      elementCount = mesh.numActiveElements()
      globalDofCount = mesh.globalDofs()

      refinementNumber = 0
      threshold = ?
      while energyError > threshold and refinement <= 8:
         form.hRefine()
         form.solve()
         energyError = form.solution().energyErrorTotal()
         refinementNumber += 1
         elementcount = mesh.numActiveElements()
         globalDofCount = mesh.numGlobalDofs()
         print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
         print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))

      

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


      

