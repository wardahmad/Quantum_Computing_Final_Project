#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 17:26:52 2024

@author: khawlahd
"""


"""
Require: Cover Image (CI), Secret Message (SM)
1: CI: Cover Image
2: SI: Stego Image
3: SM: Secret Message
4: BSM: Binary Secret Message
5: Index_: Binary to determain which Qubit to measure
6: Stego: Stego Image, Decoded Message
"""



import cv2
from Confusing import Confusing 
import numpy as np
"""
Step 3: Encode the Secret Message using Quantum
Circuits
19: Convert the SM into binary.
20: Creat FBSM = BSM pluse Confusing bit after  random_steps 
20: Create a quantum circuit with qubits equal to FBSM length.
22: iterate for 
22: Check bit value of BSM.
23: if bit is ’1’ then
24: Apply an X gate.
25: end if
26: end for
"""

SM="Yo" #17 bit

# convert massage to ASCII code then to  8-bit binary string
#sm=''.join(str(ord(c)) for c in SM)
a_bytes = bytes(SM, "ascii")
BSM=''.join(["{0:b}".format(x) for x in a_bytes])

print("BSM: ",BSM)

#FBMS : confusing string , Index_: indecate what Qubit hold a massage.
FBSM,Index_=Confusing(BSM)

print("FBSM: ",FBSM)
#insert FBSM inside the Qcircit
from qiskit import QuantumCircuit,Aer,execute

l_Index= len(Index_)
qc=QuantumCircuit(l_Index)

for i,s in enumerate(FBSM):
    if s == '1':
        qc.x(i)
    elif s=='x':
        qc.h(i)
    else:
        qc.id(i)
#qc.draw('mpl')
"""
Step 1: Detect Keypoints in the CI
8: Load the CI using OpenCV library.
9: Create a SIFT object.
10: Detect keypoints in the CI using SIFT.
11: Save the keypoints information to a file.
"""
# Loading the image CI
img3 = cv2.imread('/Users/khawlahd/Desktop/cover.jpeg',cv2.IMREAD_COLOR)
#cv2.imwrite('/Users/khawlahd/Desktop/org.jpeg', img3)
img=img3.copy()
print("image size",img.size)
# Converting image to grayscale
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Applying SIFT detector
sift = cv2.SIFT_create()
kp = sift.detect(gray, None)

# Marking the keypoint on the image using circles
img2=cv2.drawKeypoints(gray ,
					kp ,
					img ,
					flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

"""
Step 2: Cluster the Detected Keypoints
13: Load the keypoints file.
14: Convert the keypoints information.
15: Create a K-means object with desired clusters.
16: Perform K-means clustering.
17: Save cluster centers to a file.
"""
from sklearn.cluster import KMeans

pts = cv2.KeyPoint_convert(kp)

kmeans = KMeans(n_clusters=l_Index, random_state=0, n_init="auto").fit(pts)
cluster_center  = kmeans.cluster_centers_
#pixel_centroids = kmeans.labels_ 

"""
Step 4: Encode the Secret Message in the CI
29: Load the CI again.
30: Load cluster centers.
35: for each pixel in CI do
36: Get pixel value.
37: if iterrator < Index length then
38: Calculate new pixel value.
39: Set blue channel to :replace LSB by Index bit.
40: Update SI pixel.
41: Increment iterrator.
42: end if
43: end for
"""
#Creating Stego Image   
stegoImg= img3

for i,m in enumerate(cluster_center):
    #Retreive the location of desiered pixel
    y=int(m[0])
    x=int(m[1])
    # take Blue value 
    pixel_b, pixel_g, pixel_r = stegoImg[x][y]
    # convert to binary
    b=f'{pixel_b:08b}'
    #insert the (index_:which Qubit to measure)
    new_str = b[:-1] + Index_[i]
    # conversion
    blue = int(new_str, 2)
    # Reinsert the pixel in image 
    stegoImg[x][y] = np.array([blue,pixel_g, pixel_r], dtype=np.uint8)
    #Stop when the string end
    if i ==l_Index:
        break
cv2.imwrite('/Users/khawlahd/Desktop/stegoImg.jpeg', stegoImg)
   
 
   
"""
#########################################
#           RESERVER
########################################

# 1- measure the circit
# 2- calculate LSB
    #as the code has no server applyment, We skip this step and use the list apove
# 3- get the massage
"""
qc.measure_all()
job= execute(qc, Aer.get_backend('qasm_simulator'))
output_ = list(job.result().get_counts())[0]
output_=output_[::-1]

print(output_)
massage=""

for i,data in  enumerate(output_) :
    if Index_[i]=='1':
        massage=massage+data

     
# 3- convert Binary to string

Bmassage_len=len(massage)

secrt=''
byte=[(massage[i:i+7]) for i in range(0, len(massage), 7)]
for i in byte:
    binary_int = int(i, 2);
    import math
   
    # Getting the byte number
    byte_number = math.ceil(Bmassage_len / 7)
   
    # Getting an array of bytes
    binary_array = binary_int.to_bytes(byte_number, "big")

    # Converting the array into ASCII text
    ascii_text = binary_array.decode()
    secrt += ascii_text
# printing the result
print("The Secret Massage is:", secrt)



