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


      
      #boundary/inflow conditions
      inflowNum = raw_input("How many inflow conditions? (Ex. 2) \n>")
      i = 0
      if inflowNum == "exit":
         return 0
      try:
         while i < int(inflowNum):
            inflow = raw_input("What is inflow region " + str(i+1) +"? (Ex. x = 0, y < 4) \n>")
            inf = [z.strip() for z in inflow.split(',')]
            
            #if len(inflow[0]) == 3:
            spFils = self.getSF(inf[0])
            del inf[0]
         #   else:
          #     raise ValueError 
         
            for x in inf:
           #    if len(x) == 3:
               spFils = spFils and self.getSF(x) 
               #else:
                #  raise ValueError
            
            
                  
            inflowxVel = raw_input("What is the x component of the velocity? \n>")
            #parse
            xVel = Function.constant(0)

            inflowyVel = raw_input("What is the y component of the velocity? \n>")
            #parse
            yVel = Function.constant(0)
   
            velocity = Function.vectorize(xVel,yVel)
            form.addInflowCondition(spFils, velocity)
            form.addWallCondition(SpatialFilter.negatedFilter(spFils))
            i += 1
      except: #(ValueError):
         print("Input not understood")
         return self
         

      #outflow conditions
      outflowNum = raw_input("How many outflow conditions? (Ex. 2) \n>")
      i = 0
      if outflowNum == "exit":
         return 0
      try:
         while i < int(outflowNum):
            outflow = raw_input("What is outflow region " + str(i+1) +"? (Ex. x = 0, y > 2 \n>") 
            inf = [z.strip() for z in inflow.split(',')]
            
            #if len(inf[0]) == 3:
            spFilsO = self.getSF(inf[0])
            del inf[0]
            #else:
             #  raise ValueError 
              # return 0
            for x in inf:
             #  if len(x) == 3:
               spFilsO = spFilsO and self.getSF(x) 
               #else:
                #  raise ValueError
            
            form.addOutflowCondition(spFilsO)
            form.addWallCondition(SpatialFilter.negatedFilter(spFilsO))
            i += 1
      except(ValueError):
         print("Input not understood")
         return self

      print "Solving..."
      
      form.solve()  #attribute error??

      #energyError = form.solution().energyErrorTotal()  #-----> SEG FAULT
      #mesh = form.solution().mesh()
      #elementCount = mesh.numActiveElements()
      #globalDofCount = mesh.numGlobalDofs()
      #print("Initial mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
      #print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
      
      #Form.Instance.setForm(form)
      nextAction = ''
      while nextAction != 'exit':
         nextAction = raw_input("You can now: plot, refine, save, load, or exit. \n>")
      #change state to next action
         if nextAction == 'plot':
            return plot()
         elif nextAction == 'refine':
            return refine()
         elif nextAction == 'save':
            return save()
         elif nextAction == 'load':
            return load()
         else:
            print "Input not understood."

      return 0 #exit the program


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


   def getSF(self, arg):
      #arg = [x.strip() for x in args.split()]
      index = 0
      arg = list(arg)
      for x in arg:
         if x == ' ':
            del arg[index]
         else:
            index += 1
      
   
      op = arg[1]
      xory = arg[0]
      try:
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
      except: #(ValueError, TypeError):
         #print "Input not understood"
         pass
