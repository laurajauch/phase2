from PyCamellia import *
import unittest
from RefineS import *
from RefineNS import *


class testRefine(unittest.TestCase):

    dims = [3.0, 6.0]
    numElements = [3, 6]
    x0 = [0., 0.]
    delta_k = 1
    polyOrder = 3

    #build Stokes form
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
    mesh = compForm.solution().mesh()
    numElems = mesh.numActiveElements()
    gdcount = mesh.numGlobalDofs()
 
    Form.Instance().setForm(compForm)
    Form.Instance().setData(['Stokes', polyOrder, 1])



    def testStokesHAuto(self):
        #refine Stokes automatically in h
        RefineS().handle('h-auto')
        testMesh = Form.Instance().get().solution().mesh()
        tenergyError = Form.Instance().get().solution().energyErrorTotal()
        telementcount = testMesh.numActiveElements()
        tgdCount = testMesh.numGlobalDofs()
        #refine example in h-auto
        self.compForm.hRefine() 
        self.compForm.solve() 
        energyError = self.compForm.solution().energyErrorTotal()
        elementcount = self.mesh.numActiveElements()
        globalDofCount = self.mesh.numGlobalDofs()

        #self.assertEqual(tenergyError, energyError)
        self.assertEqual(telementcount, elementcount)
        self.assertEqual(tgdcount, globalDofCount)


    def testStokesPAuto(self):
        #rebuild the form, unrefined
        meshTopo = MeshFactory.rectilinearMeshTopology(self.dims, self.numElements, self.x0)
        compForm = StokesVGPFormulation(2, True, 1.0)
        compForm.initializeSolution(meshTopo, self.polyOrder, self.delta_k)
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
        mesh = compForm.solution().mesh()
        numElems = mesh.numActiveElements()
        gdcount = mesh.numGlobalDofs()
        
        Form.Instance().setForm(compForm)
        Form.Instance().setData(['Stokes', self.polyOrder, 1])

        #refine Stokes automatically in p
        RefineS().handle('p-auto')
        testMesh = Form.Instance().get().solution().mesh()
        tenergyError = Form.Instance().get().solution().energyErrorTotal()
        telementcount = testMesh.numActiveElements()
        tgdCount = testMesh.numGlobalDofs()
        print "Through Stokes p-auto"

        #refine example in p-auto
        self.compForm.pRefine() #HERE'S WHERE WE FREAK OUT, I THINK
        print "test1"
        self.compForm.solve() 
        print "test2"
        energyError = self.compForm.solution().energyErrorTotal()
        elementcount = self.mesh.numActiveElements()
        globalDofCount = self.mesh.numGlobalDofs()

        #self.assertEqual(tenergyError, energyError)
        self.assertEqual(telementcount, elementcount)
        self.assertEqual(tgdcount, globalDofCount)
