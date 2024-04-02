#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 15:34:17 2024

@author: wardah
"""

print('Quantum OTP')

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute, Aer, AncillaRegister
from qiskit.visualization import plot_histogram
import numpy as np
import time

# Generate Random Number
def generate_random_number():
    qr = QuantumRegister(8, name='qubits')
    cr = ClassicalRegister(4, name='encoding bit')
    cr2 = ClassicalRegister(4, name='OTP')
    qc = QuantumCircuit(qr, cr, cr2)

    qc.h([0, 1, 2, 3])
    qc.measure([0, 1, 2, 3], [0, 1, 2, 3])
    qc.barrier(label="QRNG") # QRNG => Quantum Random Number Generation
    
    # create an entanglement
    qc.h(4)
    qc.cx(4, 5)
    qc.h(6)
    qc.cx(6, 7)
    
    # If Condition
    qc.x(qr[4]).c_if(cr[0], 1)
    qc.z(qr[4]).c_if(cr[1], 1)
    qc.x(qr[6]).c_if(cr[2], 1)
    qc.z(qr[6]).c_if(cr[3], 1)
    
    qc.cx(4, 5)
    qc.h(4)
    qc.cx(6, 7)
    qc.h(6)
    qc.barrier(label='OTP')
    
    qc.measure([4, 5, 6, 7], [4, 5, 6, 7])

    job = execute(qc, Aer.get_backend('qasm_simulator'), shots=1)
    output = job.result().get_counts()
    # qc.draw('mpl')

    cr2_bits = next(iter(output.keys()))[-4:]
    number = int(cr2_bits, 2) % 10 
    return number

# Update OTP value after 30 seconds
def update_OTP():
    time.sleep(30)  # Wait for 30 seconds
    OTP = np.random.randint(9, size=4)
    OTPString = ''.join(str(num) for num in OTP)
    print('Updated OTP:', OTP)
    print("Updated OTPString:", OTPString)

# generate_random_number()
OTP =[generate_random_number() for i in  range(4)]
print(OTP)

# Convert from array to string
OTPString = ''.join(str(num) for num in OTP)
print(OTPString)

# After 30 Seconds, OTP and OTPString Values will be updated
# update_OTP()

__all__ = ['generate_random_number']