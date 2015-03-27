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

      numElements = [int(response[0]), int(response[1])]
     
      meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)

      polyOrder = self.re_num("What polynomial order? (1 to 9) \n> ")
      if polyOrder == "exit": 
         return 0
      
      delta_k = 1
      
      if self.s_type:  #NavierStokes form
         form = NavierStokesVGPFormulation(meshTopo,re,polyOrder,delta_k)
      else:            #Stokes form
         form = StokesVGPFormulation(spaceDim,True,1.0)
         form.initializeSolution(meshTopo,polyOrder,delta_k)

      form.addZeroMeanPressureCondition() 


      
      #inflow conditions
      inflowNum = self.re_num("How many inflow conditions? (Ex. 2) \n> ")
      i = 0
      if inflowNum == "exit":
         return 0
      try:
         while i < int(inflowNum):
            inflow = raw_input("For inflow condition "+ str(i + 1) +", What is inflow region " + str(i+1) +"? (Ex. x = 0, y < 4) \n> ")
            inf = [z.strip() for z in inflow.split(',')]
            spFils = self.getSF(inf[0])
            del inf[0] 
            for x in inf:
               spFils = spFils and self.getSF(x) 

                  
            inflowxVel = raw_input("For inflow condition "+ str(i + 1) +", What is the x component of the velocity? \n> ")
            xVel = self.functionParser(inflowxVel)

            inflowyVel = raw_input("For inflow condition  "+ str(i + 1) +", What is the y component of the velocity? \n> ")
            yVel = self.functionParser(inflowyVel)
   
            velocity = Function.vectorize(xVel, yVel)
            form.addInflowCondition(spFils, velocity)
            form.addWallCondition(SpatialFilter.negatedFilter(spFils))
            i += 1
      except(ValueError):
         print("Input not understood")
         return self
         

      #outflow conditions
      outflowNum = self.re_num("How many outflow conditions? (Ex. 2) \n> ")
      i = 0
      if outflowNum == "exit":
         return 0
      try:
         while i < int(outflowNum):
            outflow = raw_input("What is outflow region " + str(i+1) +"? (Ex. x = 0, y > 2) \n> ") 
            inf = [z.strip() for z in outflow.split(',')]
            
            spFilsO = self.getSF(inf[0])
            del inf[0]
            for x in inf:
               spFilsO = spFilsO and self.getSF(x) 
            
            form.addOutflowCondition(spFilsO)
            form.addWallCondition(SpatialFilter.negatedFilter(spFilsO))
            i += 1
      except:
         print("Input not understood")
         return self

      print "Solving..."
      
      if self.s_type: #solve Navier-Stokes
         def nonlinearSolve(maxSteps):
            normOfIncrement = 1
            stepNumber = 0
            nonlinearThreshold = 1e-3
            while normOfIncrement > nonlinearThreshold and stepNumber < maxSteps:
               form.solveAndAccumulate()
               normOfIncrement = form.L2NormSolutionIncrement()
               print("L^2 norm of increment %i: %0.3f" % (stepNumber, normOfIncrement))
               stepNumber += 1

         maxSteps = 10
         nonlinearSolve(maxSteps)
         energyError = form.solutionIncrement().energyErrorTotal()

      else:   #solve Stokes
         form.solve() 
         energyError = form.solution().energyErrorTotal()
      


      mesh = form.solution().mesh()
      elementCount = mesh.numActiveElements()
      globalDofCount = mesh.numGlobalDofs()
      print("Initial mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
      print("Energy error is %0.3f" %energyError)
   
      Form.Instance().setData([self.s_type, polyOrder, re])
      Form.Instance().setForm(form)

      return transition()


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
	    return "exit"  
      return temp


   def getSF(self, arg):
      arg = arg.replace(" ", "")
      arg = list(arg)
   
      op = arg[1]
      xory = arg[0]
      
      if xory == 'x':
         if op == '=':
            return SpatialFilter.matchingX(float(arg[2]))
         if op == '>':
            return SpatialFilter.greaterThanX(float(arg[2]))
         if op == '<':
            return SpatialFilter.lessThanX(float(arg[2]))

      elif xory == 'y':
         if op == '=':
            return SpatialFilter.matchingY(float(arg[2]))
         if op == '>':
            return SpatialFilter.greaterThanY(float(arg[2]))
         if op == '<':
            return SpatialFilter.lessThanY(float(arg[2]))
   

   def functionParser(self, fun):
      operators = []
      comp = []
      i = 0
      while (i < (len(fun))):
         if i == 0 and fun[i] == "-":
            temp = "-"
            i+=1
            while self.isNum(fun[i]):
               temp+=fun[i]
               i+=1
            i = i - 1
            comp.append(float(temp))
         else: 
            subFun = "" 
            if fun[i] == "(":
               i+=1

               j = i
               lastParen = ["("]

               while (len(lastParen) > 0):
                  if fun[j] == ")":
                     lastParen.pop()
                  elif fun[j] == "(":
                     lastParen.append("(")
                  j = j+1

               while i < j:
                  subFun += fun[i]
                  i+=1
               i = i-1
               comp.append(self.functionParser(subFun))
            elif fun[i] == "-" and i>0 and (fun[i-1] == "*" or fun[i-1] == "/" or fun[i-1] == "+"): 
               temp = "-"
               i+=1
               while self.isNum(fun[i]):
                  temp+=fun[i]
                  i+=1
               i = i - 1
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
               i = i-1
               comp.append(float(temp))
         i = i + 1

      if len(comp) == 1:
         if self.isNum(comp[0]):
            return Function.constant(int(comp[0]))
         else:
            return comp[0]

      opComp = {0:["*","/"], 1:["+","-"]} 
      j = 0
      
      """
      for i in range(len(operators)):
         print operators[i]
      """

      i = 0
      while(i < (len(comp)-1)):
         if operators[i] == opComp[j][0]:
            comp [i] = comp[i] * comp[i+1]
            comp.pop(i+1)
            operators.pop(i)
            i -= 1
         elif operators[i] == opComp[j][1]:
            comp[i] = comp[i] / comp[i+1]
            comp.pop(i+1)
            operators.pop(i)
            i-=1
         i = i + 1
            
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
         
      


                           



