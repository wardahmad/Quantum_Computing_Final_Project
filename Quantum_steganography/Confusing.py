#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 18:13:38 2024

@author: khawlahd
"""

def Confusing(BSM):
    
    
    random_steps=3
    FBSM=[] 
    index_=[]
    x=0
    
    #create FBSM and Indexes
    for i in range(len(BSM)):
             FBSM.append(BSM[i])
             index_.append('1')
             x+=1
             if x==2:
                 FBSM.append('x')
                 index_.append('0')
                 x=0

    #converting lists to strings
    FBSM = ''.join(str(i) for i in FBSM )
    index_ = ''.join(str(i) for i in index_ )
    
    return FBSM,index_