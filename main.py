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
      elif(selection == "navier-stokes"): # I saw something in the slides from last class that NS would be steady state only...
         return solver(True)
      else:
         print ("Input not understood")
         return self
   
class plot: #So to get the info to plot, refine we pass in the form object from above??
   
   def prompt(self):
         return "Plotting mesh..." #I don't think there's other stuff we need to know
   
   def handle(self): #No selection to pass in?
      #use .getCellValues(mesh, cellID, refPoints) 
      #refPoints in the form [[-1,0],[1,0]...] 
      #returns a tuple (value -list of floats, physical points)
      pass
   
class refine:
      pass

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


      

