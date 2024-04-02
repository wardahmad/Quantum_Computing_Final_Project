from qiskit import ClassicalRegister , QuantumCircuit ,QuantumRegister ,execute , Aer
from bitstring import BitArray
from PIL import Image
import numpy as np


d=[]
def qr():
 x=8
 qb=QuantumRegister(x)
 cb=ClassicalRegister(x)
 qr=QuantumCircuit(qb,cb)
 qr.h(qb)
 qr.measure(qb,cb)
 backend= Aer.get_backend('qasm_simulator')
 job=execute(qr,backend,shots= 1)
 output=job.result().get_counts()
 k=list(output.keys())
 # print(k) 
 o=k[0]
 b =BitArray(bin=o)
 s=b.uint

 # print("random output:",k)
 return s
print(qr())
# print(b.uint)



img = np.zeros(shape=(20,10,3), dtype=np.uint8)
for i in range(20):
 for j in range(10):              
  img[i][j] = [qr(),qr(),qr()] 

img2 = Image.fromarray(img)  
img2.save('om.png')