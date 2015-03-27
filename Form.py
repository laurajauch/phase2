from Singleton import *


@Singleton
class Form(object):
 
   def __init__(self):#, s_type, polyOrder, re):
      pass
       

   def setForm(self, form):
     self.form = form


   def get(self):
      return self.form

   def getData(self):
      return [self.type, self.polyOrder, self.re]
   
   def setData(self, data):
      if data[0] == False:
         self.type = 'Stokes'
      else:
         self.type = 'Navier-Stokes'
      self.polyOrder = data[1]
      self.re = data[2]
