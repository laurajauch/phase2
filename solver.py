from PyCamellia import *
from main import *
from plot import *
from Form import *

class solver:

   def __init__(self, s_type):
      self.s_type = s_type

   def prompt(self):
      return "Transient or Steady State? \n> "

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
      #numElements = [int(y[0]), int(y[1])]
      numElements = [int(response[0]), int(response[1])]
     
      meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)

      polyOrder = self.re_num("What polynomial order? (1 to 9) \n> ")
      if polyOrder == "exit": 
         return 0
      
      delta_k = 1
      
      form = NavierStokesVGPFormulation(meshTopo,re,polyOrder,delta_k)
 
      form.addZeroMeanPressureCondition() 

      Form.Instance().setForm(form)
      
      #boundary/inflow conditions
      inflowNum = raw_input("How many inflow conditions? (Ex. 2) \n>")
      i = 0
      if inflowNum == "exit":
         return 0
      try:
         while i < int(inflowNum):
            inflow = raw_input("What is inflow region " + str(i+1) +"? (Ex. -3*(3+5)-2) \n>")
            #parse inflow. NASTY.
            #save this somewhere so we can build walls
            i += 1
      except(ValueError):
         print("Input not understood")
         return self
         

      #outflow conditions
      outflowNum = raw_input("How many outflow conditions? (Ex. 2) \n>")
      i = 0
      if outflowNum == "exit":
         return 0
      try:
         while i < int(outflowNum):
            outflow = raw_input("What is outflow region " + str(i+1) +"? (Ex. -3*(3+5)-2) \n>")
            #parse inflow. NASTY.
            #save this somewhere so we can build walls
            i += 1
      except(ValueError):
         print("Input not understood")
         return self


      #Set walls. Whatever isn't inflow or outflow
      


      print "Solving..."
      #does this belong stuff here?
      #energyError = form.solution().energyErrorTotal()  -----> SEG FAULT
      #mesh = form.solution().mesh()
      #elementCount = mesh.numActiveElements()
      #globalDofCount = mesh.numGlobalDofs()
      #print("Initial mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
      #print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
      

      nextAction = raw_input("You can now: plot, refine, save, load, or exit. \n>")
      #change state to next action
      if nextAction == 'plot':
         return plot()
      if nextAction == 'refine':
         return refine()
      if nextAction == 'save':
         return save()
      if nextAction == 'load':
         return load()
      if nextAction == 'exit':
         return 0


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
         except (ValueError, IndexError):
            print ("Input not understood")
	    return "exit"  #Do we really want to exit here? 
      return temp



   def functionParser(self, fun):
      print fun
      operators = []
      comp = []
      for i in range(len(fun)):
         if i == 0 and fun[i] == "-":
            temp = "-"
            i+=1
            while self.isNum(fun[i]):
               temp+=fun[i]
               i+=1
            comp.append(float(temp))
         else: 
            subFun = "" 
            if fun[i] == "(":
               i+=1
               while fun[i] != ")":
                  subFun += fun[i]
                  i+=1
               print subFun
               comp.append(self.functionParser(subFun))
            elif fun[i] == "-" and i>0 and (fun[i-1] == "*" or fun[i-1] == "/" or fun[i-1] == "+"): 
               temp = "-"
               i+=1
               while self.isNum(fun[i]):
                  temp+=fun[i]
                  i+=1
               comp.append(int(temp))
            elif fun[i] == "*" or fun[i] == "/" or fun[i] == "+" or fun[i] == "-":
               operators.append(fun[i])
            elif fun[i].isalpha():
               if fun[i+1] == "^":
                  i += 2
                  temp = ""
                  while self.isNum(fun[i]):
                     temp+=fun[i]
                     i+=1
                  comp.append(Function.xn(int(temp)))
               else:
                  comp.append(Function.xn(1))
            elif self.isNum(fun[i]):
               temp = ""
               while i<len(fun) and (self.isNum(fun[i]) or fun[i] == "."):
                  temp+=fun[i]
                  i+=1
               comp.append(float(temp))

      if len(comp) == 1:
         if self.isNum(comp[0]):
            return Function.constant(int(comp[0]))
         else:
            return comp[0]

      print comp[0]

      opComp = {0:["*","/"], 1:["+","-"]} 
      j = 0
      for i in range(len(comp)-1):
         if operators[i] == opComp[j][0]:
            comp [i] = comp[i] * comp[i+1]
            comp.pop(i+1)
            operators.pop(i)
         elif operators[i] == opComp[j][1]:
            toReturn += comp[i] / comp[i+1]
            comp.pop(i+1)
            operators.pop(i)
            
      j+=1
      toReturn = comp[0]
      for i in range(len(comp)-1):
         if operators[i] == opComp[j][0]:
            toReturn += comp[i+1]
         elif operators[i] == opComp[j][1]:
            toReturn -= comp[i+1]
         
      if self.isNum(toReturn):
         return Function.constant(toReturn)
      else:
         return toReturn
         


   def isNum(self, num):
      try:
         int(num)
         return True
      except:
         return False
         
      


                           

