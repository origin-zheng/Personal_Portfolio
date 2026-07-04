import pandas as pd
import numpy as np
'''
s1 = pd.Series([1,2,3,4],index = ['q','w','e','r'])
s2 = pd.Series({'a':1,'b':2,'c':3,'d':4})
s3 = pd.Series(np.arange(1,5,2))
'''
s4 = pd.Series([i for i in range(7)],index = ['a','b','c','d','e','f','g'])

print(s4.values)
print(s4.index)
print(s4['c'])
s4['c'] = 99
print(s4)