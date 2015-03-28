from solver import *
from PyCamellia import *
from plot import *
from Form import *
import cPickle as pickle

class Main: 

   def __init__(self):
      self.state = Initial()
      selection = ""
      while selection != "exit":
         if isinstance(self.state, int): #if state is a number, quit
            break
         selection = raw_input(self.state.prompt())
         if(selection != "exit"):
            self.state = self.state.handle(selection.lower())
            
      print ("Exiting")

class Initial:

   def prompt(self):
      return "You can now: create or load \n> "

   def handle(self, selection):
      if(selection == "create"):
         return Solver_Type()
      elif(selection == "load"):
         return Load() 
      else:
         print ("Input not understood")
         return self

class Solver_Type:

   def prompt(self):
      return "Would you like to solve Stokes or Navier-Stokes? \n> "

   def handle(self, selection):
      #determines what type of problem
      if(selection == "stokes"):
         return Solver(False)
      elif(selection == "navier-stokes"):
         return Solver(True)
      else:
         print ("Input not understood")
         return self

def start():
   print "Welcome to the PyCamellia incompressible flow solver!"
   Main()

if __name__ == "__main__":
   start()
