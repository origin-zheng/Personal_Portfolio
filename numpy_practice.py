import numpy as np
array = np.array([[1,2,3],
                 [2,3,4]], dtype = np.int64)
print(array)

array1 = np.zeros((2,3), dtype = np.int64)
array2  = np.ones((3,2),dtype = np.int64)
array3 = np.arange(10,22,2).reshape(2,3)
array4 = np.linspace(0, 15, 4, dtype = np.int64).reshape(2,2)
print(array4)