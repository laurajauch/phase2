from solver import *

class main:

   def __init__(self):
      self.state = initial()
      selection = ""
      while selection != "exit":
         if isinstance(self.state, int):
            break
         selection = raw_input(self.state.prompt())
         if(selection != "exit"):
            self.state = self.state.handle(selection)
      print ("Exiting")


class initial:

   def prompt(self):
      return "You can now: create or load \n> "

   def handle(self, selection):
      if(selection == "create"):
         return solver()
      elif(selection == "load"):
         print ("load not yet implemented")
         return self #this should be whatever state handles loading
      else:
         print ("Input not understood")
         return self

class exiter:

   def prompt(self):
      return ""

   def handle(self, selection):
      return 0
   





      

