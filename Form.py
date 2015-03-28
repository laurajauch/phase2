from Singleton import *


@Singleton
class Form(object):
 
   def __init__(self):
      pass
       
   def setForm(self, form):
     self.form = form


   def get(self):
      return self.form

   def getData(self):
      return [self.type, self.polyOrder, self.re]
   
   def setData(self, data):
      if isinstance(data[0], bool):
         if data[0] == False:
            self.type = 'Stokes'
         elif data[0] == True:
            self.type = 'Navier-Stokes'
      else:
         self.type = data[0]
      self.polyOrder = data[1]
      self.re = data[2]
