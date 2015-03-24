from Singleton import *


@Singleton
class Form(object):
   #self.form = None
   def __init__(self):
       self.type = ''
       self.polyOrder = ''
       self.re = ''
       

   def setForm(self, form):
     self.form = form


   def get(self):
      return self.form
