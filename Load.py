from PyCamellia import *
from Transition import *
from Form import *
import cPickle as pickle

class Load:

   def prompt(self):
      return "Filename: \n> "

   def handle(self, selection):
      filename = selection + ".data"
      data = pickle.load(open(filename, 'rb'))

      s_type = data[0]
      polyOrder = data[1]
      Re = data[2]
      delta_k =1
      spaceDim = 2
      useConformingTraces = True
      mu = 1.0
      
      if s_type == 'Stokes':
         form = StokesVGPFormulation(spaceDim, useConformingTraces, mu)
         form.initializeSolution(selection, polyOrder, delta_k)
         

      elif s_type == 'Navier-Stokes':
         form = NavierStokesVGPFormulation(selection, spaceDim, Re, polyOrder, delta_k)
      
      print "Loaded."
      Form.Instance().setData(data)
      Form.Instance().setForm(form)
      
      return Transition()
