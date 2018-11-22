'''
Created on 21 nov. 2018

@author: Elodie
'''


import matplotlib.pyplot as plt
import numpy as np; np.random.seed(0)
import sqlite3
from database.Animal import *
from tkinter.filedialog import askopenfilename
from matplotlib.patches import *
from matplotlib.collections import PatchCollection
from database.Util import *
from matplotlib import patches


def plot( ax , animal, title , color = None ):
    xList, yList = animal.getTrajectoryData( )

    if ( color == None ):
        color = animal.getColor()
    ax.plot( xList, yList, color=color, linestyle='-', linewidth=1, alpha=0.5, label= animal.name )
    ax.set_title( title + " " + animal.RFID )
    ax.legend().set_visible(False)
    ax.set_xlim(90, 420)
    ax.set_ylim(-370, -40)
    ax.axis('off')
    
def plotZone( ax, colorEdge, colorFill, xa=114, xb=398, ya=-353, yb=-63 ):
    ax.add_artist(patches.Rectangle((xa, ya), xb-xa, yb-ya, edgecolor=colorEdge, fill=True, facecolor=colorFill, alpha=0.2, linewidth=2))
    
    
def plotSap( ax , animal ):

    sapDico = animal.getSapDictionnary()
        
    xList = []
    yList = []
    
    for t in sapDico.keys() :
        detection = animal.detectionDictionnary.get( t )
        xList.append( detection.massX )
        yList.append( -detection.massY )    
    color = "red"
    ax.scatter( xList, yList,  color=color, alpha=1, label= "sap", s=20 )
    

if __name__ == '__main__':
    
    print("Code launched.")
    
    '''
    This script draws the trajectory of the mouse in the two phases of the single object exploration test. The positions at which
    the animal is in SAP is marked in red. The object zone is drawn in light blue.
    '''
    
    files = askopenfilename( title="Choose a set of file to process", multiple=1 )
    text_file = getFileNameInput()
        
    nbFiles = len(files)
    fig, axes = plt.subplots( nrows = nbFiles, ncols = 2, figsize = (13,8*nbFiles) )

    n = 0
        
    for file in files:
        connection = sqlite3.connect( file )
             
        pool = AnimalPool()
        pool.loadAnimals( connection )
        animal = pool.animalDictionnary[1]
            
        #draw the trajectory in the first phase, without the object
        pool.loadDetection( start=0 , end=28*oneMinute )
        plotZone(axes[n,0], colorEdge='yellow', colorFill='yellow') #whole cage
        #plotZone(axes[n,0], colorEdge='blue', colorFill='blue', xa=120, xb=250, ya=-210, yb=-340) #object zone
        plot ( axes[n,0], animal , title = "First phase" , color ="black")
        #add the frames where the animal is in SAP
        plotSap( axes[n,0], animal )
        dt1 = animal.getDistance( 0 , 28*oneMinute )
        d1 = animal.getDistanceSpecZone( 0 , 28*oneMinute , xa=120, xb=250, ya=210, yb=340 )
        t1 = animal.getCountFramesSpecZone( 0*oneMinute , 28*oneMinute , xa=120, xb=250, ya=210, yb=340)
        sap1=len(animal.getSap(tmin=0, tmax=28*oneMinute, xa=120, xb=250, ya=210, yb=340 ))
                   
            
        #draw the trajectory in the second phase, with the object
        pool.loadDetection( start=32*oneMinute , end=60*oneMinute )
        plotZone(axes[n,1], colorEdge='yellow', colorFill='yellow' ) #whole cage
        plotZone(axes[n,1], colorEdge='blue', colorFill='blue', xa=120, xb=250, ya=-210, yb=-340) #object zone
        plot ( axes[n,1], animal, title = "Second phase", color ="black" )
        #add the frames where the animal is in SAP
        plotSap( axes[n,1], animal )
        dt2 = animal.getDistance( 32*oneMinute , 60*oneMinute )
        d2 = animal.getDistanceSpecZone( 32*oneMinute , 60*oneMinute , xa=120, xb=250, ya=210, yb=340 )
        t2 = animal.getCountFramesSpecZone( 32*oneMinute , 60*oneMinute , xa=120, xb=250, ya=210, yb=340)
        sap2=len(animal.getSap(tmin=32*oneMinute, tmax=60*oneMinute, xa=120, xb=250, ya=210, yb=340)) 
                  
        n = n+1
        
        text_file.write( "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format( file, animal.RFID, animal.genotype, animal.user1, d1*10/57, dt1*10/57, t1, sap1, d2*10/57, dt2*10/57, t2, sap2 ) )
        
    fig.suptitle('Single object exploration', fontsize=14, fontweight='bold') 
    plt.show()
    fig.savefig('single_obj_explo.pdf', transparent=False, dpi=80, bbox_inches="tight")
    
    text_file.write( "\n" )
    text_file.close()
    

   
       