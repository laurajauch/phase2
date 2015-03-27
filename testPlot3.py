import matplotlib.pyplot as plt
from numpy import *

def test1():
    selection = ""
    while selection != "exit":
        print("Mesh dimensions, doubles please: ")
        selection = raw_input()
        if(selection == "exit"):
            break
        #mesh dim / num elements = increments between cells
        mDims = [ceil(float(s.strip())) for s in selection.split("x")]
        print mDims
        
        print("Mesh elements, ints please: ")
        selection = raw_input()
        if(selection == "exit"):
            break
        mElems = [int(s.strip()) for s in selection.split("x")]
        print mElems

        mScale = divide(mDims, mElems) #the mDims should just help define the scale of each cell
        print mScale
        
        mElemsArray = random.randn(mElems[0], mElems[1]) #the elements should define how many cells
        c = plt.pcolormesh(mElemsArray, edgecolors='k', linewidths=2, 
                           cmap='bwr', vmin='-100', vmax='100')
        plt.title('Test1: Basic Graph Printing and Mesh Lines')

        #configure  X axes
        plt.xlim(0.5,4.5)
        plt.xticks([1,2,3,4])

        #configure  Y axes
        plt.ylim(19.8,21.2)
        plt.yticks([20, 21, 20.5, 20.8])


        plt.show()
        
            
    print ("Exiting")


def test2():
    selection = ""
    while selection != "exit":
        print("Mesh dimensions, doubles please: ")
        selection = raw_input()
        if(selection == "exit"):
            break
        #mesh dim / num elements = increments between cells
        mDims = [ceil(float(s.strip())) for s in selection.split("x")]
        print mDims
        
        #--------GET NUMBER OF X ELEMENTS---------
        print("Mesh x elements, int please: ")
        selection = raw_input()
        if(selection == "exit"):
            break
        mXElems = int(selection.strip())
        print mXElems

        #--------GET NUMBER OF Y ELEMENTS---------
        print("Mesh y elements, int please: ")
        selection = raw_input()
        if(selection == "exit"):
            break
        mYElems = int(selection.strip())
        print mYElems
        
        #mDims[0]/mXElems is the range of values that any X value can be, as the mesh in only so large
        mXEA = random.random_integers(-(mDims[0]/mXElems), (mDims[0]/mXElems), (mXElems, mYElems)) #Fill an array of size mXElems with random values for all X Coordinates
        print("mXEA:\n" + str(mXEA))
        mYEA = random.random_integers(-(mDims[1]/mYElems), (mDims[1]/mYElems), (mXElems, mYElems)) #Fill an array of size mXElems with random values for all Y Coordinates
        print("mYEA:\n" + str(mYEA))
        colA = random.random_integers(-100, 100, (mXElems-1, mYElems-1)) #Fill an array with Z Values
        print("colA:\n" + str(colA))

        #plots all X values mapped to all Y values and then makes them into a grid?
        c = plt.pcolormesh(mXEA, mYEA, colA, edgecolors='k', linewidths=2, 
                           cmap='bwr', vmin='-100', vmax='100') 
        plt.title('Test2: Individual Array Inputs')

        #configure  X axes
        #plt.xlim(0, 10)
        #plt.xticks([2, 5.676, 7, 10])

        #configure  Y axes
        #plt.ylim(0, 10)
        #plt.yticks([1, 2, 3, 4, 7, 8, 10])


        plt.show()
               
    print ("Exiting")


def test3():
    selection = ""
    while selection != "exit":
        print("Mesh dimensions, doubles please:")
        selection = raw_input()
        if(selection == "exit"):
            break
        #mesh dim / num elements = increments between cells
        mDims = [float(s.strip()) for s in selection.split("x")]
        print mDims
        
        print("Number of elements, ints please:")
        #--------GET NUMBER OF X AND Y ELEMENTS---------
        selection = raw_input()
        if(selection == "exit"):
            break
        mXYE = [int(s.strip()) for s in selection.split("x")]
        print mXYE #meshXandYElements

        mXElems = mXYE[0]
        mYElems = mXYE[1]
        
        #mDims[0]/mXElems is the range of values that any X value can be, as the mesh in only so large
        #Fill an array of size mXElems with random values for all X Coordinates
        mXEA = [] #meshXElementsArray
        xRatio = mDims[0]/mXElems
        for i in range(0, int(mXElems)+1):
            mXEA.append(mDims[0]-(xRatio*i))
        print("mXEA:\n" + str(mXEA))

        #Fill an array of size mXElems with random values for all Y Coordinates
        mYEA = []
        yRatio = mDims[1]/mYElems
        print yRatio
        for i in range(0, int(mYElems)+1):
            mYEA.append(mDims[1]-(yRatio*i)) 
        print("mYEA:\n" + str(mYEA))

        colA = random.random_integers(-100, 100, (mXElems, mYElems)) #Fill an array with Z Values
        print("colA:\n" + str(colA) + "\n")

        print("array(mXEA): " + str(array(mXEA)))
        print("array(mYEA): " + str(array(mYEA)))

        #plots all X values mapped to all Y values and then makes them into a grid?
        c = plt.pcolormesh(array(mXEA), array(mYEA), colA, edgecolors='k', linewidths=2, 
                           cmap='bwr', vmin='-100', vmax='100') 
        plt.title('Test3: X and Y Values Preset Based on Input')

        #configure  X axes
        
        #plt.xlim(0, 10)
        #print mXEA
        #mXEA = round(mXEA)
        plt.xticks(mXEA)

        #configure  Y axes
        #plt.ylim(0, 10))
        plt.yticks(mYEA)


        plt.show()
        
            
    print ("Exiting")


def test4():
    selection = ""
    while selection != "exit":
        print("Mesh dimensions, doubles please:")
        selection = raw_input()
        if(selection == "exit"):
            break
        #mesh dim / num elements = increments between cells
        mDims = [float(s.strip()) for s in selection.split("x")]
        print mDims
        
        print("Number of elements, ints please:")
        #--------GET NUMBER OF X AND Y ELEMENTS---------
        selection = raw_input()
        if(selection == "exit"):
            break
        mXYE = [int(s.strip()) for s in selection.split("x")]
        print mXYE #meshXandYElements

        mXElems = mXYE[0]
        mYElems = mXYE[1]
        
        #mDims[0]/mXElems is the range of values that any X value can be, as the mesh in only so large
        #Fill an array of size mXElems with random values for all X Coordinates
        mXEA = [] #meshXElementsArray
        xRatio = mDims[0]/mXElems
        for i in range(0, int(mXElems)+1):
            mXEA.append(mDims[0]-(xRatio*i))
        print("mXEA:\n" + str(mXEA))

        #Fill an array of size mXElems with random values for all Y Coordinates
        mYEA = []
        yRatio = mDims[1]/mYElems
        print yRatio
        for i in range(0, int(mYElems)+1):
            mYEA.append(mDims[1]-(yRatio*i)) 
        print("mYEA:\n" + str(mYEA))

        colA = random.random_integers(-100, 100, (mXElems, mYElems)) #Fill an array with Z Values
        print("colA:\n" + str(colA) + "\n")

        print("array(mXEA): " + str(array(mXEA)))
        print("array(mYEA): " + str(array(mYEA)))

        #plots all X values mapped to all Y values and then makes them into a grid?
        c = plt.pcolormesh(array(mXEA), array(mYEA), colA, edgecolors='k', linewidths=2, 
                           cmap='bwr', vmin='-100', vmax='100') 
        plt.title('Test4: Rounding ticks on the axes')

        #configure  X axes
        
        #print mXEA
        mXEA = around(mXEA, decimals = 3)
        plt.xticks(mXEA)

        #configure  Y axes
        #plt.ylim(0, 10))
        plt.yticks(mYEA)
        plt.xlim(0, 5.4)


        plt.show()
        
            
    print ("Exiting")

#Run the test
test4()
