from PyCamellia import *
import unittest
from RefineS import *
from RefineNS import *


class testRefine(unittest.TestCase):

    def testStokesHAuto(self):
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
        inflowTot = inflow1 & inflow2
        velocity = Function.vectorize(Function.constant(9), Function.xn(8))
        compForm.addInflowCondition(inflowTot, velocity)
        
        outflow1 = SpatialFilter.lessThanY(1.0)
        compForm.addOutflowCondition(outflow1)
        compForm.addWallCondition(SpatialFilter.negatedFilter(inflowTot) | SpatialFilter.negatedFilter(outflow1))
        mesh = compForm.solution().mesh()
        numElems = mesh.numActiveElements()
        gdcount = mesh.numGlobalDofs()
        
        Form.Instance().setForm(compForm)
        Form.Instance().setData(['Stokes', polyOrder, 1])

        #refine Stokes automatically in h
        RefineS().handle('h-auto')
        testMesh = Form.Instance().get().solution().mesh()
        tenergyError = Form.Instance().get().solution().energyErrorTotal()
        telementcount = testMesh.numActiveElements()
        tgdCount = testMesh.numGlobalDofs()
        #refine example in h-auto


        meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)
        compForm = StokesVGPFormulation(2, True, 1.0)
        compForm.initializeSolution(meshTopo, polyOrder, delta_k)
        compForm.addZeroMeanPressureCondition()
        
        inflow1 = SpatialFilter.matchingX(2.0)
        inflow2 = SpatialFilter.greaterThanY(4.0)
        inflowTot = inflow1 & inflow2
        velocity = Function.vectorize(Function.constant(9), Function.xn(8))
        compForm.addInflowCondition(inflowTot, velocity)
        
        outflow1 = SpatialFilter.lessThanY(1.0)
        compForm.addOutflowCondition(outflow1)
        compForm.addWallCondition(SpatialFilter.negatedFilter(inflowTot) | SpatialFilter.negatedFilter(outflow1))
        mesh = compForm.solution().mesh()
        numElems = mesh.numActiveElements()
        gdcount = mesh.numGlobalDofs()
        compForm.hRefine() 
        compForm.solve() 
        energyError = compForm.solution().energyErrorTotal()
        elementcount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()

        self.assertEqual(tenergyError, energyError)
        self.assertEqual(telementcount, elementcount)
        self.assertEqual(tgdCount, globalDofCount)


    def testStokesPAuto(self): 
        dims = [3.0, 6.0]
        numElements = [3, 6]
        x0 = [0., 0.]
        delta_k = 1
        polyOrder = 3
        #rebuild the Stokes form, unrefined
        meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements,x0)
        compForm = StokesVGPFormulation(2, True, 1.0)
        compForm.initializeSolution(meshTopo, polyOrder, delta_k)
        compForm.addZeroMeanPressureCondition()
        
        inflow1 = SpatialFilter.matchingX(2.0)
        inflow2 = SpatialFilter.greaterThanY(4.0)
        inflowTot = inflow1 & inflow2
        velocity = Function.vectorize(Function.constant(9), Function.xn(8))
        compForm.addInflowCondition(inflowTot, velocity)
        
        outflow1 = SpatialFilter.lessThanY(1.0)
        compForm.addOutflowCondition(outflow1)
        compForm.addWallCondition(SpatialFilter.negatedFilter(inflowTot) | SpatialFilter.negatedFilter(outflow1))
        mesh = compForm.solution().mesh()
        numElems = mesh.numActiveElements()
        gdcount = mesh.numGlobalDofs()
        
        Form.Instance().setForm(compForm)
        Form.Instance().setData(['Stokes', polyOrder, 1])

        #refine Stokes automatically in p
        RefineS().handle('p-auto')
        testMesh = Form.Instance().get().solution().mesh()
        tenergyError = Form.Instance().get().solution().energyErrorTotal()
        telementcount = testMesh.numActiveElements()
        tgdCount = testMesh.numGlobalDofs()
        print "Through Stokes p-auto"

        meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements,x0)
        compForm = StokesVGPFormulation(2, True, 1.0)
        compForm.initializeSolution(meshTopo, polyOrder, delta_k)
        compForm.addZeroMeanPressureCondition()
        
        inflow1 = SpatialFilter.matchingX(2.0)
        inflow2 = SpatialFilter.greaterThanY(4.0)
        inflowTot = inflow1 & inflow2
        velocity = Function.vectorize(Function.constant(9), Function.xn(8))
        compForm.addInflowCondition(inflowTot, velocity)
        
        outflow1 = SpatialFilter.lessThanY(1.0)
        compForm.addOutflowCondition(outflow1)
        compForm.addWallCondition(SpatialFilter.negatedFilter(inflowTot) | SpatialFilter.negatedFilter(outflow1))
        mesh = compForm.solution().mesh()
        numElems = mesh.numActiveElements()
        gdcount = mesh.numGlobalDofs()
        #refine example in p-auto
        compForm.pRefine()
        compForm.solve() 
        energyError = compForm.solution().energyErrorTotal()
        elementcount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()

        self.assertEqual(tenergyError, energyError)
        self.assertEqual(telementcount, elementcount)
        self.assertEqual(tgdCount, globalDofCount)


    """def testNSHAuto(self):
        #A function to solve Navier-Stokes
        def nonlinearSolve(maxSteps, form):
            normOfIncrement = 1
            stepNumber = 0
            nonlinearThreshold = 1e-3
            while normOfIncrement > nonlinearThreshold and stepNumber < maxSteps:
                form.solveAndAccumulate()
                normOfIncrement = form.L2NormSolutionIncrement()
                stepNumber += 1


        dims = [3.0, 6.0]
        numElements = [3, 6]
        x0 = [0., 0.]
        delta_k = 1
        polyOrder = 3
        re = 800
        maxSteps = 3
        #build the Navier-Stokes form, unrefined
        meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements,x0)
        compForm = NavierStokesVGPFormulation(meshTopo,re,polyOrder,delta_k)
        compForm.addZeroMeanPressureCondition()
        inflow1 = SpatialFilter.matchingX(2.0)
        inflow2 = SpatialFilter.greaterThanY(4.0)
        inflowTot = inflow1 and inflow2
        velocity = Function.vectorize(Function.constant(9), Function.xn(8))
        compForm.addInflowCondition(inflowTot, velocity)
        
        outflow1 = SpatialFilter.lessThanY(1.0)
        compForm.addOutflowCondition(outflow1)
        compForm.addWallCondition(SpatialFilter.negatedFilter(inflowTot) | SpatialFilter.negatedFilter(outflow1))

        nonlinearSolve(maxSteps, compForm)
        Form.Instance().setForm(compForm)
        Form.Instance().setData(['Navier-Stokes', polyOrder, 1])

        #refine in our code
        RefineNS().handle('h-auto')
        testMesh = Form.Instance().get().solution().mesh()
        tenergyError = Form.Instance().get().solutionIncrement().energyErrorTotal()
        telementcount = testMesh.numActiveElements()
        tgdCount = testMesh.numGlobalDofs()

        #rebuild form and feed through regular code
        meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements,x0)
        compForm = NavierStokesVGPFormulation(meshTopo,re,polyOrder,delta_k)
        compForm.addZeroMeanPressureCondition() 
        inflow1 = SpatialFilter.matchingX(2.0)
        inflow2 = SpatialFilter.greaterThanY(4.0)
        inflowTot = inflow1 and inflow2
        velocity = Function.vectorize(Function.constant(9), Function.xn(8))
        compForm.addInflowCondition(inflowTot, velocity)
        
        outflow1 = SpatialFilter.lessThanY(1.0)
        compForm.addOutflowCondition(outflow1)
        compForm.addWallCondition(SpatialFilter.negatedFilter(inflowTot) | SpatialFilter.negatedFilter(outflow1))

        compForm.hRefine()
        nonlinearSolve(maxSteps, compForm)
        energyError = compForm.solutionIncrement().energyErrorTotal()

        mesh = compForm.solution().mesh()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()

        #self.assertEqual(tenergyError, energyError)
        self.assertEqual(telementcount, elementCount)
        self.assertEqual(tgdCount, globalDofCount)"""
