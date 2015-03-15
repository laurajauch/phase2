from PyCamellia import *
from main import *


class solver:

   def prompt(self):
      return "Would you like to solve Stokes or Navier-Stokes? \n> "

   def handle(self, selection):
      #determines what type of problem
      if(selection == "Stokes"):
         self.s_type = False
      elif(selection == "Navier-Stokes"):
         self.s_type = True
      else:
         print ("Input not understood")
         return self

      print("This solver handles rectangular meshes with lower-left corner at the origin.")

      re = 1 #if the problem is a stokes problem, this is always 1

      step = True #handles syntax errors

      if(self.s_type):
         re = self.re_num("What Reynolds number? \n> ")
         if re == "exit":
            return 0
               

      spaceDim = 2
      x0 = [0.,0.]

      temp = self.dims_num("What are the dimensions of your mesh?  (E.g., 1.0 x 2.0) \n> ")      
      dims = [float(temp[0]), float(temp[1])]

      response = self.dims_num("How many elements are in the mesh?  (E.g., 3 x 5) \n> ")
      numElements = [int(y[0]), int(y[1])]

      polyOrder = self.re_num("What polynomial order? (1 to 9) \n> ")      


   def re_num(self, prompt):
      step = True
      while(step):
         re = raw_input(prompt)
         if re == "exit":
             return "exit"
         try:
            toReturn = int(re)
            step = False
         except (ValueError):
            print ("Input not understood")
      return toReturn

   def dims_num(self, prompt):
      step = True
      while(step):
         response = raw_input(prompt)
         if response == "exit":
             return "exit"
         try:
            temp = response.split('x') #splits the string in two and deletes the x
            step = False
         except (ValueError):
            print ("Input not understood")
      return temp

         
      
      




