import pandas as pd
import numpy as np
s1 = pd.Series([1,2,3,4],index = ['q','w','e','r'])
s2 = pd.Series({'a':1,'b':2,'c':3,'d':4})
s3 = pd.Series(np.arange(1,5,2))
print(s1)
print(s2)
print(s3)