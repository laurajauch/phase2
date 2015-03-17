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
         return self #this should be whatever state handles loading
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
   





      

