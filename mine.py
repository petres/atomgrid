#!/bin/python2
import numpy as np
import matplotlib.image as MImage
import matplotlib.pyplot as plt
import scipy.stats as st
from PIL import Image, ImageFilter, ImageDraw

import sys
import os

# Flush STDOUT continuously
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

orgFileName = "11_NP3_011_0.bmp"
size = (1024, 1024)  # width and height of image in pixels
#size = (300, 300)  # width and height of image in pixels

######### SOME AUX FUNCTIONS #########
def gkern(kernlen=21, nsig=3):
    """Returns a 2D Gaussian kernel array."""

    interval = (2*nsig+1.)/(kernlen)
    x = np.linspace(-nsig-interval/2., nsig+interval/2., kernlen+1)
    kern1d = np.diff(st.norm.cdf(x))
    kernel_raw = np.sqrt(np.outer(kern1d, kern1d))
    kernel = kernel_raw/kernel_raw.sum()
    return kernel

def saveImage(name, matrix = None, format = "BMP", image = None):
    print " -> Saving Image " + name + " ...",
    if image is not None:
        pass
    elif matrix is not None:
        image =  Image.fromarray(matrix)
    else:
        raise ValueError("matrix or image must be specified")

    image.save("dst/" + name + "." + format.lower(), format)
    print "DONE"
    return image


#######################################

print "Loading and Converting Image ...",
orgImg = Image.open("src/" + orgFileName, mode = 'r').convert()

try:
    orgImg = orgImg.convert().crop((0,0,size[0],size[1]))
except NameError:
    size = orgImg.size


orgGreyscaleMatrix = MImage.pil_to_array(orgImg.convert('L'))

emptyGreyscaleMatrix = MImage.pil_to_array(Image.new('L', size, 0))
emptyColoredMatrix = MImage.pil_to_array(Image.new('RGB', size, (0,0,0)))
print "DONE"


# print "Compute the 2-dimensional FFT ...",
# #print "."
# m = np.fft.rfft2(orgGreyscaleMatrix)
# #print m.shape
# #print m
# #print np.amax(m)
# am = np.log(np.absolute(m)+1)
# mm = np.around(am/np.amax(am)*255, decimals=0).astype(np.uint8)
# print "DONE"
# #print orgGreyscaleMatrix
# #print orgGreyscaleMatrix[1, 1]
# #print mm
# #print mm[1, 1]
# saveImage("fft", mm)



print "Gaussian Filter ... ",
gaussianMatrix = emptyGreyscaleMatrix*0
kernelSize = 7
matrix = gkern(kernelSize)
for i in range(size[1] - (kernelSize - 1)):
    for j in range(size[0] - (kernelSize - 1)):
        iS = i + (kernelSize - 1)/2
        jS = j + (kernelSize - 1)/2
        #print t[i:(i + kernelSize), j:(j + kernelSize)]
        gaussianMatrix[iS, jS] = np.sum(np.multiply(orgGreyscaleMatrix[i:(i + kernelSize), j:(j + kernelSize)], matrix))
        #s[iS, jS] = np.sum(t[i:(i + kernelSize), j:(j + kernelSize)],)/kernelSize**2

print "DONE"



# SAVING GAUSSIAN
saveImage("gaussian", gaussianMatrix)


print "Kernel Max Filter and Create Concordance ...",
maxMatrix = emptyGreyscaleMatrix * 0
concordanceMatrix = emptyGreyscaleMatrix * 0
kernelSize = 9
for i in range(size[1] - (kernelSize - 1)):
    for j in range(size[0] - (kernelSize - 1)):
        iS = i + (kernelSize - 1)/2
        jS = j + (kernelSize - 1)/2
        #print t[i:(i + kernelSize), j:(j + kernelSize)]
        maxMatrix[iS, jS] = np.amax(gaussianMatrix[i:(i + kernelSize), j:(j + kernelSize)])
        if maxMatrix[iS, jS] == gaussianMatrix[iS, jS]:
            concordanceMatrix[iS, jS] = 1
        #print iS, jS;
        #exit();
print "DONE"



saveImage("max", maxMatrix)
concordanceImg = saveImage("concordance", concordanceMatrix*255)


print "Color Concordance Image ... ",
coloredConcordanceMatrix = emptyColoredMatrix * 0
for i in range(size[1]):
    for j in range(size[0]):
        if concordanceMatrix[i, j] == 1:
            coloredConcordanceMatrix[i, j] = (255, 0, 0)
print "DONE"




coloredConcordanceImg = Image.fromarray(coloredConcordanceMatrix, 'RGB')

compositeImg = Image.composite(coloredConcordanceImg, orgImg.convert("RGB"), concordanceImg)
saveImage("composite", image = compositeImg)

#exit()

print "Finding Centers ...",
kernelSize = 35 # ODD
maxCenterSize = 2
movingSize = 20

centerMatrix = emptyGreyscaleMatrix * 0

compImgDraw = ImageDraw.Draw(compositeImg)


arcs = []
dir1 = 73
dir2 = 145
tolerance = 20
maxLength = 18

for i in range(0, size[1] - (kernelSize - 1), movingSize):
    for j in range(0, size[0] - (kernelSize - 1), movingSize):
        iS = i + (kernelSize - 1)/2
        jS = j + (kernelSize - 1)/2
        areaCenterDict = {}
        resetList = []
        #print "Window centered at " + str((iS, jS)) + " size: " + str((kernelSize, kernelSize)) + " borders: " + str((iS - (kernelSize - 1)/2, jS - (kernelSize - 1)/2, iS + (kernelSize - 1)/2, jS + (kernelSize - 1)/2)) +" :"
        for ii in range(0, kernelSize):
            for jj in range(0, kernelSize):
                iiS = iS - (kernelSize - 1)/2 + ii
                jjS = jS - (kernelSize - 1)/2 + jj
                if concordanceMatrix[iiS , jjS] == 1:
                    concordanceMatrix[iiS, jjS] = 0
                    resetList.append((iiS, jjS))
                    centerInfo = { "pixels": []}
                    centerInfo["pixels"].append((iiS, jjS))

                    leftLimit = 0
                    if ii == 0:
                        leftLimit = -1

                    topLimit = 0
                    if jj == 0:
                        topLimit = -1

                    for ci in range(leftLimit*maxCenterSize, maxCenterSize + 1):
                        for cj in range(topLimit*maxCenterSize, maxCenterSize + 1):
                            if ci == 0 and cj == 0:
                                continue
                            if concordanceMatrix[iiS + ci, jjS + cj] == 1:
                                concordanceMatrix[iiS + ci, jjS + cj] = 0
                                resetList.append((iiS + ci, jjS + cj))
                                centerInfo["pixels"].append((iiS + ci, jjS + cj))
                    areaCenterDict[(iiS, jjS)] = centerInfo

        for x, y in resetList:
            #print "reseting " + str((x, y))
            concordanceMatrix[x, y] = 1

        #print len(areaCenterDict)

        for center1 in areaCenterDict:
            for center2 in areaCenterDict:
                if center1 == center2:
                    continue
                dist1 = center1[1] - center2[1]
                dist2 = center1[0] - center2[0]
                vLength = np.sqrt(dist1**2 + dist2**2)
                # Maximum Distance To Connect
                if vLength < maxLength:
                    arc = np.arccos(dist1/vLength)/(2*np.pi)*360
                    if dist2 > 0:
                        arc = 360 - arc
                    arcs.append(arc)
                    if abs(arc - dir1) < tolerance or abs(arc - dir2) < tolerance:
                        compImgDraw.line([center1[1], center1[0], center2[1], center2[0]], "green")


        #centerMatrix[iS, jS] = 255
print "DONE"
#a, b = np.histogram(arcs, 100)
#for i, e in enumerate(a):
#    print a[i], ":", b[i]
#plt.hist(arcs, 100)
#plt.show()

#saveImage("withLines", image = compositeImg)

compositeImg = Image.composite(coloredConcordanceImg, compositeImg, concordanceImg)
saveImage("withLines", image = compositeImg)
