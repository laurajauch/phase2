from PyCamellia import *
from main import *



class solver:

   def __init__(self, s_type):
      self.s_type = s_type

   def prompt(self):
      return "Transient or steady state? \n> "

   def handle(self, selection):
      #determines what type of problem
      if(selection == "steady state"):
         self.f_type = False
      elif(selection == "transient"):
         self.f_type = True
      else:
         print ("Input not understood")
         return self

      print("This solver handles rectangular meshes with lower-left corner at the origin.")

      re = 1 #if the problem is a stokes problem, this is always 1


      if(self.s_type): #if Navier-Stokes then ask user for the Reynolds number
         re = self.re_num("What Reynolds number? \n> ")
         if re == "exit":
            return 0 #this causes the macro parser to skip all steps and quit

      
               

      spaceDim = 2
      x0 = [0.,0.]

      temp = self.dims_num("What are the dimensions of your mesh?  (E.g., 1.0 x 2.0) \n> ")
      if temp == "exit": 
         return 0
      dims = [float(temp[0]), float(temp[1])]

      response = self.dims_num("How many elements are in the mesh?  (E.g., 3 x 5) \n> ")
      if response == "exit": 
         return 0
      numElements = [int(y[0]), int(y[1])]

      meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
     
      polyOrder = self.re_num("What polynomial order? (1 to 9) \n> ")
      if polyOrder == "exit": 
         return 0
      
      delta_k = 1
      
      form = NavierStokesVGPFormulation(meshTopo,Re,polyOrder,delta_k)

      form.addZeroMeanPressureCondition()
            


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
            test = [float(temp[0]), float(temp[1])] #tests to make sure it is two numbers
            step = False
         except (ValueError):
            print ("Input not understood")
	    return "exit"
      return temp


         
      
      




