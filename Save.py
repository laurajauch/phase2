from Form import *
import cPickle as pickle

class Save:

   def prompt(self):
      return "Name a file to save to: \n> "

   def handle(self, selection):
      data = Form.Instance().getData()

      pickle.dump(data, open(selection +".data", 'wb'))

      print("Saving to "+ selection)
      Form.Instance().get().save(selection)
      print "...saved."

      from Transition import Transition
      return Transition()
