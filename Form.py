from Singleton import *


@Singleton
class Form(object):
   #self.form = None
   def __init__(self):
       pass

   def setForm(self, form):
     self.form = form


   def get(self):
      return self.form
