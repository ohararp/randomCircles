# code.Pylet - Circle Packing
# watch the video here - https://youtu.be/HLUqDIOng80
# Any questions? Just ask!

import random
import math
import pygame
import cv2
from dxfwrite import DXFEngine as dxf
import os

Win,Hin = 14.5,24
W=round(Win*25.4)
H=round(Hin*25.4)

# Desired Density 
densityDesired = 0.55

# Minimum Circle Radius
minRadius = 5 # mm 

# Maximum Circle Radius - Govern by Code
maxRadius = 50 # mm

# Gap Between Circles
minGap = 10 # mm

borderGap = 25 #mm

#------------------------------------------------------------------------------
# Global Variables
#------------------------------------------------------------------------------

areaTotal = W*H
density = 0

# Add a Border Around Default Panel Size
xMin = borderGap
xMax = W-borderGap
yMin = borderGap
yMax = H-borderGap
areaInsideBorder = (xMax-xMin)*(yMax-yMin)
densInsideBorder = 0

# Number of Seed Circles
startCircles=1

# Seed the Circles a minimum Radius from the Border - Using Lists
x=[int(round(W/2)),1]
y=[int(round(H/2)),1]
r=[minRadius,1]

# Factor to Grow the Radius Per Each Iteration
radGrow = 1

# While Loop Iterations for Density
iterations = 0
maxIterations = int(1E5)

#------------------------------------------------------------------------------
# Sub Functions
#------------------------------------------------------------------------------
# Perform a Size Test
#------------------------------------------------------------------------------
def tests(x_,y_,r_,xMin_,xMax_,yMin_,yMax_,maxRadius_):
    if x_ + r_ > xMax_ or x_ -  r_ < xMin_ or y_ + r_ > yMax_ or y_ -r_ < yMin_ or r_ > maxRadius_:
        return 1
    else:
        return 0
#------------------------------------------------------------------------------
# Create a New Circle
#------------------------------------------------------------------------------        
def newCircle(xMin_,xMax_,yMin_,yMax_,minRadius_):
    xNew_=random.randint(xMin_+minRadius_,xMax_-minRadius_)
    yNew_=random.randint(yMin_+minRadius_,yMax_-minRadius_)
    rNew_=minRadius_;
    return xNew_,yNew_,rNew_

#------------------------------------------------------------------------------
# Test Overlap and Boundary
#------------------------------------------------------------------------------
def overlapAndBoundary(x_,y_,r_,xNew_,yNew_,rNew_,xMin_,xMax_,yMin_,yMax_,maxRadius_,minGap_):
    overlap = 0
    b=0
    # Test Overlap Against All Circles
    for n in range(0,len(x_)):
        disBetweenCircles = math.hypot(x_[n]-xNew_,y_[n]-yNew_)
        combinedRadius = r_[n] + rNew
        actGap = disBetweenCircles - combinedRadius
        if actGap <= minGap_:
            overlap = 1
            break
            #print("Overlap Found - %d" % rNew)
        else:
            overlap = 0
        
    # Test Boundary of the Circle to the Border
    if xNew_ + rNew_ > xMax_ or xNew_ -  rNew_ < xMin_ or yNew_ + rNew_ > yMax_ or yNew_ -rNew_ < yMin_:
        b = 1
        #print("Boundary Found - %d" % rNew)
    else:
        b = 0    
        
    if  rNew_ > maxRadius_:
        r = 1
        #print("Max Radius Reached - %d" % rNew)
    else:
        r=0
        
    #print("Iter- %d Rnew- %d Dis - %d Rad - %d Act - %d %d %d" % (n,rNew,disBetweenCircles,combinedRadius,actGap,minGap,overlap))    
    if overlap == 1 or b == 1 or r == 1:
        return 1
    else:
        return 0
    
#------------------------------------------------------------------------------
# Main Loop
#------------------------------------------------------------------------------
m=0
areaCovered=0
print("Starting Circle Generation")
    
# Begin Adding Circles and Detect Overlaps
#while densityBorder < densityDesired:
for j in range(0,maxIterations):        
# Generate a New Circle
    [xNew,yNew,rNew]=newCircle(xMin,xMax,yMin,yMax,minRadius) 
    while overlapAndBoundary(x,y,r,xNew,yNew,rNew,xMin,xMax,yMin,yMax,maxRadius,minGap)==0:
        # Subtract Growth Factor Since Last Test Failed
        rNew=rNew+radGrow
    
    # Subtract Growth Factor Since Last Test Failed
    rNew=rNew-radGrow;

    #print("Exited First While Loop")
    # Re-Do Test Since an Initial New May Not Overlap
    if overlapAndBoundary(x,y,r,xNew,yNew,rNew,xMin,xMax,yMin,yMax,maxRadius,minGap)==0:
        x.append(xNew)
        y.append(yNew)
        r.append(rNew)
       
    #Calculate Density
    areaCircle=0
    for n in range(0,len(x)):     
        areaCircle=areaCircle+(math.pi*r[n]**2)
    
    density = areaCircle/(areaInsideBorder)
        
    if density > densityDesired:
        print("Density Reached")
        break
#------------------------------------------------------------------------------
# Export Dxf
#------------------------------------------------------------------------------
fileName=("Panel-%dx%d-0.dxf" % (Win,Hin))
fctr=0
while os.path.isfile(fileName) == True:
    fctr += 1
    fileName=("Panel-%dx%d-%d.dxf" % (Win,Hin,fctr))

print("Outputting DXF - %s" % fileName)     
drawing = dxf.drawing(fileName)
for n in range(0,len(x)):
    circle = dxf.circle(r[n], (x[n], y[n]))
    drawing.add(circle)
    
drawing.add(dxf.rectangle((0,0),W,H))
drawing.save()
  
#------------------------------------------------------------------------------
# Write image to jpeg
#------------------------------------------------------------------------------
imageName=("Panel-%dx%d-0.jpg" % (Win,Hin))
fctr=0
while os.path.isfile(imageName) == True:
    fctr += 1
    imageName=("Panel-%dx%d-%d.jpg" % (Win,Hin,fctr))

print("Outputting JPG - %s" % imageName)    
image = pygame.Surface((W, H))
for n in range(0,len(x)):
	pygame.draw.circle(image, (255, 255, 255), (x[n], y[n]), r[n], 1)

pygame.image.save(image, imageName)
print("Done")

#------------------------------------------------------------------------------
# Open Image for Display Using OpenCV
#------------------------------------------------------------------------------
cvImage = cv2.imread(imageName)
print(type(image))
imS = cv2.resize(cvImage, (1280, 1024)) 
cv2.imshow('Test image',cvImage)
cv2.waitKey(0)
cv2.destroyAllWindows()
