from PyCamellia import *
from Save import *
from Load import *
from Form import *
import unittest


class testSaveLoad(unittest.TestCase):

    dims = [3.0, 6.0]
    numElements = [3, 6]
    x0 = [0., 0.]
    delta_k = 1
    polyOrder = 3

    #original to compare to saved/loaded
    meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)
    compForm = StokesVGPFormulation(2, True, 1.0)
    compForm.initializeSolution(meshTopo, polyOrder, delta_k)
    compForm.addZeroMeanPressureCondition()

    inflow1 = SpatialFilter.matchingX(2.0)
    inflow2 = SpatialFilter.greaterThanY(4.0)
    inflowTot = inflow1 and inflow2
    velocity = Function.vectorize(Function.constant(9), Function.xn(8))
    compForm.addInflowCondition(inflowTot, velocity)
    compForm.addWallCondition(SpatialFilter.negatedFilter(inflowTot))

    outflow1 = SpatialFilter.lessThanY(1.0)
    compForm.addOutflowCondition(outflow1)
    compForm.addWallCondition(SpatialFilter.negatedFilter(inflowTot) or SpatialFilter.negatedFilter(outflow1))
    numElems = compForm.solution().mesh().numActiveElements()
    gdcount = compForm.solution().mesh().numGlobalDofs()
    #create Saved file to compare to original
    Form.Instance().setForm(compForm)
    Form.Instance().setData(['Stokes', polyOrder, 1])
    Save().handle('testForm') #save this Form in order to compare it to the original


    #Test that the Form object saves accurately
    def testForm(self):
        self.assertEqual(self.polyOrder, Form.Instance().getData()[1])
        self.assertIsNotNone(Form.Instance().get())
        tfElems = Form.Instance().get().solution().mesh().numActiveElements()
        cfElems = self.compForm.solution().mesh().numActiveElements()
        self.assertEqual(tfElems, self.numElems)
        tfcount = Form.Instance().get().solution().mesh().numGlobalDofs()
        self.assertEqual(self.gdcount, tfcount)

    #Test that our Saved and Loaded forms equal the original
    def testSaveandLoad(self):
        Load().handle('testForm') #The form has been saved
        self.assertEqual(self.polyOrder, Form.Instance().getData()[1])
        self.assertIsNotNone(Form.Instance().get())
        #self.assertEqual(self.compForm, Form.Instance().get())
        tfElems = Form.Instance().get().solution().mesh().numActiveElements()
        self.assertEqual(tfElems, self.numElems)
        tfcount = Form.Instance().get().solution().mesh().numGlobalDofs()
        self.assertEqual(self.gdcount, tfcount)
