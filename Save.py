from Form import *
import cPickle as pickle

class Save:

   def prompt(self):
      return "Name a file to save to: \n> "

   def handle(self, selection):
      form = Form.Instance()
      data = form.getData()

      pickle.dump(data, open(selection +".data", 'wb'))

      print("Saving to "+ selection)
      form.get().save(selection)
      #exporter = HDF5Exporter(form.solution().mesh(), selection, ".")
      #exporter.exportSolution(form.solution(),0)
      print "...saved."

      from Transition import Transition
      return Transition()
